const cards = [
  {
    title: 'Hands-off delegation',
    desc: 'Send tasks from Claude to Droid, Cursor, or Aider while tmux sessions stay observable.',
  },
  {
    title: 'Context-aware summaries',
    desc: 'Automatic task recaps prevent context pollution and keep Claude in control.',
  },
  {
    title: 'Cost awareness',
    desc: 'Track run metadata and costs so you know when to escalate to premium agents.',
  },
];

export default function SummaryCards() {
  return (
    <section className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {cards.map((card) => (
        <article key={card.title} className="glass-panel rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-slate-100">{card.title}</h3>
          <p className="mt-3 text-sm text-slate-300">{card.desc}</p>
        </article>
      ))}
    </section>
  );
}
