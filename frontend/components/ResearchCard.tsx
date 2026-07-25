import { Building2 } from "lucide-react";
import type { CompanyResearch } from "@/types";
import { ConfidencePill, CopyButton } from "./ui";

function Tag({ children }: { children: React.ReactNode }) {
  return (
    <span className="pill bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
      {children}
    </span>
  );
}

function ListBlock({ title, items }: { title: string; items: string[] }) {
  if (items.length === 0) return null;
  return (
    <div>
      <div className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
        {title}
      </div>
      <ul className="list-inside list-disc space-y-0.5 text-sm text-slate-700 dark:text-slate-300">
        {items.map((it, i) => (
          <li key={i}>{it}</li>
        ))}
      </ul>
    </div>
  );
}

export default function ResearchCard({ data }: { data: CompanyResearch }) {
  const exportText = `Company Research\n\n${data.company_description}\n\nProducts: ${data.products.join(
    ", "
  )}\nLocations: ${data.locations.join(", ")}\nFunding: ${data.funding}\nEmployees: ${data.employee_count_estimate}`;

  return (
    <div className="card animate-fade-in">
      <div className="card-header">
        <h3 className="flex items-center gap-2 font-semibold">
          <Building2 size={18} className="text-brand-600" /> Company Research
        </h3>
        <div className="flex items-center gap-2">
          <ConfidencePill score={data.confidence_score} />
          <CopyButton text={exportText} />
        </div>
      </div>

      <p className="mb-4 text-sm text-slate-700 dark:text-slate-300">{data.company_description}</p>

      <div className="mb-4 flex flex-wrap gap-1.5">
        {data.industry && <Tag>{data.industry}</Tag>}
        {data.employee_count_estimate && <Tag>{data.employee_count_estimate} employees</Tag>}
        {data.funding && <Tag>{data.funding}</Tag>}
        {data.locations.map((l, i) => (
          <Tag key={i}>{l}</Tag>
        ))}
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <ListBlock title="Products" items={data.products} />
        <ListBlock title="Tech Stack" items={data.technology_stack} />
        <ListBlock title="Recent News" items={data.recent_news} />
        <ListBlock title="Hiring Signals" items={data.hiring_signals} />
        <ListBlock title="Growth Signals" items={data.growth_signals} />
        <ListBlock title="Competitors" items={data.competitors} />
      </div>

      {data.sources.length > 0 && (
        <div className="mt-4 border-t border-slate-100 pt-3 text-xs text-slate-400 dark:border-slate-800">
          Sources: {data.sources.length} web result{data.sources.length !== 1 ? "s" : ""} referenced
        </div>
      )}
    </div>
  );
}
