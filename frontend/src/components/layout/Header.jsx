import { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import './Header.css';

const LINKS = [
  { to: '/', label: 'Buscar Voos', end: true },
  { to: '/fidelidade', label: 'Milhas' },
  { to: '/suporte', label: 'Suporte' },
  { to: '/testes', label: 'Testes BDD' },
];

export default function Header() {
  const [aberto, setAberto] = useState(false);

  return (
    <header className="header">
      <div className="header__inner">
        <Link to="/" className="header__logo" onClick={() => setAberto(false)}>
          <span className="header__icon" aria-hidden="true">✈</span> SkyAgent
        </Link>

        <button
          type="button"
          className="header__toggle"
          aria-expanded={aberto}
          aria-controls="menu-principal"
          aria-label={aberto ? 'Fechar menu' : 'Abrir menu'}
          onClick={() => setAberto((v) => !v)}
        >
          <span aria-hidden="true">{aberto ? '✕' : '☰'}</span>
        </button>

        <nav
          id="menu-principal"
          className={`header__nav ${aberto ? 'header__nav--open' : ''}`}
          aria-label="Navegação principal"
        >
          {LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.end}
              className={({ isActive }) => (isActive ? 'is-active' : '')}
              onClick={() => setAberto(false)}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}
