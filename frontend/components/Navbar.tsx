import Link from "next/link";
import { Radar } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-200 bg-white/80 backdrop-blur dark:border-slate-800 dark:bg-slate-950/80">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-600 text-white">
            <Radar size={18} />
          </span>
          <span>
            FlytBase <span className="text-brand-600">BDR Assistant</span>
          </span>
        </Link>
        <nav className="flex items-center gap-3">
          <Link
            href="/dashboard"
            className="hidden text-sm font-medium text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white sm:inline"
          >
            Dashboard
          </Link>
          <ThemeToggle />
        </nav>
      </div>
    </header>
  );
}
