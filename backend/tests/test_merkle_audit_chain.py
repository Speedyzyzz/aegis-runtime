from app.coordinator.merkle_audit import MerkleAuditLedger
from app.ir.normalizer import ActionIRNormalizer
from app.ir.schemas import ActionStatus

def test_merkle_chain_tamper_detection():
    ledger = MerkleAuditLedger()

    a1 = ActionIRNormalizer.normalize("fs_write", {"path": "/tmp/a.txt"}, "s1", "k1")
    a2 = ActionIRNormalizer.normalize("fs_write", {"path": "/tmp/b.txt"}, "s1", "k2")

    r1 = ledger.append_receipt(a1, ActionStatus.COMMITTED)
    r2 = ledger.append_receipt(a2, ActionStatus.COMMITTED)

    assert r2.previous_receipt_hash == r1.merkle_root_hash
    assert ledger.verify_integrity() is True

    # Tamper with r1's action_ir_hash
    ledger.receipts[0].action_ir_hash = "tampered_hash_deadbeef"
    assert ledger.verify_integrity() is False
