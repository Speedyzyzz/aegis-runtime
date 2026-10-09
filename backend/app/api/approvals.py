from typing import List
from fastapi import APIRouter, HTTPException
from app.api.actions import coordinator
from app.ir.schemas import ActionStatus

router = APIRouter(prefix="/approvals", tags=["Approvals"])

@router.get("/pending")
async def list_pending_approvals():
    pending = []
    for action_id, status in coordinator.action_statuses.items():
        if status == ActionStatus.PENDING_APPROVAL:
            action = coordinator.prepared_actions.get(action_id)
            if action:
                pending.append(action.model_dump())
    return pending

@router.post("/{action_id}/approve")
async def approve_action(action_id: str, approver_signature: str = "sig_admin"):
    token = coordinator.approve_human(action_id, approver_signature)
    if not token:
        raise HTTPException(status_code=400, detail="Action not pending approval or not found.")
    return {"status": "approved", "capability_token": token}

@router.post("/{action_id}/reject")
async def reject_action(action_id: str):
    if action_id in coordinator.action_statuses:
        coordinator.action_statuses[action_id] = ActionStatus.REJECTED
        return {"status": "rejected"}
    raise HTTPException(status_code=404, detail="Action not found.")
