import { useCallback, useEffect, useMemo, useState, type FormEvent } from 'react';
import { CirclePause, CirclePlay, FolderKanban, Layers3, LoaderCircle, Plus, RefreshCw } from 'lucide-react';
import api from '../api';
import type { Project, Queue } from '../types';
import { formatDate, getApiError } from '../utils';

const Queues = () => {
  const [queues, setQueues] = useState<Queue[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [projectId, setProjectId] = useState('');
  const [concurrency, setConcurrency] = useState(2);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [busyQueueId, setBusyQueueId] = useState<string | null>(null);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const loadData = useCallback(async () => {
    setError('');
    try {
      const [queueResponse, projectResponse] = await Promise.all([api.get<Queue[]>('/api/queues/'), api.get<Project[]>('/api/projects/')]);
      setQueues(queueResponse.data);
      setProjects(projectResponse.data);
      setProjectId((current) => current || projectResponse.data[0]?.id || '');
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void loadData(); }, [loadData]);
  const projectsById = useMemo(() => new Map(projects.map((project) => [project.id, project.name])), [projects]);

  const handleCreateQueue = async (event: FormEvent) => {
    event.preventDefault();
    if (!projectId) { setError('Create a demo workspace from Overview before adding a queue.'); return; }
    setSubmitting(true); setError(''); setNotice('');
    try {
      await api.post('/api/queues/', { name, description: description.trim() || null, project_id: projectId, concurrency_limit: concurrency });
      setName(''); setDescription(''); setConcurrency(2); setNotice('Queue created and ready to accept jobs.');
      await loadData();
    } catch (requestError) { setError(getApiError(requestError, 'We could not create that queue.')); }
    finally { setSubmitting(false); }
  };

  const togglePause = async (queue: Queue) => {
    setBusyQueueId(queue.id); setError(''); setNotice('');
    try {
      await api.post(`/api/queues/${queue.id}/${queue.is_paused ? 'resume' : 'pause'}`);
      setNotice(queue.is_paused ? 'Queue resumed.' : 'Queue paused. New work will wait safely.');
      await loadData();
    } catch (requestError) { setError(getApiError(requestError, 'We could not update that queue.')); }
    finally { setBusyQueueId(null); }
  };

  if (loading) return <div className="page-loading"><LoaderCircle className="spin" size={24} /> Loading queues…</div>;

  return <div className="page-stack">
    <header className="page-header"><div><p className="eyebrow">Routing</p><h1>Queues</h1><p>Balance urgent work, throughput, and concurrency in one place.</p></div><button onClick={() => void loadData()} className="secondary-button"><RefreshCw size={17} /> Refresh</button></header>
    {error && <div className="form-alert page-alert" role="alert">{error}</div>}
    {notice && <div className="form-notice page-alert" role="status">{notice}</div>}

    <section className="surface creation-surface">
      <div className="surface-header"><div><h2>Create a queue</h2><p>Queues isolate workloads and determine how much work can run at once.</p></div><span className="surface-icon"><Layers3 size={19} /></span></div>
      <form onSubmit={handleCreateQueue} className="queue-form">
        <label><span>Queue name</span><input placeholder="e.g. customer-notifications" value={name} onChange={(event) => setName(event.target.value)} required /></label>
        <label><span>Project</span><select value={projectId} onChange={(event) => setProjectId(event.target.value)} disabled={!projects.length}>{projects.length ? projects.map((project) => <option key={project.id} value={project.id}>{project.name}</option>) : <option>Create a workspace first</option>}</select></label>
        <label><span>Concurrency</span><input type="number" min="1" max="100" value={concurrency} onChange={(event) => setConcurrency(Number(event.target.value))} required /></label>
        <label className="wide-field"><span>Description <small>optional</small></span><input placeholder="What should this queue process?" value={description} onChange={(event) => setDescription(event.target.value)} /></label>
        <button type="submit" className="primary-button" disabled={submitting || !projects.length}>{submitting ? 'Creating…' : 'Create queue'} <Plus size={18} /></button>
      </form>
    </section>

    {queues.length ? <section className="queue-card-grid">{queues.map((queue) => <article key={queue.id} className="queue-card surface"><div className="queue-card-head"><div><span className={`status-badge ${queue.is_paused ? 'paused' : 'active'}`}>{queue.is_paused ? 'Paused' : 'Active'}</span><h2>{queue.name}</h2></div><button className="icon-button" onClick={() => void togglePause(queue)} disabled={busyQueueId === queue.id} title={queue.is_paused ? 'Resume queue' : 'Pause queue'}>{busyQueueId === queue.id ? <LoaderCircle className="spin" size={19} /> : queue.is_paused ? <CirclePlay size={19} /> : <CirclePause size={19} />}</button></div><p className="queue-description">{queue.description || 'No description added.'}</p><div className="queue-stat-row"><span><b>{queue.concurrency_limit}</b> concurrent jobs</span><span><b>{queue.priority}</b> priority</span></div><footer><FolderKanban size={15} /> {projectsById.get(queue.project_id) ?? 'Project'} <span>Created {formatDate(queue.created_at)}</span></footer></article>)}</section> : <section className="empty-state surface"><div className="empty-icon"><Layers3 size={25} /></div><h2>No queues yet</h2><p>Create a queue above to start routing jobs. Need a project first? Create the demo workspace from Overview.</p></section>}
  </div>;
};

export default Queues;
