import Link from "next/link";
import { ArrowRight, Bot, Search, Target, Send, Workflow } from "lucide-react";
import Navbar from "@/components/Navbar";

const FEATURES = [
  { icon: Bot, title: "8 Specialized AI Agents", desc: "Parsing, qualification, research, signals, case-study matching, GTM, outreach, and AE handoff - each a focused, swappable module." },
  { icon: Search, title: "Grounded Research", desc: "Live web search feeds the Company Research Agent so profiles are based on real public data, not hallucination." },
  { icon: Target, title: "MEDDPICC Qualification", desc: "Every lead is scored against the full MEDDPICC framework with honest gaps flagged for discovery calls." },
  { icon: Workflow, title: "Real GTM Routing", desc: "Direct AE, Enterprise Team, Partner-led, or Channel Partner - recommended with explicit reasoning." },
  { icon: Send, title: "Ready-to-Send Outreach", desc: "Personalized email, LinkedIn message, call opening, discovery questions, and two follow-ups - generated in seconds." },
];

export default function LandingPage() {
  return (
    <main>
      <Navbar />

      <section className="mx-auto max-w-5xl px-4 pb-16 pt-20 text-center sm:px-6">
        <span className="pill mx-auto mb-6 border border-brand-200 bg-brand-50 text-brand-700 dark:border-brand-900 dark:bg-brand-950 dark:text-brand-300">
          FlytBase Inbound BDR Hiring Hackathon
        </span>
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
          Turn one inbound email into a
          <span className="text-brand-600"> fully-worked lead</span>
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-600 dark:text-slate-400">
          Paste a contact-form email. An 8-agent AI pipeline parses it, qualifies it with
          MEDDPICC, researches the company live, matches the best FlytBase case study,
          recommends a GTM motion, and drafts every outreach message an SDR needs -
          in under a minute.
        </p>
        <div className="mt-10 flex items-center justify-center gap-4">
          <Link href="/dashboard" className="btn-primary">
            Try the Dashboard <ArrowRight size={16} />
          </Link>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 pb-24 sm:px-6">
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <div key={f.title} className="card">
              <span className="mb-4 flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-600 dark:bg-brand-950 dark:text-brand-400">
                <f.icon size={20} />
              </span>
              <h3 className="mb-1 font-semibold">{f.title}</h3>
              <p className="text-sm text-slate-600 dark:text-slate-400">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="border-t border-slate-200 py-8 text-center text-sm text-slate-500 dark:border-slate-800">
        Built for the FlytBase Inbound BDR Hiring Hackathon.
      </footer>
    </main>
  );
}
