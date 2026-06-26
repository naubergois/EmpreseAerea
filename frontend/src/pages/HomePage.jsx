import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useBooking } from '../context/BookingContext';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { todayISO } from '../utils/formatters';
import './HomePage.css';

export default function HomePage() {
  useDocumentTitle('Buscar voos');
  const navigate = useNavigate();
  const { setSearch } = useBooking();
  const [form, setForm] = useState({
    origem: 'GRU', destino: 'GIG', data_ida: '2026-08-15', classe: 'economica', adultos: 1,
  });

  const update = (campo) => (e) => setForm({ ...form, [campo]: e.target.value });
  const updateIata = (campo) => (e) =>
    setForm({ ...form, [campo]: e.target.value.toUpperCase().replace(/[^A-Z]/g, '').slice(0, 3) });

  const handleSubmit = (e) => {
    e.preventDefault();
    setSearch(form);
    const params = new URLSearchParams(form);
    navigate(`/resultados?${params}`);
  };

  return (
    <div>
      <section className="hero">
        <h1 className="hero__title">Encontre seu próximo voo</h1>
        <p className="hero__subtitle">Busca inteligente com precificação dinâmica e milhas</p>
      </section>

      <form className="card search-form" onSubmit={handleSubmit}>
        <div className="search-form__grid">
          <div className="field">
            <label htmlFor="origem">Origem</label>
            <input
              id="origem"
              name="origem"
              value={form.origem}
              onChange={updateIata('origem')}
              placeholder="GRU"
              autoComplete="off"
              maxLength={3}
              aria-describedby="origem-hint"
              required
            />
            <span id="origem-hint" className="field__hint">Código IATA (3 letras)</span>
          </div>

          <div className="field">
            <label htmlFor="destino">Destino</label>
            <input
              id="destino"
              name="destino"
              value={form.destino}
              onChange={updateIata('destino')}
              placeholder="GIG"
              autoComplete="off"
              maxLength={3}
              required
            />
          </div>

          <div className="field">
            <label htmlFor="data_ida">Data de ida</label>
            <input
              id="data_ida"
              name="data_ida"
              type="date"
              min={todayISO()}
              value={form.data_ida}
              onChange={update('data_ida')}
              required
            />
          </div>

          <div className="field">
            <label htmlFor="classe">Classe</label>
            <select id="classe" name="classe" value={form.classe} onChange={update('classe')}>
              <option value="economica">Econômica</option>
              <option value="executiva">Executiva</option>
            </select>
          </div>

          <div className="field">
            <label htmlFor="adultos">Passageiros</label>
            <select id="adultos" name="adultos" value={form.adultos} onChange={update('adultos')}>
              {[1, 2, 3, 4, 5, 6].map((n) => (
                <option key={n} value={n}>{n} {n === 1 ? 'adulto' : 'adultos'}</option>
              ))}
            </select>
          </div>
        </div>

        <button type="submit" className="btn-primary btn-block">Buscar voos</button>
      </form>
    </div>
  );
}
