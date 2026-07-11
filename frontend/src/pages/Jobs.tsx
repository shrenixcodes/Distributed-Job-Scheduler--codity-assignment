import { useCallback, useEffect, useMemo, useState, type FormEvent } from 'react';
import { Braces, Clock3, LoaderCircle, Plus, RefreshCw } from 'lucide-react';
import api from '../api';
import type { Job, Queue } from '../types';
import { formatDate, getApiError } from '../utils';

const statusOptions = ['queued', 'claimed', 'running', 'completed', 'failed'];

const Jobs = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [queues, setQueues] = useState<Queue[]>([]);
  const [queueId, setQueueId] = useState('');
  const [filterQueueId, setFilterQueueId] = useState('');
  const [status, setStatus] = useState('');
  const [payload, setPayload] = useState('{\n  "type": "send_email",\n  "recipient": "customer@example.com"\n}');
  const [priority, setPriority] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const loadData = useCallback(async () => {
    setError('');
    try {
      const [jobsResponse, queuesResponse] = await Promise.all([api.get<Job[]>('/api/jobs/', { params: { queue_id: filterQueueId || undefined, status: status || undefined } }), api.get<Queue[]>('/api/queues/')]);
      setJobs(jobsResponse.data); setQueues(queuesResponse.data); setQueueId((current) => current || queuesResponse.data[0]?.id || '');
    } catch (requestError) { setError(getApiError(requestError)); }
    finally { setLoading(false); }
  }, [filterQueueId, status]);

  useEffect(() => { void loadData(); }, [loadData]);
  const queueNames = useMemo(() => new Map(queues.map((queue) => [queue.id, queue.name])), [queues]);

  const handleCreateJob = async (event: FormEvent) => {
    event.preventDefault(); setError(''); setNotice('');
    if (!queueId) { setError('Create a queue before submitting a job.'); return; }
    let parsedPayload: unknown;
    try { parsedPayload = JSON.parse(payload); }
    catch { setError('Payload must be valid JSON.'); return; }
    setSubmitting(true);
    try {
      await api.post('/api/jobs/', { queue_id: queueId, payload: parsedPayload, priority });
      setNotice('Job accepted and added to the selected queue.');
      await loadData();
    } catch (requestError) { setError(getApiError(requestError, 'We could not submit that job.')); }
    finally { setSubmitting(false); }
  };

  if (loading) return <div className="page-loading"><LoaderCircle className="spin" size={24} /> Loading jobs…</div>;

  return <div className="page-stack">
    <header className="page-header"><div><p className="eyebrow">Workload</p><h1>Jobs</h1><p>Submit work, inspect payloads, and follow each job through its lifecycle.</p></div><button onClick={() => void loadData()} className="secondary-button"><RefreshCw size={17} /> Refresh</button></header>
    {error && <div className="form-alert page-alert" role="alert">{error}</div>}{notice && <div className="form-notice page-alert" role="status">{notice}</div>}
    <section className="surface creation-surface"><div className="surface-header"><div><h2>Submit a job</h2><p>Jobs are processed in priority order within their queue.</p></div><span className="surface-icon"><Braces size={19} /></span></div>
      <form onSubmit={handleCreateJob} className="job-form"><label><span>Queue</span><select value={queueId} onChange={(event) => setQueueId(event.target.value)} disabled={!queues.length}>{queues.length ? queues.map((queue) => <option key={queue.id} value={queue.id}>{queue.name}</option>) : <option>Create a queue first</option>}</select></label><label><span>Priority</span><input type="number" min="0" max="100" value={priority} onChange={(event) => setPriority(Number(event.target.value))} /></label><label className="payload-field"><span>Payload <small>valid JSON</small></span><textarea value={payload} onChange={(event) => setPayload(event.target.value)} spellCheck="false" rows={5} /></label><button type="submit" className="primary-button" disabled={submitting || !queues.length}>{submitting ? 'Submitting…' : 'Submit job'} <Plus size={18} /></button></form>
    </section>
    <section className="filter-row"><div><label>Queue<select value={filterQueueId} onChange={(event) => setFilterQueueId(event.target.value)}><option value="">All queues</option>{queues.map((queue) => <option key={queue.id} value={queue.id}>{queue.name}</option>)}</select></label><label>Status<select value={status} onChange={(event) => setStatus(event.target.value)}><option value="">All statuses</option>{statusOptions.map((value) => <option key={value} value={value}>{value}</option>)}</select></label></div><span>{jobs.length} job{jobs.length === 1 ? '' : 's'} shown</span></section>
    {jobs.length ? <section className="job-table surface"><div className="job-table-head"><span>Job</span><span>Queue</span><span>Priority</span><span>Status</span><span>Created</span></div>{jobs.map((job) => <details key={job.id} className="job-row"><summary><span className="job-id">{job.id.slice(0, 8)}…</span><strong>{queueNames.get(job.queue_id) ?? 'Unknown queue'}</strong><span>{job.priority}</span><span className={`status-badge ${job.status}`}>{job.status}</span><time>{formatDate(job.created_at)}</time></summary><pre>{JSON.stringify(job.payload, null, 2)}</pre></details>)}</section> : <section className="empty-state surface"><div className="empty-icon"><Clock3 size={25} /></div><h2>No jobs match this view</h2><p>Submit a job above, or adjust your queue and status filters.</p></section>}
  </div>;
};

export default Jobs;
