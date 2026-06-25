import { Link } from 'react-router-dom';
import './Header.css';

export default function Header() {
  return (
    <header className="header">
      <div className="header__inner">
        <Link to="/" className="header__logo">
          <span className="header__icon">✈</span> SkyAgent
        </Link>
        <nav className="header__nav">
          <Link to="/">Buscar Voos</Link>
          <Link to="/fidelidade">Milhas</Link>
          <Link to="/suporte">Suporte</Link>
        </nav>
      </div>
    </header>
  );
}
