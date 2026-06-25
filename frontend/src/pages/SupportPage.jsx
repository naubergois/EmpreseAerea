import { useState, useRef, useEffect } from 'react';
import { enviarChat } from '../api/atendimentoApi';

export default function SupportPage() {
  const [mensagem, setMensagem] = useState('');
  const [pnr, setPnr] = useState('');
  const [historico, setHistorico] = useState([]);
  const [protocolo, setProtocolo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);
  const fimRef = useRef(null);

  useEffect(() => {
    fimRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [historico]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!mensagem.trim()) return;
    setLoading(true);
    setErro(null);
    const msgUsuario = mensagem.trim();
    setHistorico((h) => [...h, { role: 'user', text: msgUsuario }]);
    setMensagem('');

    try {
      const data = await enviarChat({
        mensagem: msgUsuario,
        canal: 'chat',
        pnr: pnr.trim() || undefined,
      });
      setProtocolo(data.protocolo);
      setHistorico((h) => [...h, {
        role: 'assistant',
        text: data.resposta,
        sentimento: data.sentimento,
        escalado: data.escalado,
      }]);
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Erro ao conectar com o suporte';
      setErro(msg);
      setHistorico((h) => [...h, { role: 'error', text: msg }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: 640, display: 'flex', flexDirection: 'column', minHeight: 480 }}>
      <h2>Suporte SkyAgent</h2>
      <p style={{ color: '#6b7280', fontSize: '0.875rem', marginBottom: '1rem' }}>
        Assistente com IA — tire dúvidas sobre reservas, bagagem, cancelamento e milhas.
      </p>

      {protocolo && (
        <p style={{ fontSize: '0.8rem', color: '#0066cc', marginBottom: '0.75rem' }}>
          Protocolo: <strong>{protocolo}</strong>
        </p>
      )}

      <div style={{
        flex: 1, overflowY: 'auto', maxHeight: 320, marginBottom: '1rem',
        border: '1px solid #e5e7eb', borderRadius: 8, padding: '0.75rem',
        background: '#fafafa',
      }}>
        {historico.length === 0 && (
          <p style={{ color: '#9ca3af', fontSize: '0.875rem' }}>
            Exemplo: &quot;Qual a política de bagagem?&quot; ou &quot;Quero cancelar minha reserva&quot;
          </p>
        )}
        {historico.map((item, i) => (
          <div key={i} style={{
            marginBottom: '0.75rem',
            textAlign: item.role === 'user' ? 'right' : 'left',
          }}>
            <div style={{
              display: 'inline-block',
              padding: '0.6rem 0.9rem',
              borderRadius: 12,
              maxWidth: '85%',
              background: item.role === 'user' ? '#0066cc' : item.role === 'error' ? '#fef2f2' : '#fff',
              color: item.role === 'user' ? '#fff' : item.role === 'error' ? '#b91c1c' : '#1a1a2e',
              border: item.role === 'assistant' ? '1px solid #e5e7eb' : 'none',
              whiteSpace: 'pre-wrap',
              fontSize: '0.9rem',
            }}>
              {item.text}
            </div>
            {item.escalado && (
              <div style={{ fontSize: '0.75rem', color: '#b45309', marginTop: 4 }}>
                Encaminhado para atendente humano
              </div>
            )}
          </div>
        ))}
        {loading && <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>Digitando...</p>}
        <div ref={fimRef} />
      </div>

      {erro && <div className="alert alert-error" style={{ marginBottom: '0.75rem' }}>{erro}</div>}

      <form onSubmit={handleSend}>
        <input
          placeholder="PNR (opcional, ex: ABC123)"
          value={pnr}
          onChange={(e) => setPnr(e.target.value.toUpperCase())}
          maxLength={6}
          style={{ marginBottom: '0.5rem' }}
        />
        <textarea
          value={mensagem}
          onChange={(e) => setMensagem(e.target.value)}
          placeholder="Digite sua mensagem..."
          rows={3}
          style={{ width: '100%', padding: '0.75rem', borderRadius: 8, border: '1px solid #e5e7eb', marginBottom: '0.75rem', resize: 'vertical' }}
          disabled={loading}
        />
        <button type="submit" className="btn-primary" disabled={loading || !mensagem.trim()}>
          {loading ? 'Enviando...' : 'Enviar'}
        </button>
      </form>
    </div>
  );
}
