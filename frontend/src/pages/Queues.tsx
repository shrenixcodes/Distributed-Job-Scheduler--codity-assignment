
import { useEffect, useState } from 'react';
import api from '../api';

interface Queue {
  id: string;
  name: string;
  description?: string;
  is_paused: boolean;
  concurrency_limit: number;
  priority: number;
  created_at: string;
}

const Queues = () => {
  const [queues, setQueues] = useState<Queue[]>([]);
  const [newQueueName, setNewQueueName] = useState('');
  const [newQueueProjectId, setNewQueueProjectId] = useState('');

  useEffect(() => {
    fetchQueues();
  }, []);

  const fetchQueues = async () => {
    const res = await api.get('/api/queues');
    setQueues(res.data);
  };

  const handleCreateQueue = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post('/api/queues', {
      name: newQueueName,
      project_id: newQueueProjectId || '00000000-0000-0000-0000-000000000000',
    });
    setNewQueueName('');
    fetchQueues();
  };

  const togglePause = async (queue: Queue) => {
    const endpoint = queue.is_paused ? 'resume' : 'pause';
    await api.post(`/api/queues/${queue.id}/${endpoint}`);
    fetchQueues();
  };

  return (
    <div className="queues-page">
      <h1>Queues</h1>
      <form onSubmit={handleCreateQueue} className="create-form">
        <input
          placeholder="Queue Name"
          value={newQueueName}
          onChange={(e) => setNewQueueName(e.target.value)}
          required
        />
        <button type="submit">Create Queue</button>
      </form>
      <div className="queues-list">
        {queues.map((queue) => (
          <div key={queue.id} className="queue-card">
            <div className="queue-header">
              <h3>{queue.name}</h3>
              <span className={`queue-status ${queue.is_paused ? 'paused' : 'active'}`}>
                {queue.is_paused ? 'Paused' : 'Active'}
              </span>
            </div>
            <p>{queue.description}</p>
            <div className="queue-meta">
              <span>Concurrency: {queue.concurrency_limit}</span>
              <span>Priority: {queue.priority}</span>
            </div>
            <button onClick={() => togglePause(queue)} className="toggle-btn">
              {queue.is_paused ? 'Resume' : 'Pause'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Queues;
