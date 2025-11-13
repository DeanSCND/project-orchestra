'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

type RunStatus = 'running' | 'completed' | 'failed';

type RunLog = {
  runId: string;
  agent: string;
  task: string;
  status: RunStatus;
  timestamp: string;
};

type Envelope = {
  type?: string;
  payload?: Record<string, unknown> | null;
  from?: string;
  meta?: Record<string, unknown> | null;
};

type EventLog = {
  id: string;
  type: string;
  from: string;
  receivedAt: string;
  payloadPreview: string;
};

type ConnectionState = 'idle' | 'connecting' | 'connected' | 'disconnected' | 'error' | 'disabled';

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

function normaliseStatus(rawStatus: unknown): RunStatus {
  const status = String(rawStatus ?? '').toLowerCase();
  if (status === 'success' || status === 'completed') {
    return 'completed';
  }
  if (status === 'failed' || status === 'error') {
    return 'failed';
  }
  return 'running';
}

function extractRun(envelope: Envelope): RunLog | null {
  if (!envelope.payload || typeof envelope.payload !== 'object') {
    return null;
  }
  const payload = envelope.payload as Record<string, unknown>;
  const runId = payload.runId ?? payload.id ?? payload.run_id;
  const agent = payload.agent ?? payload.secondary ?? payload.tool;
  const task = payload.task ?? payload.description ?? envelope.type;
  const status = payload.status ?? payload.state;
  if (!runId || !agent || !status) {
    return null;
  }
  const timestamp = payload.timestamp ?? payload.completed_at ?? new Date().toISOString();
  const formattedTime = new Date(String(timestamp)).toLocaleTimeString(undefined, {
    hour: '2-digit',
    minute: '2-digit',
  });
  return {
    runId: String(runId),
    agent: String(agent),
    task: String(task ?? 'Unknown task'),
    status: normaliseStatus(status),
    timestamp: formattedTime,
  };
}

function formatEventPayload(payload: unknown): string {
  if (payload == null) {
    return '—';
  }
  try {
    const serialised = JSON.stringify(payload);
    return serialised.length > 120 ? `${serialised.slice(0, 117)}…` : serialised;
  } catch {
    return '[unserializable payload]';
  }
}

function buildEvent(envelope: Envelope): EventLog {
  return {
    id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
    type: envelope.type ?? 'unknown',
    from: envelope.from ?? 'daemon',
    receivedAt: new Date().toLocaleTimeString(undefined, {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    }),
    payloadPreview: formatEventPayload(envelope.payload),
  };
}

const connectionColours: Record<ConnectionState, string> = {
  idle: 'text-slate-400',
  connecting: 'text-amber-300',
  connected: 'text-emerald-300',
  disconnected: 'text-amber-400',
  error: 'text-rose-300',
  disabled: 'text-slate-500',
};

const connectionLabels: Record<ConnectionState, string> = {
  idle: 'Idle',
  connecting: 'Connecting',
  connected: 'Connected',
  disconnected: 'Disconnected',
  error: 'Error',
  disabled: 'Disabled',
};

