from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ir.normalizer import ActionIRNormalizer
from app.coordinator.two_phase_commit import TwoPhaseCommitCoordinator

router = APIRouter(prefix="/actions", tags=["Actions"])
coordinator = TwoPhaseCommitCoordinator()

class PrepareRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    session_id: str
    idempotency_key: str

class CommitRequest(BaseModel):
    action_id: str
    capability_token: str
    signature: str = "sig_user"

@router.post("/prepare")
async def prepare_action(req: PrepareRequest):
    action = ActionIRNormalizer.normalize(
        tool_name=req.tool_name,
        arguments=req.arguments,
        session_id=req.session_id,
        idempotency_key=req.idempotency_key
    )
    sim_res, token = coordinator.prepare(action)
    return {
        "action": action.model_dump(),
        "simulation": sim_res.model_dump(),
        "capability_token": token
    }

@router.post("/commit")
async def commit_action(req: CommitRequest):
    success, receipt, msg = coordinator.commit(req.action_id, req.capability_token, req.signature)
    if not success:
        raise HTTPException(status_code=403, detail=msg)
    return {
        "status": "committed",
        "receipt": receipt.model_dump() if receipt else None,
        "message": msg
    }

@router.post("/{action_id}/rollback")
async def rollback_action(action_id: str, reason: str = "user_requested"):
    receipt = coordinator.rollback(action_id, reason)
    if not receipt:
        raise HTTPException(status_code=404, detail="Action not found.")
    return {"status": "rolled_back", "receipt": receipt.model_dump()}
