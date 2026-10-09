import React from "react";
import { AlertTriangle, ShieldCheck, ShieldAlert } from "lucide-react";

interface BlastRadiusMeterProps {
  score: number; // 0.0 to 100.0
  riskLevel: string;
}

export function BlastRadiusMeter({ score, riskLevel }: BlastRadiusMeterProps) {
  const getBadgeStyle = () => {
    if (score >= 75) return "bg-rose-950/80 border-rose-800 text-rose-400";
    if (score >= 35) return "bg-amber-950/80 border-amber-800 text-amber-400";
    return "bg-emerald-950/80 border-emerald-800 text-emerald-400";
  };

  const getBarColor = () => {
    if (score >= 75) return "bg-rose-500";
    if (score >= 35) return "bg-amber-500";
    return "bg-emerald-500";
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <span className="text-xs text-slate-400 font-medium flex items-center gap-1.5">
          {score >= 75 ? (
            <ShieldAlert className="w-4 h-4 text-rose-400" />
          ) : (
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          )}
          <span>Blast Radius Impact Score</span>
        </span>
        <span className={`text-xs px-2 py-0.5 rounded-full font-mono font-bold uppercase border ${getBadgeStyle()}`}>
          {riskLevel} ({score.toFixed(1)}/100)
        </span>
      </div>

      <div className="w-full bg-slate-950 h-2.5 rounded-full overflow-hidden border border-slate-800">
        <div
          className={`h-full transition-all duration-500 ${getBarColor()}`}
          style={{ width: `${Math.min(100, Math.max(5, score))}%` }}
        />
      </div>

      <div className="flex justify-between text-[10px] text-slate-500 font-mono">
        <span>0 (Read-Only)</span>
        <span>30 (Auto-Approve Threshold)</span>
        <span>100 (Critical Destructive)</span>
      </div>
    </div>
  );
}
