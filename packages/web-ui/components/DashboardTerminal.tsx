'use client';

import { useEffect, useMemo, useState } from 'react';

type RunLog = {
  runId: string;
  agent: string;
  task: string;
  status: 'running' | 'completed' | 'failed';
  timestamp: string;
};

const MOCK_RUNS: RunLog[] = [
  {
    runId: 'c87a3d00',
    agent: 'droid',
    task: 'Create User model',
    status: 'completed',
    timestamp: '2m ago',
  },
  {
    runId: '41d9ba27',
    agent: 'cursor',
    task: 'Ship dashboard header',
    status: 'running',
    timestamp: '45s ago',
  },
  {
    runId: '555dc78d',
    agent: 'aider',
    task: 'Refactor auth checks',
    status: 'completed',
    timestamp: '10m ago',
  },
];

export default function DashboardTerminal() {
  const runs = useMemo(() => MOCK_RUNS, []);
  const [highlightIndex, setHighlightIndex] = useState(0);

  useEffect(() => {
    const poller = setInterval(() => {
      setHighlightIndex((prev) => (prev + 1) % runs.length);
    }, 4000);
    return () => clearInterval(poller);
  }, [runs.length]);

  const summary = useMemo(() => {
    const completed = runs.filter((run) => run.status === 'completed').length;
    return { total: runs.length, completed };
  }, [runs]);

  return (
    <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
      <section className="glass-panel rounded-3xl p-6">
        <h3 className="text-sm uppercase tracking-[0.4em] text-brand-200">Live runs</h3>
        <div className="mt-6 space-y-4">
          {runs.map((run, idx) => (
            <article
              key={run.runId}
              className={`rounded-2xl border px-4 py-3 transition ${
                highlightIndex === idx
                  ? 'border-brand-500 bg-brand-500/10'
                  : 'border-slate-700/60 bg-slate-900/70'
              }`}
            >
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span>{run.timestamp}</span>
                <span className="font-mono text-brand-100">{run.runId}</span>
              </div>
              <div className="mt-2 flex flex-wrap items-baseline gap-2">
                <span className="rounded-full bg-slate-800 px-2 py-0.5 text-[11px] uppercase text-slate-300">
                  {run.agent}
                </span>
                <p className="text-sm text-slate-100">{run.task}</p>
              </div>
              <p className="mt-1 text-xs uppercase tracking-wide text-slate-500">{run.status}</p>
            </article>
          ))}
        </div>
      </section>
      <aside className="glass-panel rounded-3xl p-6">
        <h3 className="text-sm uppercase tracking-[0.4em] text-brand-200">Summary</h3>
        <dl className="mt-6 space-y-4 text-sm">
          <div>
            <dt className="text-slate-400">Total runs</dt>
            <dd className="text-3xl font-semibold text-slate-100">{summary.total}</dd>
          </div>
          <div>
            <dt className="text-slate-400">Completed</dt>
            <dd className="text-3xl font-semibold text-emerald-300">{summary.completed}</dd>
          </div>
          <p className="mt-6 text-xs text-slate-400">
            Real-time data will stream from the daemon WebSocket once connected. For now, runs are simulated using mock payloads.
          </p>
        </dl>
      </aside>
    </div>
  );
}
