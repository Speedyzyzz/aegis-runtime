import json
from typing import Any, Dict
from app.ir.schemas import ActionIR, ActionDomain, RiskLevel
from app.ir.blast_radius import BlastRadiusCalculator

try:
    import blake3
    def hash_str(val: str) -> str:
        return blake3.blake3(val.encode("utf-8")).hexdigest()
except ImportError:
    import hashlib
    def hash_str(val: str) -> str:
        return hashlib.blake2b(val.encode("utf-8")).hexdigest()

class ActionIRNormalizer:
    @staticmethod
    def normalize(
        tool_name: str,
        arguments: Dict[str, Any],
        session_id: str,
        idempotency_key: str
    ) -> ActionIR:
        t_name = tool_name.lower()
        domain = ActionDomain.NETWORK
        operation = "invoke"
        target_resource = "generic_resource"
        rollback_recipe = None

        if "sql" in t_name or "db" in t_name or "database" in t_name or "query" in t_name:
            domain = ActionDomain.DATABASE
            query = arguments.get("query", "")
            operation = "query"
            target_resource = arguments.get("table", "unknown_table")
            if "INSERT INTO" in query.upper():
                operation = "insert"
            elif "DELETE FROM" in query.upper():
                operation = "delete"
            elif "DROP" in query.upper():
                operation = "drop"

        elif "fs" in t_name or "file" in t_name or "write" in t_name:
            domain = ActionDomain.FILESYSTEM
            operation = arguments.get("action", "write" if "write" in t_name else "read")
            target_resource = arguments.get("path", "unknown_file")
            if operation == "write":
                rollback_recipe = {
                    "undo_operation": "restore_or_delete",
                    "path": target_resource,
                    "previous_content_hash": arguments.get("previous_hash")
                }

        elif "stripe" in t_name or "pay" in t_name or "billing" in t_name:
            domain = ActionDomain.PAYMENT
            operation = arguments.get("action", "charge")
            target_resource = arguments.get("customer_id", "unknown_customer")
            if operation == "charge":
                rollback_recipe = {
                    "undo_operation": "refund",
                    "charge_id": None # Populated post-execution
                }

        elif "git" in t_name or "vcs" in t_name:
            domain = ActionDomain.VCS
            operation = arguments.get("action", "push")
            target_resource = arguments.get("repo", "current_repo")

        # Calculate blast radius
        score, risk_lvl, summary = BlastRadiusCalculator.calculate(
            domain, operation, target_resource, arguments
        )

        canonical_data = {
            "session_id": session_id,
            "domain": domain.value,
            "operation": operation,
            "target_resource": target_resource,
            "parameters": arguments
        }
        canonical_str = json.dumps(canonical_data, sort_keys=True, separators=(",", ":"), default=str)
        action_id = hash_str(canonical_str)

        return ActionIR(
            action_id=action_id,
            idempotency_key=idempotency_key,
            session_id=session_id,
            domain=domain,
            operation=operation,
            target_resource=target_resource,
            parameters=arguments,
            blast_radius_score=score,
            risk_level=risk_lvl,
            required_capabilities=[f"{domain.value}:{operation}"],
            rollback_recipe=rollback_recipe
        )
