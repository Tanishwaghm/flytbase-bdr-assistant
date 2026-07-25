"use client";

import { useState } from "react";
import Navbar from "@/components/Navbar";
import EmailInput from "@/components/EmailInput";
import QualificationCard from "@/components/QualificationCard";
import ResearchCard from "@/components/ResearchCard";
import BuyingSignalsCard from "@/components/BuyingSignalsCard";
import CaseStudyCard from "@/components/CaseStudyCard";
import GTMCard from "@/components/GTMCard";
import OutreachCard from "@/components/OutreachCard";
import AEHandoffCard from "@/components/AEHandoffCard";
import { SkeletonCard, CopyButton } from "@/components/ui";
import Toast from "@/components/Toast";
import { analyzeEmail, ApiError } from "@/lib/api";
import type { FullAnalysisResult } from "@/types";
import { History, User2 } from "lucide-react";

interface HistoryEntry {
  id: string;
  companyName: string;
  leadScore: number;
  timestamp: string;
}

export default function DashboardPage() {
  const [emailText, setEmailText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<FullAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryEntry[]>([]);

  async function handleSubmit() {
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeEmail(emailText);
      setResult(data);
      setHistory((prev) => [
        {
          id: crypto.randomUUID(),
          companyName: data.parsed_email.company_name || "Unknown Company",
          leadScore: data.qualification.lead_score,
          timestamp: new Date().toLocaleTimeString(),
        },
        ...prev,
      ].slice(0, 8));
    } catch (e) {
      const msg =
        e instanceof ApiError
          ? `${e.message} (is the backend running and configured with an API key?)`
          : "Something went wrong reaching the backend. Is it running on the configured URL?";
      setError(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen pb-24">
      <Navbar />

      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold">Inbound Lead Dashboard</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Paste an inbound email and let the agent pipeline do the BDR work.
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1fr_280px]">
          <div className="space-y-6">
            <EmailInput value={emailText} onChange={setEmailText} onSubmit={handleSubmit} loading={loading} />

            {result && !loading && (
              <div className="card flex flex-wrap items-center justify-between gap-3 border-brand-200 bg-brand-50/50 dark:border-brand-900 dark:bg-brand-950/20">
                <div className="flex items-center gap-3">
                  <span className="flex h-10 w-10 items-center justify-center rounded-full bg-white text-brand-600 dark:bg-slate-900">
                    <User2 size={18} />
                  </span>
                  <div>
                    <div className="font-semibold">
                      {result.parsed_email.contact_name || "Unknown Contact"} —{" "}
                      {result.parsed_email.company_name || "Unknown Company"}
                    </div>
                    <div className="text-xs text-slate-500 dark:text-slate-400">
                      {result.parsed_email.email || "no email"} · {result.parsed_email.country || "unknown country"} ·
                      Intent: {result.parsed_email.intent} · Urgency: {result.parsed_email.urgency}
                    </div>
                  </div>
                </div>
                <CopyButton text={JSON.stringify(result, null, 2)} label="Copy full JSON" />
              </div>
            )}

            {loading && (
              <div className="grid gap-6">
                <SkeletonCard title="Lead Qualification (MEDDPICC)" />
                <SkeletonCard title="Company Research" />
                <SkeletonCard title="Buying Signals" />
              </div>
            )}

            {!loading && result && (
              <div className="grid gap-6">
                <QualificationCard data={result.qualification} />
                <ResearchCard data={result.research} />
                <BuyingSignalsCard data={result.buying_signals} />
                <CaseStudyCard data={result.case_study} />
                <GTMCard data={result.gtm} />
                <OutreachCard data={result.outreach} />
                <AEHandoffCard data={result.ae_handoff} />
              </div>
            )}

            {!loading && !result && (
              <div className="card flex flex-col items-center justify-center py-16 text-center text-slate-400">
                <p className="text-sm">Paste an inbound email above and click Analyze to see the full pipeline output here.</p>
              </div>
            )}
          </div>

          <aside className="space-y-4">
            <div className="card">
              <h3 className="mb-3 flex items-center gap-2 text-sm font-semibold">
                <History size={15} /> Search History
              </h3>
              {history.length === 0 ? (
                <p className="text-xs text-slate-400">Analyzed leads will appear here.</p>
              ) : (
                <ul className="space-y-2">
                  {history.map((h) => (
                    <li key={h.id} className="rounded-lg bg-slate-50 p-2.5 text-xs dark:bg-slate-800/50">
                      <div className="font-medium">{h.companyName}</div>
                      <div className="text-slate-400">
                        Score {h.leadScore}/100 · {h.timestamp}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </aside>
        </div>
      </div>

      {error && <Toast message={error} onClose={() => setError(null)} />}
    </main>
  );
}
