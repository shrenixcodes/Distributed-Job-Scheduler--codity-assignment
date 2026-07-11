import { Activity, HardDrive, LayoutDashboard, List, LogOut, Users } from 'lucide-react';
import { NavLink } from 'react-router-dom';

interface NavbarProps {
  onLogout: () => void;
}

const navigation = [
  { to: '/dashboard', label: 'Overview', icon: LayoutDashboard },
  { to: '/queues', label: 'Queues', icon: List },
  { to: '/jobs', label: 'Jobs', icon: HardDrive },
  { to: '/workers', label: 'Workers', icon: Users },
];

const Navbar = ({ onLogout }: NavbarProps) => (
  <nav className="navbar">
    <NavLink to="/dashboard" className="navbar-brand" aria-label="Dispatch overview">
      <span className="brand-mark"><Activity size={19} /></span>
      <span>Dispatch</span>
    </NavLink>
    <div className="navbar-links">
      {navigation.map(({ to, label, icon: Icon }) => (
        <NavLink key={to} to={to} className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
          <Icon size={17} /><span>{label}</span>
        </NavLink>
      ))}
    </div>
    <button onClick={onLogout} className="logout-button"><LogOut size={17} /><span>Sign out</span></button>
  </nav>
);

export default Navbar;
