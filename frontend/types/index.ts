export interface ParsedEmail {
  company_name: string | null;
  contact_name: string | null;
  email: string | null;
  phone: string | null;
  country: string | null;
  industry: string | null;
  intent: string;
  urgency: "low" | "medium" | "high" | "critical";
  pain_points: string[];
  raw_text: string;
  confidence_score: number;
}

export interface MeddpiccBreakdown {
  metrics: string;
  economic_buyer: string;
  decision_criteria: string;
  decision_process: string;
  paper_process: string;
  pain: string;
  champion: string;
  competition: string;
}

export interface QualificationResult {
  meddpicc: MeddpiccBreakdown;
  lead_score: number;
  confidence_score: number;
  missing_information: string[];
  reasoning: string;
}

export interface CompanyResearch {
  company_description: string;
  products: string[];
  industry: string;
  employee_count_estimate: string;
  locations: string[];
  funding: string;
  recent_news: string[];
  hiring_signals: string[];
  technology_stack: string[];
  growth_signals: string[];
  competitors: string[];
  website_summary: string;
  linkedin_summary: string;
  confidence_score: number;
  sources: string[];
}

export interface BuyingSignal {
  signal_type: string;
  detected: boolean;
  explanation: string;
  strength: "weak" | "moderate" | "strong";
}

export interface BuyingSignalResult {
  signals: BuyingSignal[];
  overall_buying_intent_score: number;
}

export interface CaseStudyMatch {
  case_study_id: string;
  title: string;
  industry: string;
  similarity_score: number;
  reasoning: string;
}

export interface CaseStudyResult {
  top_matches: CaseStudyMatch[];
  recommended_case_study: CaseStudyMatch;
}

export interface GTMRecommendation {
  motion: "direct_ae" | "partner_led" | "enterprise_team" | "channel_partner";
  reasoning: string;
  confidence_score: number;
  suggested_owner_type: string;
}

export interface OutreachPackage {
  personalized_email_subject: string;
  personalized_email_body: string;
  linkedin_message: string;
  call_opening: string;
  discovery_questions: string[];
  follow_up_1: string;
  follow_up_2: string;
}

export interface AEHandoffSummary {
  lead_score: number;
  research_summary: string;
  pain_points: string[];
  buying_signals: string[];
  recommended_demo_focus: string;
  recommended_case_study: string;
  recommended_owner: string;
  next_action: string;
  confidence_score: number;
}

export interface FullAnalysisResult {
  parsed_email: ParsedEmail;
  qualification: QualificationResult;
  research: CompanyResearch;
  buying_signals: BuyingSignalResult;
  case_study: CaseStudyResult;
  gtm: GTMRecommendation;
  outreach: OutreachPackage;
  ae_handoff: AEHandoffSummary;
}
