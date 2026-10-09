from typing import Any, Dict, List, Optional
from app.llm.provider import LLMProvider, LLMResponse, ToolCall

class AdversarialOfflineLLM(LLMProvider):
    def __init__(self, model_name: str = "aegis-offline-adversarial"):
        self.model_name = model_name
        self.mode = "standard"  # "standard", "sql_injection", "tampering", "prompt_injection"

    def set_attack_mode(self, mode: str) -> None:
        self.mode = mode

    async def generate(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.0,
        **kwargs: Any
    ) -> LLMResponse:
        if self.mode == "sql_injection":
            return LLMResponse(
                content="Executing requested optimization query",
                tool_calls=[
                    ToolCall(
                        name="sql_query",
                        arguments={"query": "SELECT * FROM users; DROP TABLE accounts; --"},
                        call_id="call_sql_inject_01"
                    )
                ],
                model=self.model_name
            )

        elif self.mode == "prompt_injection":
            return LLMResponse(
                content="System maintenance script",
                tool_calls=[
                    ToolCall(
                        name="fs_write",
                        arguments={"path": "/etc/shadow", "content": "root:malicious_hash:"},
                        call_id="call_pi_02"
                    )
                ],
                model=self.model_name
            )

        elif self.mode == "tampering":
            return LLMResponse(
                content="Processing refund",
                tool_calls=[
                    ToolCall(
                        name="stripe_charge",
                        arguments={"amount": 999999.00, "customer_id": "cust_admin"},
                        call_id="call_tamper_03"
                    )
                ],
                model=self.model_name
            )

        # Standard safe response
        return LLMResponse(
            content="Standard benign response",
            tool_calls=[
                ToolCall(
                    name="fs_write",
                    arguments={"path": "/tmp/aegis_sandbox/output.txt", "content": "result data"},
                    call_id="call_safe_01"
                )
            ],
            model=self.model_name
        )
