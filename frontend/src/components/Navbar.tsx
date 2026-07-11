
import { Link } from 'react-router-dom';
import { LayoutDashboard, List, HardDrive, Users, LogOut } from 'lucide-react';

interface NavbarProps {
  onLogout: () => void;
}

const Navbar = ({ onLogout }: NavbarProps) => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>Job Scheduler</h1>
      </div>
      <div className="navbar-links">
        <Link to="/dashboard" className="nav-link">
          <LayoutDashboard size={20} />
          <span>Dashboard</span>
        </Link>
        <Link to="/queues" className="nav-link">
          <List size={20} />
          <span>Queues</span>
        </Link>
        <Link to="/jobs" className="nav-link">
          <HardDrive size={20} />
          <span>Jobs</span>
        </Link>
        <Link to="/workers" className="nav-link">
          <Users size={20} />
          <span>Workers</span>
        </Link>
        <button onClick={onLogout} className="nav-link logout">
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
