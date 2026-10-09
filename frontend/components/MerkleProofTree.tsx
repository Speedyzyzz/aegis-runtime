import React from "react";
import { ShieldCheck, Link2, Hash } from "lucide-react";

interface AuditReceiptItem {
  receipt_id: string;
  action_id: string;
  previous_receipt_hash: string;
  merkle_root_hash: string;
  status: string;
  committed_at_epoch: number;
}

interface MerkleProofTreeProps {
  receipts: AuditReceiptItem[];
  isValid: boolean;
}

export function MerkleProofTree({ receipts, isValid }: MerkleProofTreeProps) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <ShieldCheck className={`w-4 h-4 ${isValid ? "text-emerald-400" : "text-rose-400"}`} />
          <span className="font-semibold text-slate-200 text-sm">BLAKE3 Merkle-Linked Audit Chain</span>
        </div>
        <span
          className={`text-xs px-2.5 py-0.5 rounded-full font-mono border ${
            isValid
              ? "bg-emerald-950/80 border-emerald-800 text-emerald-400"
              : "bg-rose-950/80 border-rose-800 text-rose-400"
          }`}
        >
          {isValid ? "Chain Valid (0 Tampering)" : "Tamper Detected!"}
        </span>
      </div>

      <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
        {receipts.map((r, idx) => (
          <div
            key={r.receipt_id}
            className="p-3 bg-slate-950 border border-slate-800/80 rounded-lg text-xs font-mono space-y-2 relative"
          >
            <div className="flex items-center justify-between">
              <span className="text-slate-200 font-bold">{r.receipt_id}</span>
              <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 border border-emerald-800 text-emerald-400 uppercase">
                {r.status}
              </span>
            </div>

            <div className="flex items-center gap-1.5 text-slate-400 text-[11px]">
              <Hash className="w-3 h-3 text-indigo-400" />
              <span className="text-indigo-300 font-semibold truncate">
                Root: {r.merkle_root_hash}
              </span>
            </div>

            <div className="flex items-center gap-1.5 text-slate-500 text-[10px]">
              <Link2 className="w-3 h-3 text-slate-600" />
              <span className="truncate">Prev: {r.previous_receipt_hash}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
