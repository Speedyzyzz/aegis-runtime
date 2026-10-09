from typing import Any, Dict, Tuple
from app.ir.schemas import ActionDomain, RiskLevel

class BlastRadiusCalculator:
    @staticmethod
    def calculate(
        domain: ActionDomain,
        operation: str,
        target_resource: str,
        parameters: Dict[str, Any]
    ) -> Tuple[float, RiskLevel, str]:
        op = operation.lower()
        res = target_resource.lower()

        if domain == ActionDomain.DATABASE:
            sql_query = str(parameters.get("query", "")).upper()
            if "DROP DATABASE" in sql_query or "DROP TABLE" in sql_query:
                return 100.0, RiskLevel.CRITICAL, "Destructive DDL drop operation"
            if "TRUNCATE" in sql_query:
                return 90.0, RiskLevel.CRITICAL, "Full table truncation"
            if "DELETE" in sql_query and "WHERE" not in sql_query:
                return 85.0, RiskLevel.HIGH, "Unbounded DELETE without WHERE clause"
            if "UPDATE" in sql_query and "WHERE" not in sql_query:
                return 75.0, RiskLevel.HIGH, "Unbounded UPDATE without WHERE clause"
            if "ALTER" in sql_query:
                return 60.0, RiskLevel.HIGH, "Schema modification"
            if "DELETE" in sql_query or "UPDATE" in sql_query:
                return 35.0, RiskLevel.MEDIUM, "Targeted table row modification"
            if "INSERT" in sql_query:
                return 15.0, RiskLevel.LOW, "Row insertion"
            return 0.0, RiskLevel.LOW, "Read-only query"

        elif domain == ActionDomain.FILESYSTEM:
            path = parameters.get("path", target_resource)
            # Detect root-level or critical paths
            if path in ["/", "/etc", "/usr", "/bin", "/System"] or path.startswith(("/etc", "/bin", "/usr")):
                return 100.0, RiskLevel.CRITICAL, "Attempt to access protected system filesystem path"
            if op in ["delete", "remove", "rmdir"]:
                return 60.0, RiskLevel.HIGH, f"File deletion on {path}"
            if op in ["write", "overwrite"]:
                return 30.0, RiskLevel.MEDIUM, f"File write/overwrite on {path}"
            return 5.0, RiskLevel.LOW, f"Read or append on {path}"

        elif domain == ActionDomain.PAYMENT:
            amount = float(parameters.get("amount", 0))
            if op in ["charge", "transfer"]:
                if amount > 1000:
                    return 95.0, RiskLevel.CRITICAL, f"High-value payment of ${amount:.2f}"
                if amount > 250:
                    return 65.0, RiskLevel.HIGH, f"Moderate payment of ${amount:.2f}"
                return 25.0, RiskLevel.LOW, f"Low-value payment of ${amount:.2f}"
            if op == "refund":
                return 40.0, RiskLevel.MEDIUM, f"Refund transaction of ${amount:.2f}"
            return 10.0, RiskLevel.LOW, "Payment status read"

        elif domain == ActionDomain.VCS:
            branch = str(parameters.get("branch", "main")).lower()
            force = bool(parameters.get("force", False))
            if op == "push" and branch in ["main", "master", "prod", "release"] and force:
                return 95.0, RiskLevel.CRITICAL, f"Force-push to protected branch '{branch}'"
            if op == "push" and branch in ["main", "master", "prod"]:
                return 50.0, RiskLevel.MEDIUM, f"Direct push to protected branch '{branch}'"
            if op == "create_branch" or op == "commit":
                return 15.0, RiskLevel.LOW, "Non-destructive VCS commit/branch"
            return 5.0, RiskLevel.LOW, "VCS read/fetch"

        # Default fallback
        return 20.0, RiskLevel.LOW, f"Standard {domain.value} {operation}"
