"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";
import clsx from "clsx";

export function CopyButton({ text, label = "Copy" }: { text: string; label?: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      className="btn-secondary"
      onClick={async () => {
        await navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 1500);
      }}
    >
      {copied ? <Check size={13} /> : <Copy size={13} />}
      {copied ? "Copied" : label}
    </button>
  );
}

export function ConfidencePill({ score }: { score: number }) {
  const pct = Math.round(score * 100);
  const tone =
    pct >= 70
      ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300"
      : pct >= 40
      ? "bg-amber-50 text-amber-700 dark:bg-amber-950 dark:text-amber-300"
      : "bg-rose-50 text-rose-700 dark:bg-rose-950 dark:text-rose-300";
  return <span className={clsx("pill", tone)}>Confidence {pct}%</span>;
}

export function ScoreGauge({ score, label }: { score: number; label: string }) {
  const circumference = 2 * Math.PI * 42;
  const offset = circumference - (score / 100) * circumference;
  const color = score >= 70 ? "#10b981" : score >= 40 ? "#f59e0b" : "#f43f5e";
  return (
    <div className="flex flex-col items-center">
      <svg width="110" height="110" viewBox="0 0 110 110" className="-rotate-90">
        <circle cx="55" cy="55" r="42" fill="none" stroke="currentColor" strokeWidth="10" className="text-slate-100 dark:text-slate-800" />
        <circle
          cx="55"
          cy="55"
          r="42"
          fill="none"
          stroke={color}
          strokeWidth="10"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-700 ease-out"
        />
      </svg>
      <div className="-mt-16 text-2xl font-bold">{score}</div>
      <div className="mt-16 text-xs text-slate-500 dark:text-slate-400">{label}</div>
    </div>
  );
}

export function SkeletonCard({ title }: { title: string }) {
  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <h3 className="font-semibold">{title}</h3>
        <div className="skeleton h-5 w-16" />
      </div>
      <div className="space-y-2">
        <div className="skeleton h-4 w-full" />
        <div className="skeleton h-4 w-5/6" />
        <div className="skeleton h-4 w-3/4" />
        <div className="skeleton h-4 w-2/3" />
      </div>
    </div>
  );
}

export function StrengthPill({ strength }: { strength: string }) {
  const tone =
    strength === "strong"
      ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300"
      : strength === "moderate"
      ? "bg-amber-50 text-amber-700 dark:bg-amber-950 dark:text-amber-300"
      : "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400";
  return <span className={clsx("pill", tone)}>{strength}</span>;
}
