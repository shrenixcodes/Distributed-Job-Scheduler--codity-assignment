
import { useEffect, useState } from 'react';
import api from '../api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { CheckCircle, AlertCircle, Clock, Activity } from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState({ completed: 0, failed: 0, queued: 0, running: 0 });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/api/jobs');
        const jobs = res.data;
        setStats({
          completed: jobs.filter((j: any) => j.status === 'completed').length,
          failed: jobs.filter((j: any) => j.status === 'failed').length,
          queued: jobs.filter((j: any) => j.status === 'queued').length,
          running: jobs.filter((j: any) => j.status === 'running' || j.status === 'claimed').length,
        });
      } catch (err) {
        console.error(err);
      }
    };
    fetchStats();
  }, []);

  const chartData = [
    { name: 'Completed', value: stats.completed, color: '#34d399' },
    { name: 'Failed', value: stats.failed, color: '#f87171' },
    { name: 'Queued', value: stats.queued, color: '#60a5fa' },
    { name: 'Running', value: stats.running, color: '#fbbf24' },
  ];

  const cards = [
    { 
      title: 'Completed', 
      value: stats.completed, 
      icon: CheckCircle, 
      color: 'linear-gradient(135deg, #10b981 0%, #34d399 100%)'
    },
    { 
      title: 'Failed', 
      value: stats.failed, 
      icon: AlertCircle, 
      color: 'linear-gradient(135deg, #ef4444 0%, #f87171 100%)'
    },
    { 
      title: 'Queued', 
      value: stats.queued, 
      icon: Clock, 
      color: 'linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%)'
    },
    { 
      title: 'Running', 
      value: stats.running, 
      icon: Activity, 
      color: 'linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)'
    },
  ];

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <div className="stats-grid">
        {cards.map((card, i) => {
          const IconComponent = card.icon;
          return (
            <div key={i} className="stat-card">
              <div 
                className="stat-icon" 
                style={{ background: card.color }}
              >
                <IconComponent size={40} color="#ffffff" />
              </div>
              <div>
                <h3 style={{ color: '#94a3b8', fontSize: '1.1rem', marginBottom: '0.5rem', fontWeight: 600 }}>
                  {card.title}
                </h3>
                <p className="stat-value">{card.value}</p>
              </div>
            </div>
          );
        })}
      </div>
      <div className="chart-container">
        <h2>Job Status Overview</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="name" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip 
              contentStyle={{ 
                background: 'rgba(30, 41, 59, 0.95)', 
                border: '1px solid rgba(148, 163, 184, 0.3)', 
                borderRadius: '0.75rem'
              }}
              itemStyle={{ color: '#f8fafc' }}
              labelStyle={{ color: '#94a3b8' }}
            />
            <Bar 
              dataKey="value" 
              fill="url(#colorGradient)" 
              radius={[8, 8, 0, 0]}
            />
            <defs>
              <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#60a5fa" />
                <stop offset="100%" stopColor="#c084fc" />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Dashboard;
