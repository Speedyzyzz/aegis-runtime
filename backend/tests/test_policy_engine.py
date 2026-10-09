from app.policy.engine import PolicyEngine
from app.ir.normalizer import ActionIRNormalizer

def test_policy_blocks_sql_drop():
    engine = PolicyEngine()
    action = ActionIRNormalizer.normalize(
        tool_name="sql_query",
        arguments={"query": "DROP TABLE transactions;"},
        session_id="sess_sec",
        idempotency_key="key_01"
    )
    result = engine.evaluate(action)
    assert result.allowed is False
    assert result.requires_approval is True
    assert any("RULE_DENY_SQL_DROP" in r for r in result.reasons)

def test_policy_blocks_root_fs():
    engine = PolicyEngine()
    action = ActionIRNormalizer.normalize(
        tool_name="fs_write",
        arguments={"path": "/etc/hosts", "content": "127.0.0.1"},
        session_id="sess_sec",
        idempotency_key="key_02"
    )
    result = engine.evaluate(action)
    assert result.allowed is False
    assert any("RULE_DENY_ROOT_FS" in r for r in result.reasons)

def test_policy_allows_safe_sandbox_action():
    engine = PolicyEngine()
    action = ActionIRNormalizer.normalize(
        tool_name="fs_write",
        arguments={"path": "/tmp/aegis_sandbox/results.json", "content": "{}"},
        session_id="sess_sec",
        idempotency_key="key_03"
    )
    result = engine.evaluate(action)
    assert result.allowed is True
    assert len(result.reasons) == 0
