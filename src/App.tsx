import { BrowserRouter, Navigate, Route, Routes, useParams } from 'react-router-dom';
import { isLocale, type Locale } from './i18n/types';
import { ArticlePage } from './pages/ArticlePage';
import { PrivacyPage } from './pages/PrivacyPage';
import { UpdatesPage } from './pages/UpdatesPage';

function LocaleUpdates() {
  const { locale } = useParams();
  if (!isLocale(locale)) return <Navigate to="/en/updates.html" replace />;
  return <UpdatesPage locale={locale} />;
}

function LocalePrivacy() {
  const { locale } = useParams();
  if (!isLocale(locale)) return <Navigate to="/en/privacy.html" replace />;
  return <PrivacyPage locale={locale} />;
}

function LocaleVotd() {
  const { locale } = useParams();
  if (!isLocale(locale)) return <Navigate to="/en/votd/thoughtful-content" replace />;
  return <ArticlePage locale={locale as Locale} />;
}

function RootRedirect() {
  window.location.replace('/en/index.html');
  return null;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<RootRedirect />} />

        <Route path="/:locale/updates.html" element={<LocaleUpdates />} />
        <Route path="/:locale/updates" element={<LocaleUpdates />} />
        <Route path="/:locale/privacy.html" element={<LocalePrivacy />} />
        <Route path="/:locale/privacy" element={<LocalePrivacy />} />
        <Route path="/:locale/votd/:slug" element={<LocaleVotd />} />
        <Route path="/:locale/votd" element={<Navigate to="thoughtful-content" replace />} />

        <Route path="*" element={<RootRedirect />} />
      </Routes>
    </BrowserRouter>
  );
}
