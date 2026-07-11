import { useCallback, useEffect, useMemo, useState, type ReactNode } from 'react';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Activity, ArrowRight, CheckCircle2, CircleAlert, Clock3, Layers3, LoaderCircle, Play, RefreshCw, Server } from 'lucide-react';
import api from '../api';
import type { Job, Project, Queue, Worker } from '../types';
import { formatDate, getApiError } from '../utils';

const Dashboard = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [queues, setQueues] = useState<Queue[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [workers, setWorkers] = useState<Worker[]>([]);
  const [loading, setLoading] = useState(true);
  const [seeding, setSeeding] = useState(false);
  const [error, setError] = useState('');

  const loadData = useCallback(async () => {
    setError('');
    try {
      const [jobResponse, queueResponse, projectResponse, workerResponse] = await Promise.all([
        api.get<Job[]>('/api/jobs/'), api.get<Queue[]>('/api/queues/'), api.get<Project[]>('/api/projects/'), api.get<Worker[]>('/api/workers/'),
      ]);
      setJobs(jobResponse.data);
      setQueues(queueResponse.data);
      setProjects(projectResponse.data);
      setWorkers(workerResponse.data);
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void loadData(); }, [loadData]);

  const totals = useMemo(() => ({
    queued: jobs.filter((job) => job.status === 'queued').length,
    running: jobs.filter((job) => job.status === 'running' || job.status === 'claimed').length,
    completed: jobs.filter((job) => job.status === 'completed').length,
    failed: jobs.filter((job) => job.status === 'failed').length,
  }), [jobs]);

  const successRate = totals.completed + totals.failed ? Math.round((totals.completed / (totals.completed + totals.failed)) * 100) : 100;
  const chartData = [
    { name: 'Queued', value: totals.queued, fill: '#8b5cf6' },
    { name: 'Active', value: totals.running, fill: '#22c55e' },
    { name: 'Done', value: totals.completed, fill: '#38bdf8' },
    { name: 'Failed', value: totals.failed, fill: '#fb7185' },
  ];

  const createDemoWorkspace = async () => {
    setSeeding(true);
    setError('');
    try {
      const project = await api.post<Project>('/api/projects/', { name: 'Launch operations', description: 'A demo workspace for the product walkthrough.' });
      const [deliveryQueue, reportingQueue] = await Promise.all([
        api.post<Queue>('/api/queues/', { name: 'customer-notifications', description: 'High-priority customer communication', project_id: project.data.id, priority: 10, concurrency_limit: 4 }),
        api.post<Queue>('/api/queues/', { name: 'analytics-refresh', description: 'Scheduled reporting and metric refreshes', project_id: project.data.id, priority: 5, concurrency_limit: 2 }),
      ]);
      await Promise.all([
        api.post('/api/jobs/', { queue_id: deliveryQueue.data.id, priority: 10, payload: { type: 'welcome_email', recipient: 'customer@example.com', campaign: 'Product launch' } }),
        api.post('/api/jobs/', { queue_id: deliveryQueue.data.id, priority: 8, payload: { type: 'invoice_ready', account_id: 'acct_2048' } }),
        api.post('/api/jobs/', { queue_id: reportingQueue.data.id, priority: 5, payload: { type: 'daily_rollup', date: 'today' } }),
      ]);
      await loadData();
    } catch (requestError) {
      setError(getApiError(requestError, 'We could not set up the demo workspace.'));
    } finally {
      setSeeding(false);
    }
  };

  const queueNames = new Map(queues.map((queue) => [queue.id, queue.name]));
  const queueJobCounts = new Map(queues.map((queue) => [queue.id, jobs.filter((job) => job.queue_id === queue.id).length]));

  if (loading) return <div className="page-loading"><LoaderCircle className="spin" size={24} /> Loading your control plane…</div>;

  return (
    <div className="dashboard page-stack">
      <header className="page-header">
        <div><p className="eyebrow">Control plane</p><h1>Operations at a glance</h1><p>Track the work moving through your distributed system.</p></div>
        <button onClick={() => void loadData()} className="secondary-button"><RefreshCw size={17} /> Refresh</button>
      </header>
      {error && <div className="form-alert page-alert" role="alert">{error}</div>}

      {projects.length === 0 ? (
        <section className="empty-hero">
          <div className="empty-icon"><Layers3 size={28} /></div>
          <div><p className="eyebrow">Ready when you are</p><h2>Set up a working demo in one click</h2><p>Create an isolated project, two priority queues, and three ready-to-run jobs. You can edit everything afterward.</p></div>
          <button onClick={() => void createDemoWorkspace()} className="primary-button" disabled={seeding}>{seeding ? 'Creating workspace…' : 'Create demo workspace'} <ArrowRight size={18} /></button>
        </section>
      ) : (
        <>
          <section className="metrics-grid">
            <Metric title="Total jobs" value={jobs.length} detail={`${projects.length} project${projects.length === 1 ? '' : 's'}`} icon={<Layers3 size={20} />} tone="violet" />
            <Metric title="Ready to run" value={totals.queued} detail={`${queues.filter((queue) => !queue.is_paused).length} active queue${queues.filter((queue) => !queue.is_paused).length === 1 ? '' : 's'}`} icon={<Clock3 size={20} />} tone="blue" />
            <Metric title="In progress" value={totals.running} detail={`${workers.length} connected worker${workers.length === 1 ? '' : 's'}`} icon={<Activity size={20} />} tone="green" />
            <Metric title="Success rate" value={`${successRate}%`} detail={totals.failed ? `${totals.failed} job${totals.failed === 1 ? '' : 's'} need attention` : 'No failed jobs'} icon={<CheckCircle2 size={20} />} tone="coral" />
          </section>

          <section className="dashboard-grid">
            <article className="surface chart-surface">
              <div className="surface-header"><div><h2>Job throughput</h2><p>Current lifecycle distribution</p></div><span className="live-indicator"><i /> Live</span></div>
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={chartData} margin={{ top: 8, right: 8, left: -24, bottom: 0 }}>
                  <CartesianGrid vertical={false} stroke="#e9edf5" strokeDasharray="4 4" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#75809a', fontSize: 12 }} dy={12} />
                  <YAxis allowDecimals={false} axisLine={false} tickLine={false} tick={{ fill: '#75809a', fontSize: 12 }} />
                  <Tooltip cursor={{ fill: '#f5f7fb' }} contentStyle={{ borderRadius: 12, border: '1px solid #e4e9f2', boxShadow: '0 12px 28px rgba(30, 41, 59, 0.12)' }} />
                  <Bar dataKey="value" fill="#7256e8" radius={[7, 7, 2, 2]} />
                </BarChart>
              </ResponsiveContainer>
            </article>
            <article className="surface health-surface">
              <div className="surface-header"><div><h2>System health</h2><p>Connection and capacity status</p></div></div>
              <div className="health-list">
                <HealthRow label="API control plane" value="Operational" icon={<CheckCircle2 size={18} />} status="good" />
                <HealthRow label="Queue capacity" value={`${queues.filter((queue) => !queue.is_paused).length} active`} icon={<Play size={18} />} status={queues.some((queue) => !queue.is_paused) ? 'good' : 'neutral'} />
                <HealthRow label="Worker pool" value={workers.length ? `${workers.length} connected` : 'Awaiting worker'} icon={<Server size={18} />} status={workers.length ? 'good' : 'neutral'} />
                {totals.failed > 0 && <HealthRow label="Attention needed" value={`${totals.failed} failed`} icon={<CircleAlert size={18} />} status="warning" />}
              </div>
            </article>
          </section>

          <section className="dashboard-grid lower-grid">
            <article className="surface">
              <div className="surface-header"><div><h2>Queues</h2><p>Priority and workload at a glance</p></div></div>
              <div className="queue-overview-list">
                {queues.slice(0, 4).map((queue) => <div key={queue.id} className="queue-overview"><div className={`queue-dot${queue.is_paused ? ' paused' : ''}`} /><div className="queue-overview-main"><strong>{queue.name}</strong><span>Priority {queue.priority} · Concurrency {queue.concurrency_limit}</span></div><span className="count-badge">{queueJobCounts.get(queue.id) ?? 0} jobs</span></div>)}
              </div>
            </article>
            <article className="surface">
              <div className="surface-header"><div><h2>Recent jobs</h2><p>Latest arrivals in your queues</p></div></div>
              <div className="recent-job-list">
                {jobs.slice(0, 4).map((job) => <div key={job.id} className="recent-job"><span className={`status-dot ${job.status}`} /><div><strong>{queueNames.get(job.queue_id) ?? 'Unknown queue'}</strong><span>{formatDate(job.created_at)}</span></div><span className={`status-badge ${job.status}`}>{job.status}</span></div>)}
              </div>
            </article>
          </section>
        </>
      )}
    </div>
  );
};

function Metric({ title, value, detail, icon, tone }: { title: string; value: string | number; detail: string; icon: ReactNode; tone: string }) {
  return <article className="metric-card"><span className={`metric-icon ${tone}`}>{icon}</span><div><p>{title}</p><h2>{value}</h2><small>{detail}</small></div></article>;
}

function HealthRow({ label, value, icon, status }: { label: string; value: string; icon: ReactNode; status: string }) {
  return <div className="health-row"><span className={`health-icon ${status}`}>{icon}</span><span>{label}</span><strong>{value}</strong></div>;
}

export default Dashboard;
