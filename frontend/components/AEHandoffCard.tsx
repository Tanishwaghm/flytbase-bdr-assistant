import { FileCheck2, Download } from "lucide-react";
import type { AEHandoffSummary } from "@/types";
import { ConfidencePill, CopyButton } from "./ui";

export default function AEHandoffCard({ data }: { data: AEHandoffSummary }) {
  const exportText = `AE HANDOFF SUMMARY
==================
Lead Score: ${data.lead_score}/100
Confidence: ${Math.round(data.confidence_score * 100)}%

Research Summary:
${data.research_summary}

Pain Points:
${data.pain_points.map((p) => `- ${p}`).join("\n")}

Buying Signals:
${data.buying_signals.map((s) => `- ${s}`).join("\n")}

Recommended Demo Focus: ${data.recommended_demo_focus}
Recommended Case Study: ${data.recommended_case_study}
Recommended Owner: ${data.recommended_owner}
Next Action: ${data.next_action}`;

  function downloadTxt() {
    const blob = new Blob([exportText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "ae-handoff-summary.txt";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="card animate-fade-in border-brand-200 dark:border-brand-900">
      <div className="card-header">
        <h3 className="flex items-center gap-2 font-semibold">
          <FileCheck2 size={18} className="text-brand-600" /> AE Handoff Summary
        </h3>
        <div className="flex items-center gap-2">
          <ConfidencePill score={data.confidence_score} />
          <CopyButton text={exportText} label="Copy all" />
          <button onClick={downloadTxt} className="btn-secondary">
            <Download size={13} /> Export
          </button>
        </div>
      </div>

      <div className="mb-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Stat label="Lead Score" value={`${data.lead_score}/100`} />
        <Stat label="Owner" value={data.recommended_owner} />
        <Stat label="Case Study" value={data.recommended_case_study} />
        <Stat label="Next Action" value={data.next_action} />
      </div>

      <p className="mb-4 text-sm text-slate-700 dark:text-slate-300">{data.research_summary}</p>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Pain Points
          </div>
          <ul className="list-inside list-disc space-y-0.5 text-sm text-slate-700 dark:text-slate-300">
            {data.pain_points.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
        <div>
          <div className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
            Buying Signals
          </div>
          <ul className="list-inside list-disc space-y-0.5 text-sm text-slate-700 dark:text-slate-300">
            {data.buying_signals.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="mt-4 rounded-lg bg-brand-50 p-3 text-sm text-brand-800 dark:bg-brand-950/40 dark:text-brand-300">
        <span className="font-semibold">Recommended demo focus: </span>
        {data.recommended_demo_focus}
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg bg-slate-50 p-2.5 dark:bg-slate-800/50">
      <div className="text-[10px] font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
        {label}
      </div>
      <div className="truncate text-sm font-semibold" title={value}>
        {value}
      </div>
    </div>
  );
}
