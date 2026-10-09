import React from "react";
import Link from "next/link";
import { ArrowLeft, ShieldCheck, Database } from "lucide-react";
import { MerkleProofTree } from "@/components/MerkleProofTree";

export default function MerkleAuditPage() {
  const receipts = [
    {
      receipt_id: "rcpt_9f1a208c11",
      action_id: "act_blake3_9182a",
      previous_receipt_hash: "0000000000000000000000000000000000000000000000000000000000000000",
      merkle_root_hash: "7e81b2a991820d8f33190abce992",
      status: "committed",
      committed_at_epoch: Date.now() - 120000,
    },
    {
      receipt_id: "rcpt_3b71e04a99",
      action_id: "act_blake3_7712b",
      previous_receipt_hash: "7e81b2a991820d8f33190abce992",
      merkle_root_hash: "4a189fec0018d998231abf9911e3",
      status: "committed",
      committed_at_epoch: Date.now() - 480000,
    },
    {
      receipt_id: "rcpt_aa184f091c",
      action_id: "act_blake3_roll_01",
      previous_receipt_hash: "4a189fec0018d998231abf9911e3",
      merkle_root_hash: "11e98bbcf9912a77192cae00182b",
      status: "rolled_back",
      committed_at_epoch: Date.now() - 900000,
    },
  ];

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
            <h1 className="text-xl font-bold tracking-tight text-white">Immutable Merkle Audit Log</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Cryptographically verified append-only receipt chain powered by BLAKE3 hashes.
            </p>
          </div>
        </div>
      </div>

      <MerkleProofTree receipts={receipts} isValid={true} />
    </div>
  );
}
