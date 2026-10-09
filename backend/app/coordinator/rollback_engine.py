from typing import Any, Dict, Optional
from app.ir.schemas import ActionIR, ActionDomain

class RollbackEngine:
    @staticmethod
    def generate_compensating_action(action: ActionIR) -> Optional[Dict[str, Any]]:
        """
        Synthesizes an inverse compensating action to revert side effects.
        """
        if not action.rollback_recipe:
            return None

        recipe = action.rollback_recipe
        if action.domain == ActionDomain.FILESYSTEM:
            return {
                "domain": "filesystem",
                "operation": "revert",
                "path": action.parameters.get("path"),
                "instruction": "Restore previous snapshot or delete newly created file"
            }
        elif action.domain == ActionDomain.DATABASE:
            return {
                "domain": "database",
                "operation": "rollback_transaction",
                "instruction": "Issue compensating DELETE or RESTORE statement"
            }
        elif action.domain == ActionDomain.PAYMENT:
            return {
                "domain": "payment",
                "operation": "refund",
                "instruction": "Execute full refund on charge_id"
            }
        return None
