"use client";

import React, { useState } from "react";
import Link from "next/link";
import { ArrowLeft, CheckCircle, XCircle, AlertTriangle } from "lucide-react";
import { BlastRadiusMeter } from "@/components/BlastRadiusMeter";
import { ActionIRDiff } from "@/components/ActionIRDiff";

export default function ApprovalInbox() {
  const [approved, setApproved] = useState(false);
  const [rejected, setRejected] = useState(false);

  const pendingAction = {
    actionId: "act_blake3_4401c900e",
    domain: "payment",
    operation: "charge",
    targetResource: "cust_enterprise_01",
    score: 65.0,
    riskLevel: "high",
    parameters: {
      amount: 450.0,
      currency: "USD",
      customer_id: "cust_enterprise_01",
      description: "Automated agent provisioning charge",
    },
    rollbackRecipe: {
      undo_operation: "refund",
      charge_id: "ch_pending",
    },
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="p-2 bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-lg text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
          </Link>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white">Pending Approval Inbox</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Review high-risk actions requiring explicit cryptographic human approval.
            </p>
          </div>
        </div>
      </div>

      {approved && (
        <div className="p-4 bg-emerald-950/80 border border-emerald-800 rounded-xl text-emerald-300 text-xs font-mono flex items-center gap-2">
          <CheckCircle className="w-4 h-4 text-emerald-400" />
          <span>Action authorized! Capability token issued and 2PC commit executed into Merkle audit trail.</span>
        </div>
      )}

      {rejected && (
        <div className="p-4 bg-rose-950/80 border border-rose-800 rounded-xl text-rose-300 text-xs font-mono flex items-center gap-2">
          <XCircle className="w-4 h-4 text-rose-400" />
          <span>Action rejected. Capability token was withheld and action terminated with 0 side effects.</span>
        </div>
      )}

      {!approved && !rejected && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <ActionIRDiff
              actionId={pendingAction.actionId}
              domain={pendingAction.domain}
              operation={pendingAction.operation}
              targetResource={pendingAction.targetResource}
              parameters={pendingAction.parameters}
              rollbackRecipe={pendingAction.rollbackRecipe}
            />

            <div className="flex items-center gap-4">
              <button
                onClick={() => setApproved(true)}
                className="flex-1 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-sm font-semibold flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/20 transition-all"
              >
                <CheckCircle className="w-4 h-4" />
                <span>Sign & Authorize Execution</span>
              </button>
              <button
                onClick={() => setRejected(true)}
                className="flex-1 py-3 bg-rose-900/60 hover:bg-rose-900 border border-rose-800 text-rose-200 rounded-xl text-sm font-semibold flex items-center justify-center gap-2 transition-all"
              >
                <XCircle className="w-4 h-4" />
                <span>Reject & Abort Action</span>
              </button>
            </div>
          </div>

          <div className="space-y-6">
            <BlastRadiusMeter score={pendingAction.score} riskLevel={pendingAction.riskLevel} />

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3 text-xs">
              <h3 className="font-semibold text-slate-200">Security Guardrail Reason</h3>
              <p className="text-slate-400 leading-relaxed">
                Aegis policy <span className="font-mono text-indigo-400">RULE_REQUIRE_PAYMENT_APPROVAL</span> intercepted this transaction because amount exceeds $250.00. Automatic execution is disabled.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
