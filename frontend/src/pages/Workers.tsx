import { useCallback, useEffect, useState } from 'react';
import { Activity, LoaderCircle, RefreshCw, Server, Wifi } from 'lucide-react';
import api from '../api';
import type { Worker } from '../types';
import { formatDate, getApiError } from '../utils';

const Workers = () => {
  const [workers, setWorkers] = useState<Worker[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadWorkers = useCallback(async () => {
    setError('');
    try { const response = await api.get<Worker[]>('/api/workers/'); setWorkers(response.data); }
    catch (requestError) { setError(getApiError(requestError)); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { void loadWorkers(); }, [loadWorkers]);
  if (loading) return <div className="page-loading"><LoaderCircle className="spin" size={24} /> Loading workers…</div>;

  return <div className="page-stack">
    <header className="page-header"><div><p className="eyebrow">Execution</p><h1>Workers</h1><p>Monitor the services that claim and execute jobs from your queues.</p></div><button onClick={() => void loadWorkers()} className="secondary-button"><RefreshCw size={17} /> Refresh</button></header>
    {error && <div className="form-alert page-alert" role="alert">{error}</div>}
    {workers.length ? <section className="worker-grid">{workers.map((worker) => <article key={worker.id} className="worker-card surface"><div className="worker-card-head"><span className="worker-icon"><Server size={21} /></span><span className={`status-badge ${worker.status === 'idle' || worker.status === 'running' ? 'active' : 'paused'}`}>{worker.status}</span></div><h2>{worker.name}</h2><p className="worker-id">{worker.id}</p><div className="worker-meta"><span><Wifi size={16} /> Last heartbeat</span><strong>{formatDate(worker.last_heartbeat)}</strong></div><div className="worker-meta"><span><Activity size={16} /> Registered</span><strong>{formatDate(worker.created_at)}</strong></div></article>)}</section> : <section className="empty-state surface worker-empty"><div className="empty-icon"><Server size={25} /></div><h2>No workers connected</h2><p>Start the worker service to claim queued work. Once it sends its first heartbeat, it will appear here.</p><code>python -m src.app.services.worker</code></section>}
  </div>;
};

export default Workers;
