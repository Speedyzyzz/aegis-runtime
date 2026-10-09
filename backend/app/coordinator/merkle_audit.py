import json
import time
from typing import List, Optional
from app.ir.schemas import ActionIR, ActionStatus, AuditReceipt

try:
    import blake3
    def hash_str(val: str) -> str:
        return blake3.blake3(val.encode("utf-8")).hexdigest()
except ImportError:
    import hashlib
    def hash_str(val: str) -> str:
        return hashlib.blake2b(val.encode("utf-8")).hexdigest()

class MerkleAuditLedger:
    def __init__(self, genesis_hash: str = "0000000000000000000000000000000000000000000000000000000000000000"):
        self.genesis_hash = genesis_hash
        self.receipts: List[AuditReceipt] = []

    @property
    def latest_hash(self) -> str:
        if not self.receipts:
            return self.genesis_hash
        return self.receipts[-1].merkle_root_hash

    def append_receipt(self, action: ActionIR, status: ActionStatus, signature: str = "sig_auto") -> AuditReceipt:
        prev_hash = self.latest_hash
        action_ir_str = json.dumps(action.model_dump(), sort_keys=True, default=str)
        action_hash = hash_str(action_ir_str)

        commit_epoch = time.time()
        # Merkle-chain linking: hash(prev_hash + action_hash + status + epoch + signature)
        node_payload = f"{prev_hash}:{action_hash}:{status.value}:{commit_epoch}:{signature}"
        merkle_root = hash_str(node_payload)
        receipt_id = f"rcpt_{merkle_root[:16]}"

        receipt = AuditReceipt(
            receipt_id=receipt_id,
            action_id=action.action_id,
            session_id=action.session_id,
            previous_receipt_hash=prev_hash,
            merkle_root_hash=merkle_root,
            action_ir_hash=action_hash,
            status=status,
            committed_at_epoch=commit_epoch,
            signature=signature
        )
        self.receipts.append(receipt)
        return receipt

    def verify_integrity(self) -> bool:
        if not self.receipts:
            return True

        curr_prev = self.genesis_hash
        for r in self.receipts:
            if r.previous_receipt_hash != curr_prev:
                return False  # Chain broken!
            node_payload = f"{r.previous_receipt_hash}:{r.action_ir_hash}:{r.status.value}:{r.committed_at_epoch}:{r.signature}"
            expected_root = hash_str(node_payload)
            if r.merkle_root_hash != expected_root:
                return False  # Node tampered!
            curr_prev = r.merkle_root_hash
        return True
