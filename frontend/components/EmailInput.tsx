"use client";

import { Sparkles, Loader2 } from "lucide-react";
import { SAMPLE_EMAILS } from "@/lib/api";

interface Props {
  value: string;
  onChange: (v: string) => void;
  onSubmit: () => void;
  loading: boolean;
}

export default function EmailInput({ value, onChange, onSubmit, loading }: Props) {
  return (
    <div className="card">
      <div className="card-header">
        <h3 className="font-semibold">Inbound Contact-Form Email</h3>
        <span className="text-xs text-slate-400">{value.length} chars</span>
      </div>

      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={8}
        placeholder={`Hi,\n\nWe are a drone inspection company operating across Europe...`}
        className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm text-slate-800 outline-none transition focus:border-brand-400 focus:ring-2 focus:ring-brand-100 dark:border-slate-700 dark:bg-slate-800/50 dark:text-slate-200 dark:focus:ring-brand-900"
      />

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <span className="text-xs text-slate-500 dark:text-slate-400">Try:</span>
        {SAMPLE_EMAILS.map((s) => (
          <button key={s.label} onClick={() => onChange(s.text)} className="btn-secondary">
            {s.label}
          </button>
        ))}
      </div>

      <button
        onClick={onSubmit}
        disabled={loading || value.trim().length < 10}
        className="btn-primary mt-4 w-full justify-center"
      >
        {loading ? (
          <>
            <Loader2 size={16} className="animate-spin" /> Running 8-agent pipeline...
          </>
        ) : (
          <>
            <Sparkles size={16} /> Analyze Inbound Lead
          </>
        )}
      </button>
    </div>
  );
}
