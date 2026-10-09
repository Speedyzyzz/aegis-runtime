from app.ir.normalizer import ActionIRNormalizer
from app.ir.schemas import ActionDomain, RiskLevel

def test_sql_normalization():
    action = ActionIRNormalizer.normalize(
        tool_name="sql_query",
        arguments={"query": "SELECT * FROM users WHERE id = 1", "table": "users"},
        session_id="sess_test",
        idempotency_key="idem_001"
    )
    assert action.domain == ActionDomain.DATABASE
    assert action.operation == "query"
    assert action.risk_level == RiskLevel.LOW
    assert action.blast_radius_score == 0.0

def test_destructive_sql_normalization():
    action = ActionIRNormalizer.normalize(
        tool_name="database_exec",
        arguments={"query": "DROP TABLE accounts;", "table": "accounts"},
        session_id="sess_test",
        idempotency_key="idem_002"
    )
    assert action.domain == ActionDomain.DATABASE
    assert action.operation == "drop"
    assert action.risk_level == RiskLevel.CRITICAL
    assert action.blast_radius_score == 100.0

def test_filesystem_normalization():
    action = ActionIRNormalizer.normalize(
        tool_name="fs_write",
        arguments={"path": "/tmp/aegis_sandbox/report.txt", "content": "data"},
        session_id="sess_test",
        idempotency_key="idem_003"
    )
    assert action.domain == ActionDomain.FILESYSTEM
    assert action.operation == "write"
    assert action.rollback_recipe is not None
