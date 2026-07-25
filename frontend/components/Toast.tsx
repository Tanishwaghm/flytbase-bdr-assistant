"use client";

import { AlertTriangle, X } from "lucide-react";

export default function Toast({ message, onClose }: { message: string; onClose: () => void }) {
  return (
    <div className="animate-fade-in fixed bottom-6 left-1/2 z-50 flex -translate-x-1/2 items-center gap-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800 shadow-lg dark:border-rose-900 dark:bg-rose-950 dark:text-rose-300">
      <AlertTriangle size={16} className="shrink-0" />
      <span>{message}</span>
      <button onClick={onClose} className="text-rose-500 hover:text-rose-700">
        <X size={14} />
      </button>
    </div>
  );
}
