import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
/* Site chrome (base.css, content-header.css) loads from the HTML shell, same as content pages. */
import './styles/practice.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
