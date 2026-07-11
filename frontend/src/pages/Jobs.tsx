
import { useEffect, useState } from 'react';
import api from '../api';

interface Job {
  id: string;
  status: string;
  payload: any;
  created_at: string;
}

const Jobs = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [queueId, setQueueId] = useState('');
  const [status, setStatus] = useState('');
  const [payload, setPayload] = useState('{}');
  const [selectedQueueId, setSelectedQueueId] = useState('');

  useEffect(() => {
    fetchJobs();
  }, [selectedQueueId, status]);

  const fetchJobs = async () => {
    const params: any = {};
    if (selectedQueueId) params.queue_id = selectedQueueId;
    if (status) params.status = status;
    const res = await api.get('/api/jobs', { params });
    setJobs(res.data);
  };

  const handleCreateJob = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post('/api/jobs', {
      queue_id: queueId || '00000000-0000-0000-0000-000000000000',
      payload: JSON.parse(payload),
    });
    setPayload('{}');
    fetchJobs();
  };

  return (
    <div className="jobs-page">
      <h1>Jobs</h1>
      <div className="filters">
        <select value={selectedQueueId} onChange={(e) => setSelectedQueueId(e.target.value)}>
          <option value="">All Queues</option>
        </select>
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All Status</option>
          <option value="queued">Queued</option>
          <option value="claimed">Claimed</option>
          <option value="running">Running</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
        </select>
      </div>
      <form onSubmit={handleCreateJob} className="create-form">
        <input
          placeholder="Queue ID"
          value={queueId}
          onChange={(e) => setQueueId(e.target.value)}
        />
        <textarea
          placeholder="Payload (JSON)"
          value={payload}
          onChange={(e) => setPayload(e.target.value)}
          rows={3}
        />
        <button type="submit">Create Job</button>
      </form>
      <div className="jobs-list">
        {jobs.map((job) => (
          <div key={job.id} className="job-card">
            <div className="job-header">
              <h4>{job.id}</h4>
              <span className={`job-status ${job.status}`}>{job.status}</span>
            </div>
            <pre>{JSON.stringify(job.payload, null, 2)}</pre>
            <p className="job-date">{new Date(job.created_at).toLocaleString()}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Jobs;
