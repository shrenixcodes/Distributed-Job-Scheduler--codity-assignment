export interface Project {
  id: string;
  name: string;
  description?: string | null;
  organization_id: string;
  created_at: string;
}

export interface Queue {
  id: string;
  name: string;
  description?: string | null;
  project_id: string;
  is_paused: boolean;
  concurrency_limit: number;
  priority: number;
  created_at: string;
}

export interface Job {
  id: string;
  queue_id: string;
  status: 'queued' | 'claimed' | 'running' | 'completed' | 'failed' | string;
  payload: unknown;
  priority: number;
  scheduled_at?: string | null;
  created_at: string;
}

export interface Worker {
  id: string;
  name: string;
  status: string;
  last_heartbeat?: string | null;
  created_at: string;
}
