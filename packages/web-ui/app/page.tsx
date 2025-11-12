import Link from "next/link";
import TerminalPreview from "../components/TerminalPreview";
import SummaryCards from "../components/SummaryCards";

export default function HomePage() {
  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-12">
      <section className="grid gap-8 lg:grid-cols-2">
        <div className="glass-panel rounded-3xl p-8">
          <p className="text-sm uppercase tracking-[0.4em] text-brand-200">Personal AI Command Center</p>
          <h1 className="mt-4 text-4xl font-bold leading-tight text-slate-50 sm:text-5xl">
            One terminal to orchestrate every coding agent.
          </h1>
          <p className="mt-6 text-lg text-slate-300">
            Spin up tmux-backed agents, route tasks intelligently, and capture summaries—all from a single glass cockpit.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <span className="rounded-full bg-brand-500 px-6 py-3 text-sm font-semibold text-slate-950 transition">
              Auth coming soon
            </span>
            <Link
              href="/dashboard"
              className="rounded-full border border-slate-700 px-6 py-3 text-sm font-semibold text-slate-200 hover:border-brand-500 hover:text-brand-200"
            >
              View dashboard
            </Link>
          </div>
        </div>
        <TerminalPreview />
      </section>
      <SummaryCards />
    </div>
  );
}
