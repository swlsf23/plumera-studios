import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
/* Same site chrome CSS as content pages (bundled so /app/flashcard/ base does not rewrite paths). */
import '../public/css/base.css';
import '../public/css/content-header.css';
import './styles/practice.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