export default function DashboardTerminal() {
  const [runs, setRuns] = useState<RunLog[]>(MOCK_RUNS);
  const [highlightIndex, setHighlightIndex] = useState(0);
  const [events, setEvents] = useState<EventLog[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionState>('idle');
  const [lastAck, setLastAck] = useState<string | null>(null);
  const [lastError, setLastError] = useState<string | null>(null);

  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (runs.length === 0) {
      return undefined;
    }
    const poller = setInterval(() => {
      setHighlightIndex((prev) => ((prev + 1) % runs.length));
    }, 4000);
    return () => clearInterval(poller);
  }, [runs.length]);

  useEffect(() => {
    if (runs.length > 0 && highlightIndex >= runs.length) {
      setHighlightIndex(0);
    }
  }, [highlightIndex, runs.length]);

  const daemonBase = process.env.NEXT_PUBLIC_DAEMON_WS_URL ?? '';
  const daemonToken = process.env.NEXT_PUBLIC_DAEMON_TOKEN ?? '';

  const websocketUrl = useMemo(() => {
    if (!daemonBase) {
      return undefined;
    }
    if (!daemonToken) {
      return daemonBase;
    }
    const separator = daemonBase.includes('?') ? '&' : '?';
    return `${daemonBase}${separator}token=${encodeURIComponent(daemonToken)}`;
  }, [daemonBase, daemonToken]);

  const handleEnvelope = useCallback((envelope: Envelope) => {
    if (envelope.type === 'ack') {
      setLastAck(new Date().toLocaleTimeString());
      return;
    }

    setEvents((prev) => {
      const nextEvents = [buildEvent(envelope), ...prev];
      return nextEvents.slice(0, 20);
    });

    const run = extractRun(envelope);
    if (run) {
      setRuns((prev) => {
        const existingIndex = prev.findIndex((item) => item.runId === run.runId);
        if (existingIndex >= 0) {
          const updated = [...prev];
          updated[existingIndex] = { ...updated[existingIndex], ...run };
          return updated;
        }
        return [run, ...prev].slice(0, 20);
      });
      setHighlightIndex(0);
    }
  }, []);

  useEffect(() => {
    if (!websocketUrl) {
      setConnectionStatus('disabled');
      return undefined;
    }

    let cancelled = false;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

    const connect = () => {
      if (cancelled) {
        return;
      }
      setConnectionStatus('connecting');
      setLastError(null);

      const socket = new WebSocket(websocketUrl);
      socketRef.current = socket;

      socket.onopen = () => {
        if (cancelled) {
          return;
        }
        setConnectionStatus('connected');
        socket.send(
          JSON.stringify({
            type: 'hello',
            payload: {
              client: 'web-ui',
              version: '0.1.0',
              ts: new Date().toISOString(),
            },
          }),
        );
      };

      socket.onmessage = (event) => {
        if (cancelled) {
          return;
        }
        try {
          const envelope = JSON.parse(event.data) as Envelope;
          handleEnvelope(envelope);
        } catch {
          setLastError('Failed to parse daemon payload');
        }
      };

      socket.onerror = () => {
        if (cancelled) {
          return;
        }
        setConnectionStatus('error');
        setLastError('WebSocket reported an error');
      };

      socket.onclose = () => {
        if (cancelled) {
          return;
        }
        setConnectionStatus('disconnected');
        reconnectTimer = setTimeout(connect, 5000);
      };
    };

    connect();

    return () => {
      cancelled = true;
      if (reconnectTimer) {
        clearTimeout(reconnectTimer);
      }
      if (socketRef.current && socketRef.current.readyState < WebSocket.CLOSING) {
        socketRef.current.close();
      }
      socketRef.current = null;
    };
  }, [handleEnvelope, websocketUrl]);

  const summary = useMemo(() => {
    const completed = runs.filter((run) => run.status === 'completed').length;
    return { total: runs.length, completed };
  }, [runs]);

  return (
    <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
      <section className="glass-panel rounded-3xl p-6">
        <div className="flex items-center justify-between">
          <h3 className="text-sm uppercase tracking-[0.4em] text-brand-200">Live runs</h3>
          <span className={`text-xs font-semibold ${connectionColours[connectionStatus]}`}>
            {connectionLabels[connectionStatus]}
          </span>
        </div>
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
          {runs.length === 0 && (
            <div className="rounded-2xl border border-dashed border-slate-700/60 bg-slate-900/50 px-4 py-6 text-center text-sm text-slate-400">
              Awaiting run events from the daemon…
            </div>
          )}
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
          <div>
            <dt className="text-slate-400">Last daemon ack</dt>
            <dd className="text-sm text-slate-200">{lastAck ?? '—'}</dd>
          </div>
          {lastError && (
            <div>
              <dt className="text-slate-400">Last error</dt>
              <dd className="text-sm text-rose-300">{lastError}</dd>
            </div>
          )}
        </dl>
        <div className="mt-6">
          <h4 className="text-xs uppercase tracking-[0.4em] text-brand-200">Recent events</h4>
          <ul className="mt-3 space-y-2 text-xs text-slate-300">
            {events.length === 0 && <li className="text-slate-500">No events received yet.</li>}
            {events.map((event) => (
              <li
                key={event.id}
                className="rounded-xl border border-slate-800/60 bg-slate-900/70 px-3 py-2"
              >
                <div className="flex items-center justify-between text-[11px] text-slate-400">
                  <span className="font-semibold text-slate-200">{event.type}</span>
                  <time>{event.receivedAt}</time>
                </div>
                <p className="mt-1 text-[11px] text-slate-500">from {event.from}</p>
                <p className="mt-2 font-mono text-[11px] text-slate-400">{event.payloadPreview}</p>
              </li>
            ))}
          </ul>
        </div>
      </aside>
    </div>
  );
}
