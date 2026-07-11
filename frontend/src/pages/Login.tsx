
import { useState } from 'react';
import api from '../api';

interface LoginProps {
  onLogin: (token: string) => void;
}

const Login = ({ onLogin }: LoginProps) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [fullName, setFullName] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (isRegister) {
        await api.post('/api/auth/register', { email, password, full_name: fullName });
      }
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      const res = await api.post('/api/auth/login', formData);
      onLogin(res.data.access_token);
    } catch (err) {
      console.error(err);
      alert('Error');
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>{isRegister ? 'Register' : 'Login'}</h1>
        <form onSubmit={handleSubmit}>
          {isRegister && (
            <input
              type="text"
              placeholder="Full Name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
            />
          )}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">{isRegister ? 'Register' : 'Login'}</button>
        </form>
        <button onClick={() => setIsRegister(!isRegister)} className="toggle-btn">
          {isRegister ? 'Already have an account? Login' : "Don't have an account? Register"}
        </button>
      </div>
    </div>
  );
};

export default Login;
