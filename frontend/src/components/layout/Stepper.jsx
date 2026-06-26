import { useLocation } from 'react-router-dom';
import './Stepper.css';

const STEPS = [
  { path: '/resultados', label: 'Busca' },
  { path: '/reserva', label: 'Reserva' },
  { path: '/pagamento', label: 'Pagamento' },
  { path: '/confirmacao', label: 'Confirmação' },
];

export default function Stepper() {
  const { pathname } = useLocation();
  const current = STEPS.findIndex((s) => s.path === pathname);
  if (current === -1) return null;

  return (
    <nav className="stepper" aria-label="Progresso da compra">
      <ol className="stepper__list">
        {STEPS.map((step, i) => {
          const state = i < current ? 'done' : i === current ? 'current' : 'todo';
          return (
            <li key={step.path} className={`stepper__item stepper__item--${state}`}>
              <span className="stepper__dot" aria-hidden="true">
                {state === 'done' ? '✓' : i + 1}
              </span>
              <span className="stepper__label">
                {step.label}
                {state === 'current' && <span className="sr-only"> (etapa atual)</span>}
              </span>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
