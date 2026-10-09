from app.coordinator.two_phase_commit import TwoPhaseCommitCoordinator
from app.ir.normalizer import ActionIRNormalizer
from app.ir.schemas import ActionStatus

def test_two_phase_commit_auto_approve_flow():
    coordinator = TwoPhaseCommitCoordinator()
    action = ActionIRNormalizer.normalize(
        tool_name="fs_write",
        arguments={"path": "/tmp/aegis_sandbox/log.txt", "content": "started"},
        session_id="sess_2pc",
        idempotency_key="key_auto"
    )

    # 1. Phase 1: Prepare
    sim_res, token = coordinator.prepare(action)
    assert sim_res.allowed is True
    assert token is not None

    # 2. Phase 2: Commit
    success, receipt, msg = coordinator.commit(action.action_id, token, signature="sig_test")
    assert success is True
    assert receipt is not None
    assert receipt.status == ActionStatus.COMMITTED

    # 3. Idempotency test: duplicate prepare must return cached status and zero duplicate commit
    sim_res2, token2 = coordinator.prepare(action)
    assert token2 is None
    assert "previously processed" in sim_res2.reasons[0]

def test_toctou_tampered_token_rejection():
    coordinator = TwoPhaseCommitCoordinator()
    action1 = ActionIRNormalizer.normalize(
        tool_name="fs_write",
        arguments={"path": "/tmp/aegis_sandbox/safe.txt", "content": "ok"},
        session_id="sess_tamper",
        idempotency_key="key_tamper_1"
    )
    action2 = ActionIRNormalizer.normalize(
        tool_name="fs_write",
        arguments={"path": "/tmp/aegis_sandbox/safe2.txt", "content": "ok2"},
        session_id="sess_tamper",
        idempotency_key="key_tamper_2"
    )
    sim_res1, token1 = coordinator.prepare(action1)
    sim_res2, token2 = coordinator.prepare(action2)
    assert token1 is not None and token2 is not None

    # Attempt to commit action2 using token1 (mismatched action_id tampering)
    success, receipt, msg = coordinator.commit(action2.action_id, token1)
    assert success is False
    assert "Invalid, expired, or already-consumed capability token" in msg

    # Unknown action check
    success_unk, _, msg_unk = coordinator.commit("nonexistent_action", token1)
    assert success_unk is False
    assert "Action not found." in msg_unk
