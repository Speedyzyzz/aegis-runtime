from typing import Any, Callable, Dict, List
from app.ir.schemas import ActionIR, ActionDomain, RiskLevel

class PolicyRule:
    def __init__(self, rule_id: str, description: str, predicate: Callable[[ActionIR], tuple[bool, str]]):
        self.rule_id = rule_id
        self.description = description
        self.predicate = predicate

def rule_deny_sql_drops(action: ActionIR) -> tuple[bool, str]:
    if action.domain == ActionDomain.DATABASE:
        query = str(action.parameters.get("query", "")).upper()
        if "DROP DATABASE" in query or "DROP TABLE" in query:
            return False, "DROP statements strictly forbidden without explicit human approval."
    return True, ""

def rule_deny_root_fs(action: ActionIR) -> tuple[bool, str]:
    if action.domain == ActionDomain.FILESYSTEM:
        path = str(action.parameters.get("path", ""))
        if path.startswith(("/etc", "/usr", "/bin", "/System", "/root")) or path == "/":
            return False, f"Access to system filesystem path '{path}' is denied."
    return True, ""

def rule_deny_force_push_prod(action: ActionIR) -> tuple[bool, str]:
    if action.domain == ActionDomain.VCS:
        branch = str(action.parameters.get("branch", "")).lower()
        force = bool(action.parameters.get("force", False))
        if branch in ["main", "master", "prod"] and force:
            return False, f"Force-push to branch '{branch}' is forbidden."
    return True, ""

DEFAULT_POLICY_RULES: List[PolicyRule] = [
    PolicyRule("RULE_DENY_SQL_DROP", "Deny destructive SQL drops", rule_deny_sql_drops),
    PolicyRule("RULE_DENY_ROOT_FS", "Deny root filesystem writes", rule_deny_root_fs),
    PolicyRule("RULE_DENY_FORCE_PUSH", "Deny force-push to protected branches", rule_deny_force_push_prod),
]
