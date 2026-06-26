import { Link } from 'react-router-dom';
import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <nav className="footer__links" aria-label="Rodapé">
        <Link to="/">Buscar voos</Link>
        <Link to="/fidelidade">Milhas</Link>
        <Link to="/suporte">Suporte</Link>
      </nav>
      <p className="footer__copy">
        © 2026 SkyAgent — Plataforma Multi-Agente para Passagens Aéreas
      </p>
    </footer>
  );
}
