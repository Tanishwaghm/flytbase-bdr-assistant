"use client";

import { useState } from "react";
import { Send, Mail, Linkedin, Phone, HelpCircle } from "lucide-react";
import type { OutreachPackage } from "@/types";
import { CopyButton } from "./ui";
import clsx from "clsx";

const TABS = ["Email", "LinkedIn", "Call", "Follow-ups"] as const;

export default function OutreachCard({ data }: { data: OutreachPackage }) {
  const [tab, setTab] = useState<(typeof TABS)[number]>("Email");

  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <h3 className="flex items-center gap-2 font-semibold">
          <Send size={18} className="text-brand-600" /> Outreach
        </h3>
      </div>

      <div className="mb-4 flex gap-1 rounded-lg bg-slate-100 p-1 dark:bg-slate-800">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={clsx(
              "flex-1 rounded-md px-2 py-1.5 text-xs font-medium transition",
              tab === t
                ? "bg-white text-slate-900 shadow-sm dark:bg-slate-700 dark:text-white"
                : "text-slate-500 hover:text-slate-800 dark:text-slate-400"
            )}
          >
            {t}
          </button>
        ))}
      </div>

      {tab === "Email" && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              <Mail size={13} /> Subject
            </span>
            <CopyButton text={data.personalized_email_subject} label="Copy subject" />
          </div>
          <p className="rounded-lg bg-slate-50 p-2.5 text-sm font-medium dark:bg-slate-800/50">
            {data.personalized_email_subject}
          </p>
          <div className="flex items-center justify-between pt-1">
            <span className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              Body
            </span>
            <CopyButton text={data.personalized_email_body} label="Copy body" />
          </div>
          <p className="whitespace-pre-line rounded-lg bg-slate-50 p-3 text-sm text-slate-700 dark:bg-slate-800/50 dark:text-slate-300">
            {data.personalized_email_body}
          </p>
        </div>
      )}

      {tab === "LinkedIn" && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              <Linkedin size={13} /> Connection Message
            </span>
            <CopyButton text={data.linkedin_message} />
          </div>
          <p className="rounded-lg bg-slate-50 p-3 text-sm text-slate-700 dark:bg-slate-800/50 dark:text-slate-300">
            {data.linkedin_message}
          </p>
        </div>
      )}

      {tab === "Call" && (
        <div className="space-y-4">
          <div>
            <div className="mb-1 flex items-center justify-between">
              <span className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                <Phone size={13} /> Call Opening
              </span>
              <CopyButton text={data.call_opening} />
            </div>
            <p className="rounded-lg bg-slate-50 p-3 text-sm text-slate-700 dark:bg-slate-800/50 dark:text-slate-300">
              {data.call_opening}
            </p>
          </div>
          <div>
            <span className="mb-1 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
              <HelpCircle size={13} /> Discovery Questions
            </span>
            <ol className="list-inside list-decimal space-y-1 rounded-lg bg-slate-50 p-3 text-sm text-slate-700 dark:bg-slate-800/50 dark:text-slate-300">
              {data.discovery_questions.map((q, i) => (
                <li key={i}>{q}</li>
              ))}
            </ol>
          </div>
        </div>
      )}

      {tab === "Follow-ups" && (
        <div className="space-y-3">
          <div>
            <div className="mb-1 flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Follow-up 1 (Day 3)
              </span>
              <CopyButton text={data.follow_up_1} />
            </div>
            <p className="rounded-lg bg-slate-50 p-3 text-sm text-slate-700 dark:bg-slate-800/50 dark:text-slate-300">
              {data.follow_up_1}
            </p>
          </div>
          <div>
            <div className="mb-1 flex items-center justify-between">
              <span className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                Follow-up 2 (Day 7)
              </span>
              <CopyButton text={data.follow_up_2} />
            </div>
            <p className="rounded-lg bg-slate-50 p-3 text-sm text-slate-700 dark:bg-slate-800/50 dark:text-slate-300">
              {data.follow_up_2}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
