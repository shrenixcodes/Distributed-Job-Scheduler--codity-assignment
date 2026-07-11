
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import './App.css';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Queues from './pages/Queues';
import Jobs from './pages/Jobs';
import Workers from './pages/Workers';
import Navbar from './components/Navbar';

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  return (
    <Router>
      <div className="app">
        {token ? (
          <>
            <Navbar onLogout={() => setToken(null)} />
            <div className="content">
              <Routes>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/queues" element={<Queues />} />
                <Route path="/jobs" element={<Jobs />} />
                <Route path="/workers" element={<Workers />} />
              </Routes>
            </div>
          </>
        ) : (
          <Login onLogin={setToken} />
        )}
      </div>
    </Router>
  );
}

export default App;
