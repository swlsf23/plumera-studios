import type { Locale } from './types';

export type ChromeCopy = {
  brandHome: string;
  home: string;
  votd: string;
  updates: string;
  privacy: string;
  subscribe: string;
  search: string;
  toggleNav: string;
  chooseLanguage: string;
  languages: string;
  explore: string;
  connect: string;
  newsletter: string;
  onThisPage: string;
  relatedVotd: string;
  followUs: string;
  tagline: string;
  copyright: string;
};

export const chrome: Record<Locale, ChromeCopy> = {
  en: {
    brandHome: 'Plumera home',
    home: 'Home',
    votd: 'VOTD',
    updates: 'Updates',
    privacy: 'Privacy',
    subscribe: 'Subscribe',
    search: 'Search',
    toggleNav: 'Toggle navigation',
    chooseLanguage: 'Choose language',
    languages: 'Languages',
    explore: 'Explore',
    connect: 'Connect',
    newsletter: 'Newsletter',
    onThisPage: 'On this page',
    relatedVotd: 'Related VOTD',
    followUs: 'Follow us:',
    tagline: 'Language tools.\nWord games.\nLanguage learning.',
    copyright: '© 2026 Plumera Studios',
  },
  es: {
    brandHome: 'Inicio de Plumera',
    home: 'Inicio',
    votd: 'VOTD',
    updates: 'Novedades',
    privacy: 'Privacidad',
    subscribe: 'Suscribirse',
    search: 'Buscar',
    toggleNav: 'Abrir o cerrar navegación',
    chooseLanguage: 'Elegir idioma',
    languages: 'Idiomas',
    explore: 'Explorar',
    connect: 'Conectar',
    newsletter: 'Boletín',
    onThisPage: 'En esta página',
    relatedVotd: 'VOTD relacionados',
    followUs: 'Síguenos:',
    tagline: 'Herramientas lingüísticas.\nJuegos de palabras.\nAprendizaje de idiomas.',
    copyright: '© 2026 Plumera Studios',
  },
  fr: {
    brandHome: 'Accueil Plumera',
    home: 'Accueil',
    votd: 'VOTD',
    updates: 'Actualités',
    privacy: 'Confidentialité',
    subscribe: 'S’abonner',
    search: 'Rechercher',
    toggleNav: 'Ouvrir ou fermer la navigation',
    chooseLanguage: 'Choisir la langue',
    languages: 'Langues',
    explore: 'Explorer',
    connect: 'Connexion',
    newsletter: 'Infolettre',
    onThisPage: 'Sur cette page',
    relatedVotd: 'VOTD associés',
    followUs: 'Suivez-nous :',
    tagline: 'Outils linguistiques.\nJeux de lettres.\nApprentissage des langues.',
    copyright: '© 2026 Plumera Studios',
  },
};
