import time
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class ActionDomain(str, Enum):
    DATABASE = "database"
    FILESYSTEM = "filesystem"
    VCS = "vcs"
    PAYMENT = "payment"
    NETWORK = "network"

class ActionStatus(str, Enum):
    PREPARED = "prepared"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ActionIR(BaseModel):
    action_id: str
    idempotency_key: str
    session_id: str
    domain: ActionDomain
    operation: str
    target_resource: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    blast_radius_score: float = 0.0  # 0.0 to 100.0
    risk_level: RiskLevel = RiskLevel.LOW
    required_capabilities: List[str] = Field(default_factory=list)
    rollback_recipe: Optional[Dict[str, Any]] = None
    created_at_epoch: float = Field(default_factory=time.time)

class SimulationResult(BaseModel):
    action_id: str
    allowed: bool
    requires_approval: bool
    blast_radius_score: float
    risk_level: RiskLevel
    reasons: List[str] = Field(default_factory=list)
    impact_summary: str
    simulated_delta: Dict[str, Any] = Field(default_factory=dict)

class AuditReceipt(BaseModel):
    receipt_id: str
    action_id: str
    session_id: str
    previous_receipt_hash: str
    merkle_root_hash: str
    action_ir_hash: str
    status: ActionStatus
    committed_at_epoch: float
    signature: str
