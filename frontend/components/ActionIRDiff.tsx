import React from "react";
import { Database, FolderTree, CreditCard, GitBranch, Globe } from "lucide-react";

interface ActionIRDiffProps {
  actionId: string;
  domain: string;
  operation: string;
  targetResource: string;
  parameters: Record<string, any>;
  rollbackRecipe?: Record<string, any> | null;
}

export function ActionIRDiff({
  actionId,
  domain,
  operation,
  targetResource,
  parameters,
  rollbackRecipe,
}: ActionIRDiffProps) {
  const getDomainIcon = () => {
    switch (domain) {
      case "database":
        return <Database className="w-4 h-4 text-sky-400" />;
      case "filesystem":
        return <FolderTree className="w-4 h-4 text-emerald-400" />;
      case "payment":
        return <CreditCard className="w-4 h-4 text-purple-400" />;
      case "vcs":
        return <GitBranch className="w-4 h-4 text-amber-400" />;
      default:
        return <Globe className="w-4 h-4 text-slate-400" />;
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          {getDomainIcon()}
          <span className="font-semibold text-slate-200 text-sm capitalize">{domain} Action IR</span>
        </div>
        <span className="text-[11px] font-mono text-slate-500 bg-slate-950 px-2 py-0.5 rounded border border-slate-800">
          ID: {actionId.slice(0, 16)}...
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3 text-xs font-mono">
        <div className="p-2.5 rounded bg-slate-950 border border-slate-800">
          <span className="text-slate-500 block mb-0.5">Operation:</span>
          <span className="text-emerald-400 font-bold uppercase">{operation}</span>
        </div>
        <div className="p-2.5 rounded bg-slate-950 border border-slate-800">
          <span className="text-slate-500 block mb-0.5">Target Resource:</span>
          <span className="text-slate-300 truncate block">{targetResource}</span>
        </div>
      </div>

      <div className="space-y-1.5">
        <span className="text-xs text-slate-400 font-medium">Normalized Parameters:</span>
        <pre className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono text-slate-300 overflow-x-auto">
          {JSON.stringify(parameters, null, 2)}
        </pre>
      </div>

      {rollbackRecipe && (
        <div className="p-3 bg-indigo-950/40 border border-indigo-900/60 rounded-lg text-xs font-mono space-y-1">
          <span className="text-indigo-400 font-semibold block">Compensating Rollback Recipe:</span>
          <pre className="text-indigo-300/80 text-[11px]">
            {JSON.stringify(rollbackRecipe, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
