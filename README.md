# Aegis Runtime: Policy-Enforcing Transaction Layer & Runtime Authorization Guardrail

A programmable runtime firewall and two-phase commit protocol that intercepts agent tool calls, normalizes them into a typed `Action IR`, simulates blast radius, enforces deterministic policy predicates, and records immutable Merkle-backed audit receipts before execution.

## Architecture

- **`backend/app/ir/`**: Typed `Action IR` normalizer converting raw tool calls into canonical representations with quantitative blast radius calculation (0-100 score).
- **`backend/app/policy/`**: Deterministic policy evaluation engine with single-action scoped capability tokens (TTL-based attenuation, TOCTOU prevention).
- **`backend/app/coordinator/`**: Two-phase commit coordinator ensuring 0 duplicate side effects and append-only BLAKE3 Merkle-linked audit receipts.
- **`backend/app/llm/`**: Dual-Engine LLM architecture with adversarial attack mode.
- **`frontend/`**: Next.js 15 App Router human-in-the-loop approval inbox, blast radius meter, and cryptographic audit explorer.
- **`benchmark/`**: `AegisBench` 100+ adversarial tasks asserting 0% unauthorized side effects and 0 duplicate actions.

## Quick Start (Offline Verification)

```bash
# 1. Run all unit & integration tests (100% offline)
pytest backend/tests -v

# 2. Run the 100-task AegisBench suite
python3 benchmark/aegis_bench.py
```

## Running Full Stack

```bash
# Start backend API (FastAPI)
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8001

# Start frontend (Next.js 15)
cd frontend && npm install && npm run dev
```
