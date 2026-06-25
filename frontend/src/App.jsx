import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { BookingProvider } from './context/BookingContext';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import HomePage from './pages/HomePage';
import SearchResultsPage from './pages/SearchResultsPage';
import BookingPage from './pages/BookingPage';
import PaymentPage from './pages/PaymentPage';
import ConfirmationPage from './pages/ConfirmationPage';
import LoyaltyPage from './pages/LoyaltyPage';
import SupportPage from './pages/SupportPage';
import './App.css';

export default function App() {
  return (
    <BookingProvider>
      <BrowserRouter>
        <div className="app">
          <Header />
          <main className="app__main">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/resultados" element={<SearchResultsPage />} />
              <Route path="/reserva" element={<BookingPage />} />
              <Route path="/pagamento" element={<PaymentPage />} />
              <Route path="/confirmacao" element={<ConfirmationPage />} />
              <Route path="/fidelidade" element={<LoyaltyPage />} />
              <Route path="/suporte" element={<SupportPage />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </BookingProvider>
  );
}
