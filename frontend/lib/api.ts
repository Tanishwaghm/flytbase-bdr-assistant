import type { FullAnalysisResult } from "@/types";

const BASE = "/api";

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const data = await res.json();
      detail = data.detail || detail;
    } catch {
      /* noop */
    }
    throw new ApiError(detail, res.status);
  }
  return res.json();
}

export function analyzeEmail(emailText: string): Promise<FullAnalysisResult> {
  return post<FullAnalysisResult>("/analyze-email", { email_text: emailText });
}

export const SAMPLE_EMAILS: { label: string; text: string }[] = [
  {
    label: "European BVLOS Drone Inspection Co.",
    text: `Hi,

We are a drone inspection company operating across Europe. We are looking for software to automate BVLOS missions and fleet management. We currently run manual flights and it's becoming hard to scale across our 40+ field technicians. We'd like to schedule a demo as soon as possible.

Regards,
John Meier
Head of Operations, AeroScan Inspections GmbH
john.meier@aeroscan-inspections.eu
+49 151 2345 6789`,
  },
  {
    label: "US Utility - Enterprise Inquiry",
    text: `Hello team,

I'm on the innovation team at a regional electric utility in Texas. We're evaluating autonomous drone-in-a-box solutions for transmission line inspection as part of a digital transformation initiative approved by our VP of Operations. Budget has been earmarked for FY25. Can someone reach out to discuss enterprise pricing and a pilot program?

Best,
Sarah Coleman
Innovation Program Manager
sarah.coleman@utilityco-example.com`,
  },
  {
    label: "General / Low-Intent Inquiry",
    text: `hi just saw your website, what does your product do? thanks`,
  },
];
