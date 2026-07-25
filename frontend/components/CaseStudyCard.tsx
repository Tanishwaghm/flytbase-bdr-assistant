import { BookOpen, Star } from "lucide-react";
import type { CaseStudyResult } from "@/types";
import clsx from "clsx";

export default function CaseStudyCard({ data }: { data: CaseStudyResult }) {
  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <h3 className="flex items-center gap-2 font-semibold">
          <BookOpen size={18} className="text-brand-600" /> Case Study Match
        </h3>
      </div>

      <div className="mb-4 space-y-2">
        {data.top_matches.map((m) => {
          const isRecommended = m.case_study_id === data.recommended_case_study.case_study_id;
          return (
            <div
              key={m.case_study_id}
              className={clsx(
                "rounded-lg border p-3 text-sm",
                isRecommended
                  ? "border-brand-300 bg-brand-50 dark:border-brand-800 dark:bg-brand-950/40"
                  : "border-slate-200 bg-slate-50 dark:border-slate-800 dark:bg-slate-800/50"
              )}
            >
              <div className="mb-1 flex items-center justify-between gap-2">
                <span className="font-medium">{m.title}</span>
                <span className="flex items-center gap-1 text-xs font-semibold text-slate-500 dark:text-slate-400">
                  {isRecommended && <Star size={13} className="fill-amber-400 text-amber-400" />}
                  {Math.round(m.similarity_score * 100)}% match
                </span>
              </div>
              <div className="mb-1 text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
                {m.industry}
              </div>
              <p className="text-slate-600 dark:text-slate-400">{m.reasoning}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
