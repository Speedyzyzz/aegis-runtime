import type { Metadata } from "next";
import React from "react";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Aegis Runtime — Policy & Authorization Layer for Agents",
  description: "Programmable runtime firewall and two-phase commit coordinator with cryptographic audit trail",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen antialiased flex flex-col font-sans">
        <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur px-6 py-4 flex items-center justify-between sticky top-0 z-50">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center font-bold text-white shadow-lg shadow-emerald-500/20">
              AE
            </div>
            <div>
              <span className="font-semibold text-lg tracking-tight text-white">Aegis Runtime</span>
              <span className="ml-2 text-xs px-2 py-0.5 rounded-full bg-emerald-950 border border-emerald-800 text-emerald-300 font-mono">
                2PC Guardrail
              </span>
            </div>
          </div>
          <nav className="flex items-center gap-6 text-sm text-slate-400">
            <Link href="/" className="hover:text-white transition-colors">Transactions</Link>
            <Link href="/approvals" className="hover:text-white transition-colors flex items-center gap-1.5">
              <span>Approval Inbox</span>
              <span className="px-1.5 py-0.2 bg-rose-900 text-rose-300 rounded-full text-[10px] font-bold">1</span>
            </Link>
            <Link href="/audit" className="hover:text-white transition-colors">Merkle Audit Log</Link>
            <span className="text-xs px-2.5 py-1 bg-emerald-950 border border-emerald-800 text-emerald-400 rounded-md font-mono">
              0% Unauthorized
            </span>
          </nav>
        </header>
        <main className="flex-1 p-6 max-w-7xl w-full mx-auto">{children}</main>
      </body>
    </html>
  );
}
