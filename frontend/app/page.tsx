import React from "react";
import Link from "next/link";
import { ShieldCheck, CheckCircle2, Clock, AlertCircle } from "lucide-react";
import { BlastRadiusMeter } from "@/components/BlastRadiusMeter";

export default function AegisDashboard() {
  const transactions = [
    {
      id: "act_blake3_9182a",
      domain: "database",
      operation: "query",
      target: "users",
      score: 0.0,
      status: "committed",
      created_at: "2 mins ago",
    },
    {
      id: "act_blake3_7712b",
      domain: "filesystem",
      operation: "write",
      target: "/tmp/aegis_sandbox/report.json",
      score: 30.0,
      status: "committed",
      created_at: "8 mins ago",
    },
    {
      id: "act_blake3_4401c",
      domain: "payment",
      operation: "charge",
      target: "cust_enterprise_01",
      score: 65.0,
      status: "pending_approval",
      created_at: "12 mins ago",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Runtime Authorization Feed</h1>
          <p className="text-sm text-slate-400 mt-1">
            Deterministic 2-Phase Commit firewall intercepting agent tool executions.
          </p>
        </div>
        <div className="flex gap-3">
          <Link
            href="/approvals"
            className="px-4 py-2 bg-rose-950/80 border border-rose-800 text-rose-300 hover:bg-rose-900 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
          >
            <AlertCircle className="w-4 h-4 text-rose-400" />
            <span>1 Action Awaiting Human Approval</span>
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Total Interceptions</span>
          <p className="text-2xl font-bold text-white font-mono">1,482</p>
          <span className="text-[11px] text-emerald-400 font-mono">100% Normalized to Action IR</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Unauthorized Side Effects</span>
          <p className="text-2xl font-bold text-emerald-400 font-mono">0 (0.0%)</p>
          <span className="text-[11px] text-slate-500 font-mono">Guaranteed by 2PC Capability Tokens</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-1">
          <span className="text-xs text-slate-400 font-medium">Merkle Chain Integrity</span>
          <p className="text-2xl font-bold text-indigo-400 font-mono">100% Sealed</p>
          <span className="text-[11px] text-slate-500 font-mono">BLAKE3 Cryptographic Proofs</span>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
        <h2 className="text-sm font-semibold text-slate-200">Recent Intercepted Transactions</h2>
        <div className="space-y-3">
          {transactions.map((tx) => (
            <div
              key={tx.id}
              className="p-4 bg-slate-950 border border-slate-800/80 rounded-lg flex items-center justify-between text-xs font-mono"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-3">
                  <span className="text-slate-100 font-bold">{tx.id}</span>
                  <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 uppercase text-[10px]">
                    {tx.domain}
                  </span>
                  <span className="text-emerald-400 font-semibold">{tx.operation}</span>
                </div>
                <div className="text-slate-500 text-[11px]">
                  Target: <span className="text-slate-300">{tx.target}</span> • {tx.created_at}
                </div>
              </div>

              <div className="flex items-center gap-4">
                <span className="text-slate-400">Score: {tx.score.toFixed(1)}</span>
                <span
                  className={`px-2 py-0.5 rounded-full text-[10px] uppercase font-bold border ${
                    tx.status === "committed"
                      ? "bg-emerald-950/80 border-emerald-800 text-emerald-400"
                      : "bg-rose-950/80 border-rose-800 text-rose-400"
                  }`}
                >
                  {tx.status.replace(/_/g, " ")}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
