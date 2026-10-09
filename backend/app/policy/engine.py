from typing import List, Optional
from app.ir.schemas import ActionIR, SimulationResult, RiskLevel
from app.policy.rules import DEFAULT_POLICY_RULES, PolicyRule
from app.config import settings

class PolicyEngine:
    def __init__(self, rules: Optional[List[PolicyRule]] = None):
        self.rules = rules or list(DEFAULT_POLICY_RULES)

    def add_rule(self, rule: PolicyRule) -> None:
        self.rules.append(rule)

    def evaluate(self, action: ActionIR) -> SimulationResult:
        violations: List[str] = []

        # 1. Evaluate explicit predicate rules
        for rule in self.rules:
            allowed, reason = rule.predicate(action)
            if not allowed:
                violations.append(f"[{rule.rule_id}] {reason}")

        if violations:
            return SimulationResult(
                action_id=action.action_id,
                allowed=False,
                requires_approval=True,
                blast_radius_score=action.blast_radius_score,
                risk_level=RiskLevel.CRITICAL,
                reasons=violations,
                impact_summary="Action blocked by security policy rules."
            )

        # 2. Evaluate blast radius threshold
        requires_approval = action.blast_radius_score > settings.AUTO_APPROVE_BLAST_RADIUS_THRESHOLD

        impact_summary = (
            f"Action evaluated with risk score {action.blast_radius_score:.1f}/100. "
            + ("Requires human approval before execution." if requires_approval else "Approved for automatic execution.")
        )

        return SimulationResult(
            action_id=action.action_id,
            allowed=True,
            requires_approval=requires_approval,
            blast_radius_score=action.blast_radius_score,
            risk_level=action.risk_level,
            reasons=[],
            impact_summary=impact_summary
        )
