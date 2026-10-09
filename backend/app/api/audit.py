from fastapi import APIRouter
from app.api.actions import coordinator

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/chain")
async def get_audit_chain():
    receipts = [r.model_dump() for r in coordinator.audit_ledger.receipts]
    return {
        "total_receipts": len(receipts),
        "latest_root_hash": coordinator.audit_ledger.latest_hash,
        "receipts": receipts
    }

@router.get("/verify")
async def verify_chain():
    is_valid = coordinator.audit_ledger.verify_integrity()
    return {
        "valid": is_valid,
        "verified_receipt_count": len(coordinator.audit_ledger.receipts),
        "tamper_detected": not is_valid
    }
