import { FormEvent, useState } from 'react';
import { Activity, ArrowRight, CheckCircle2, LockKeyhole, Mail, Sparkles } from 'lucide-react';
import api from '../api';
import { getApiError } from '../utils';

interface LoginProps {
  onLogin: (token: string) => void;
}

const Login = ({ onLogin }: LoginProps) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError('');
    setIsSubmitting(true);
    try {
      if (isRegister) {
        await api.post('/api/auth/register', { email, password, full_name: fullName.trim() || null });
      }
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      const response = await api.post('/api/auth/login', formData);
      onLogin(response.data.access_token);
    } catch (requestError) {
      setError(getApiError(requestError, isRegister ? 'We could not create that account.' : 'We could not sign you in.'));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="auth-shell">
      <section className="auth-intro" aria-label="Product introduction">
        <div className="brand-lockup"><Activity size={24} /><span>Dispatch</span></div>
        <div className="intro-copy">
          <span className="eyebrow"><Sparkles size={15} /> Reliable job orchestration</span>
          <h1>Every background task, <em>under control.</em></h1>
          <p>Route, observe, and deliver work across priority queues from one focused control plane.</p>
        </div>
        <div className="intro-points">
          <span><CheckCircle2 size={17} /> Priority-aware queues</span>
          <span><CheckCircle2 size={17} /> Live worker visibility</span>
          <span><CheckCircle2 size={17} /> Clear job lifecycle</span>
        </div>
      </section>

      <section className="auth-panel">
        <div className="auth-card">
          <p className="eyebrow">{isRegister ? 'Create your workspace' : 'Welcome back'}</p>
          <h2>{isRegister ? 'Start orchestrating' : 'Sign in to Dispatch'}</h2>
          <p className="auth-subtitle">{isRegister ? 'Your organization is ready in a minute.' : 'Pick up where your operations left off.'}</p>

          <form onSubmit={handleSubmit} className="auth-form">
            {isRegister && (
              <label>
                <span>Full name <small>optional</small></span>
                <input type="text" placeholder="Ada Lovelace" value={fullName} onChange={(event) => setFullName(event.target.value)} autoComplete="name" />
              </label>
            )}
            <label>
              <span>Email address</span>
              <div className="field-with-icon"><Mail size={18} /><input type="email" placeholder="you@company.com" value={email} onChange={(event) => setEmail(event.target.value)} autoComplete="email" required /></div>
            </label>
            <label>
              <span>Password</span>
              <div className="field-with-icon"><LockKeyhole size={18} /><input type="password" placeholder="At least 8 characters" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete={isRegister ? 'new-password' : 'current-password'} minLength={8} required /></div>
            </label>
            {error && <div className="form-alert" role="alert">{error}</div>}
            <button type="submit" className="primary-button full-width" disabled={isSubmitting}>
              {isSubmitting ? 'Please wait…' : isRegister ? 'Create workspace' : 'Continue to Dispatch'} <ArrowRight size={18} />
            </button>
          </form>
          <button type="button" onClick={() => { setIsRegister((value) => !value); setError(''); }} className="text-button auth-switch">
            {isRegister ? 'Already have an account? Sign in' : 'New to Dispatch? Create an account'}
          </button>
        </div>
      </section>
    </main>
  );
};

export default Login;
