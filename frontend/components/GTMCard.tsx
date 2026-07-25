import { Route } from "lucide-react";
import type { GTMRecommendation } from "@/types";
import { ConfidencePill } from "./ui";

const MOTION_LABELS: Record<string, string> = {
  direct_ae: "Direct AE",
  partner_led: "Partner-Led",
  enterprise_team: "Enterprise Team",
  channel_partner: "Channel Partner",
};

export default function GTMCard({ data }: { data: GTMRecommendation }) {
  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <h3 className="flex items-center gap-2 font-semibold">
          <Route size={18} className="text-brand-600" /> GTM Recommendation
        </h3>
        <ConfidencePill score={data.confidence_score} />
      </div>

      <div className="mb-3 flex items-center gap-3">
        <span className="rounded-xl bg-brand-600 px-3 py-1.5 text-sm font-semibold text-white">
          {MOTION_LABELS[data.motion] || data.motion}
        </span>
        <span className="text-sm text-slate-500 dark:text-slate-400">{data.suggested_owner_type}</span>
      </div>

      <p className="text-sm text-slate-700 dark:text-slate-300">{data.reasoning}</p>
    </div>
  );
}
