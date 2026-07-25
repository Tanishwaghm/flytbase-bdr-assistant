import { ClipboardCheck } from "lucide-react";
import type { QualificationResult } from "@/types";
import { ConfidencePill, ScoreGauge, CopyButton } from "./ui";

const MEDDPICC_LABELS: Record<string, string> = {
  metrics: "Metrics",
  economic_buyer: "Economic Buyer",
  decision_criteria: "Decision Criteria",
  decision_process: "Decision Process",
  paper_process: "Paper Process",
  pain: "Pain",
  champion: "Champion",
  competition: "Competition",
};

export default function QualificationCard({ data }: { data: QualificationResult }) {
  const exportText = `MEDDPICC Qualification\nLead Score: ${data.lead_score}/100\n\n${Object.entries(
    data.meddpicc
  )
    .map(([k, v]) => `${MEDDPICC_LABELS[k]}: ${v}`)
    .join("\n")}\n\nMissing: ${data.missing_information.join(", ")}\n\nReasoning: ${data.reasoning}`;

  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <h3 className="flex items-center gap-2 font-semibold">
          <ClipboardCheck size={18} className="text-brand-600" /> Lead Qualification (MEDDPICC)
        </h3>
        <div className="flex items-center gap-2">
          <ConfidencePill score={data.confidence_score} />
          <CopyButton text={exportText} />
        </div>
      </div>

      <div className="grid gap-6 sm:grid-cols-[110px_1fr]">
        <ScoreGauge score={data.lead_score} label="Lead Score" />
        <div className="grid gap-3 sm:grid-cols-2">
          {Object.entries(data.meddpicc).map(([key, value]) => (
            <div key={key} className="rounded-lg bg-slate-50 p-3 text-sm dark:bg-slate-800/50">
              <div className="mb-0.5 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                {MEDDPICC_LABELS[key]}
              </div>
              <div className="text-slate-700 dark:text-slate-300">{value}</div>
            </div>
          ))}
        </div>
      </div>

      {data.missing_information.length > 0 && (
        <div className="mt-4">
          <div className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Discovery Call Must-Cover
          </div>
          <div className="flex flex-wrap gap-1.5">
            {data.missing_information.map((m, i) => (
              <span key={i} className="pill bg-brand-50 text-brand-700 dark:bg-brand-950 dark:text-brand-300">
                {m}
              </span>
            ))}
          </div>
        </div>
      )}

      <p className="mt-4 text-sm text-slate-600 dark:text-slate-400">{data.reasoning}</p>
    </div>
  );
}
