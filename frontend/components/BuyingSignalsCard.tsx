import { TrendingUp, CheckCircle2, XCircle } from "lucide-react";
import type { BuyingSignalResult } from "@/types";
import { StrengthPill, ScoreGauge } from "./ui";

const SIGNAL_LABELS: Record<string, string> = {
  expansion: "Expansion",
  hiring: "Hiring",
  funding: "Funding",
  digital_transformation: "Digital Transformation",
  drone_adoption: "Drone Adoption",
  enterprise_readiness: "Enterprise Readiness",
  buying_intent: "Buying Intent",
};

export default function BuyingSignalsCard({ data }: { data: BuyingSignalResult }) {
  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <h3 className="flex items-center gap-2 font-semibold">
          <TrendingUp size={18} className="text-brand-600" /> Buying Signals
        </h3>
      </div>

      <div className="grid gap-6 sm:grid-cols-[110px_1fr]">
        <ScoreGauge score={data.overall_buying_intent_score} label="Buying Intent" />
        <div className="space-y-2">
          {data.signals.map((s) => (
            <div
              key={s.signal_type}
              className="flex items-start gap-2.5 rounded-lg bg-slate-50 p-3 text-sm dark:bg-slate-800/50"
            >
              {s.detected ? (
                <CheckCircle2 size={16} className="mt-0.5 shrink-0 text-emerald-500" />
              ) : (
                <XCircle size={16} className="mt-0.5 shrink-0 text-slate-300 dark:text-slate-600" />
              )}
              <div className="flex-1">
                <div className="mb-0.5 flex items-center gap-2">
                  <span className="font-medium">{SIGNAL_LABELS[s.signal_type] || s.signal_type}</span>
                  {s.detected && <StrengthPill strength={s.strength} />}
                </div>
                <p className="text-slate-600 dark:text-slate-400">{s.explanation}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
