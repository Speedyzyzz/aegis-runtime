from typing import Any, Dict, Optional, Tuple
from app.ir.schemas import ActionIR, ActionStatus, SimulationResult, AuditReceipt
from app.policy.engine import PolicyEngine
from app.policy.attenuation import CapabilityTokenManager
from app.coordinator.merkle_audit import MerkleAuditLedger
from app.coordinator.rollback_engine import RollbackEngine

class TwoPhaseCommitCoordinator:
    def __init__(
        self,
        policy_engine: Optional[PolicyEngine] = None,
        token_manager: Optional[CapabilityTokenManager] = None,
        audit_ledger: Optional[MerkleAuditLedger] = None
    ):
        self.policy_engine = policy_engine or PolicyEngine()
        self.token_manager = token_manager or CapabilityTokenManager()
        self.audit_ledger = audit_ledger or MerkleAuditLedger()
        
        # In-memory stores (in production backed by DB models)
        self.prepared_actions: Dict[str, ActionIR] = {}
        self.action_statuses: Dict[str, ActionStatus] = {}
        self.idempotency_cache: Dict[str, Tuple[ActionStatus, Optional[AuditReceipt]]] = {}

    def prepare(self, action: ActionIR) -> Tuple[SimulationResult, Optional[str]]:
        # 1. Idempotency Check
        if action.idempotency_key in self.idempotency_cache:
            status, receipt = self.idempotency_cache[action.idempotency_key]
            return SimulationResult(
                action_id=action.action_id,
                allowed=(status in [ActionStatus.APPROVED, ActionStatus.COMMITTED]),
                requires_approval=False,
                blast_radius_score=action.blast_radius_score,
                risk_level=action.risk_level,
                reasons=[f"Action previously processed with status: {status.value}"],
                impact_summary="Idempotency match: duplicate action detected."
            ), None

        # 2. Evaluate Policy & Blast Radius
        sim_res = self.policy_engine.evaluate(action)
        self.prepared_actions[action.action_id] = action

        if not sim_res.allowed:
            self.action_statuses[action.action_id] = ActionStatus.REJECTED
            self.idempotency_cache[action.idempotency_key] = (ActionStatus.REJECTED, None)
            return sim_res, None

        if sim_res.requires_approval:
            self.action_statuses[action.action_id] = ActionStatus.PENDING_APPROVAL
            return sim_res, None

        # Auto-approved: Issue capability token for atomic commit
        self.action_statuses[action.action_id] = ActionStatus.APPROVED
        cap = self.token_manager.issue_token(
            action_id=action.action_id,
            session_id=action.session_id,
            scope=f"{action.domain.value}:{action.operation}"
        )
        return sim_res, cap.token

    def approve_human(self, action_id: str, approver_signature: str) -> Optional[str]:
        action = self.prepared_actions.get(action_id)
        if not action or self.action_statuses.get(action_id) != ActionStatus.PENDING_APPROVAL:
            return None

        self.action_statuses[action_id] = ActionStatus.APPROVED
        cap = self.token_manager.issue_token(
            action_id=action.action_id,
            session_id=action.session_id,
            scope=f"{action.domain.value}:{action.operation}"
        )
        return cap.token

    def commit(self, action_id: str, capability_token: str, signature: str = "sig_auto") -> Tuple[bool, Optional[AuditReceipt], str]:
        action = self.prepared_actions.get(action_id)
        if not action:
            return False, None, "Action not found."

        # 1. Validate capability token (attenuation & TOCTOU protection)
        scope = f"{action.domain.value}:{action.operation}"
        valid_token = self.token_manager.validate_and_consume(capability_token, action_id, scope)
        if not valid_token:
            return False, None, "Invalid, expired, or already-consumed capability token."

        # 2. Execute Action (in production executes via tool adapter)
        self.action_statuses[action_id] = ActionStatus.COMMITTED

        # 3. Append to Merkle Audit Chain
        receipt = self.audit_ledger.append_receipt(action, ActionStatus.COMMITTED, signature=signature)
        self.idempotency_cache[action.idempotency_key] = (ActionStatus.COMMITTED, receipt)

        return True, receipt, "Action committed and cryptographically sealed."

    def rollback(self, action_id: str, reason: str = "aborted") -> Optional[AuditReceipt]:
        action = self.prepared_actions.get(action_id)
        if not action:
            return None

        self.action_statuses[action_id] = ActionStatus.ROLLED_BACK
        receipt = self.audit_ledger.append_receipt(action, ActionStatus.ROLLED_BACK, signature=f"rollback:{reason}")
        self.idempotency_cache[action.idempotency_key] = (ActionStatus.ROLLED_BACK, receipt)
        return receipt
