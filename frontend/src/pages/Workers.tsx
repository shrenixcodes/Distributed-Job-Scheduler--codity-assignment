
import { useEffect, useState } from 'react';
import api from '../api';

interface Worker {
  id: string;
  name: string;
  status: string;
  last_heartbeat?: string;
  created_at: string;
}

const Workers = () => {
  const [workers, setWorkers] = useState<Worker[]>([]);

  useEffect(() => {
    fetchWorkers();
  }, []);

  const fetchWorkers = async () => {
    const res = await api.get('/api/workers');
    setWorkers(res.data);
  };

  return (
    <div className="workers-page">
      <h1>Workers</h1>
      <div className="workers-list">
        {workers.map((worker) => (
          <div key={worker.id} className="worker-card">
            <div className="worker-header">
              <h3>{worker.name}</h3>
              <span className={`worker-status ${worker.status}`}>{worker.status}</span>
            </div>
            <p>ID: {worker.id}</p>
            {worker.last_heartbeat && (
              <p>Last heartbeat: {new Date(worker.last_heartbeat).toLocaleString()}</p>
            )}
          </div>
        ))}
        {workers.length === 0 && (
          <p>No workers found. Start a worker to see it here.</p>
        )}
      </div>
    </div>
  );
};

export default Workers;
