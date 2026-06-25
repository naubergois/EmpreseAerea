import { createContext, useContext, useState } from 'react';

const BookingContext = createContext(null);

export function BookingProvider({ children }) {
  const [search, setSearch] = useState(null);
  const [selectedFlight, setSelectedFlight] = useState(null);
  const [pricing, setPricing] = useState(null);
  const [reservation, setReservation] = useState(null);
  const [payment, setPayment] = useState(null);
  const [confirmation, setConfirmation] = useState(null);

  return (
    <BookingContext.Provider value={{
      search, setSearch,
      selectedFlight, setSelectedFlight,
      pricing, setPricing,
      reservation, setReservation,
      payment, setPayment,
      confirmation, setConfirmation,
    }}>
      {children}
    </BookingContext.Provider>
  );
}

export function useBooking() {
  const ctx = useContext(BookingContext);
  if (!ctx) throw new Error('useBooking must be used within BookingProvider');
  return ctx;
}
