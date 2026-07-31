import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import PracticePage from './pages/PracticePage';

const BASENAME = '/app/flashcard';

/**
 * Flashcard app, served under /app/flashcard/ as part of the static site dist/.
 */
export default function App() {
  return (
    <BrowserRouter basename={BASENAME}>
      <Routes>
        <Route path="/" element={<Navigate to="/prendre/" replace />} />
        <Route path="/:verb/" element={<PracticePage />} />
        <Route path="/:verb" element={<PracticePage />} />
        <Route path="*" element={<Navigate to="/prendre/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
