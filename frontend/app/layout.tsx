import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FlytBase Inbound BDR Assistant",
  description: "AI-powered agent pipeline that automates inbound lead qualification, research, and outreach for FlytBase.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
