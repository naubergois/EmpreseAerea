import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useBooking } from '../context/BookingContext';

export default function HomePage() {
  const navigate = useNavigate();
  const { setSearch } = useBooking();
  const [form, setForm] = useState({
    origem: 'GRU', destino: 'GIG', data_ida: '2026-08-15', classe: 'economica', adultos: 1,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setSearch(form);
    const params = new URLSearchParams(form);
    navigate(`/resultados?${params}`);
  };

  return (
    <div>
      <section style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>Encontre seu próximo voo</h1>
        <p style={{ color: '#6b7280' }}>Busca inteligente com precificação dinâmica e milhas</p>
      </section>
      <form className="card" onSubmit={handleSubmit} style={{ maxWidth: 800, margin: '0 auto' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <label>Origem</label>
            <input value={form.origem} onChange={(e) => setForm({ ...form, origem: e.target.value })} placeholder="GRU" />
          </div>
          <div>
            <label>Destino</label>
            <input value={form.destino} onChange={(e) => setForm({ ...form, destino: e.target.value })} placeholder="GIG" />
          </div>
          <div>
            <label>Data ida</label>
            <input type="date" value={form.data_ida} onChange={(e) => setForm({ ...form, data_ida: e.target.value })} />
          </div>
          <div>
            <label>Classe</label>
            <select value={form.classe} onChange={(e) => setForm({ ...form, classe: e.target.value })}>
              <option value="economica">Econômica</option>
              <option value="executiva">Executiva</option>
            </select>
          </div>
        </div>
        <button type="submit" className="btn-primary" style={{ width: '100%' }}>Buscar Voos</button>
      </form>
    </div>
  );
}
