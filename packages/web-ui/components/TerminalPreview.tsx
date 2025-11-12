'use client';

import { useEffect, useState } from 'react';

const sampleLines = [
  '🎼  orchestra.delegate --from claude --to droid --task "Bootstrap admin view"',
  '✅  claude: Run ID 4c2f91a3',
  '⏳  droid: 3 files modified, pushing patch...',
  '💾  summary: backend routes + tests updated',
  '—'.repeat(46),
  'next steps: approve diff or request follow-up'
];

export default function TerminalPreview() {
  const [visible, setVisible] = useState(1);

  useEffect(() => {
    const timer = setInterval(() => {
      setVisible((prev) => (prev === sampleLines.length ? 1 : prev + 1));
    }, 2400);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="glass-panel min-h-[320px] rounded-3xl p-6 text-sm text-slate-200 shadow-xl">
      <div className="flex items-center gap-2 text-xs text-slate-400">
        <span className="h-2 w-2 rounded-full bg-red-500" />
        <span className="h-2 w-2 rounded-full bg-amber-400" />
        <span className="h-2 w-2 rounded-full bg-emerald-500" />
        <span className="ml-auto text-xs uppercase text-brand-100">tmux session · primary</span>
      </div>
      <pre className="mt-6 whitespace-pre-wrap break-words font-mono text-[13px] leading-6">
        {sampleLines.slice(0, visible).join('\n')}
      </pre>
    </div>
  );
}
