import DashboardTerminal from "../../components/DashboardTerminal";

export default function DashboardPage() {
  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-8">
      <header className="glass-panel rounded-3xl p-6">
        <h2 className="text-2xl font-semibold text-slate-100">Live Task Console</h2>
        <p className="mt-3 text-sm text-slate-300">
          Authentication is coming soon. For now, preview simulated delegation runs below.
        </p>
      </header>
      <DashboardTerminal />
    </div>
  );
}
