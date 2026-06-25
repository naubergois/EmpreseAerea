import FlightCard from './FlightCard';

export default function FlightList({ flights, onSelect }) {
  if (!flights.length) return null;
  return (
    <div>
      {flights.map((f) => (
        <FlightCard key={f.id} flight={f} onSelect={onSelect} />
      ))}
    </div>
  );
}
