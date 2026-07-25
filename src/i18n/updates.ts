import type { Locale } from './types';

export type UpdatesCopy = {
  metaDescription: string;
  title: string;
  eyebrow: string;
  heading: string;
  headingAccent: string;
  intro: string;
  signupTitle: string;
  signupBeforeSubject: string;
  signupSubject: string;
  signupAfterSubject: string;
  emailAria: string;
  emailAt: string;
  emailDot: string;
  signupNote: string;
  receiveTitle: string;
  receiveItems: string[];
  promiseTitle: string;
  promiseBody: string[];
};

export const updates: Record<Locale, UpdatesCopy> = {
  en: {
    metaDescription: 'Get occasional, privacy-respecting updates from Plumera Studios.',
    title: 'Updates — Plumera Studios',
    eyebrow: 'Plumera updates',
    heading: 'Useful updates.',
    headingAccent: 'No inbox noise.',
    intro: 'Hear about new language tools, learning resources, word games, and meaningful Plumera Studios releases.',
    signupTitle: 'Updates by email',
    signupBeforeSubject: 'Send a short note with',
    signupSubject: 'Updates',
    signupAfterSubject: 'in the subject line to:',
    emailAria: 'hello at plumerastudios dot com',
    emailAt: 'at',
    emailDot: 'dot',
    signupNote: 'We’ll reply to confirm that you want to be included.',
    receiveTitle: 'What you’ll receive',
    receiveItems: [
      'New product releases',
      'Significant tools and resources',
      'Occasional studio updates',
    ],
    promiseTitle: 'Our promise',
    promiseBody: [
      'We don’t track email opens or link clicks. We don’t share your information, and we won’t fill your inbox with routine promotional email.',
      'Ask to be removed at any time.',
    ],
  },
  es: {
    metaDescription: 'Recibe novedades ocasionales de Plumera Studios que respetan tu privacidad.',
    title: 'Novedades — Plumera Studios',
    eyebrow: 'Novedades de Plumera',
    heading: 'Novedades útiles.',
    headingAccent: 'Sin ruido en tu bandeja de entrada.',
    intro: 'Infórmate sobre nuevas herramientas lingüísticas, recursos de aprendizaje, juegos de palabras y lanzamientos importantes de Plumera Studios.',
    signupTitle: 'Novedades por correo electrónico',
    signupBeforeSubject: 'Envía una nota breve con',
    signupSubject: 'Novedades',
    signupAfterSubject: 'en el asunto a:',
    emailAria: 'hello arroba plumerastudios punto com',
    emailAt: 'arroba',
    emailDot: 'punto',
    signupNote: 'Te responderemos para confirmar que deseas recibirlas.',
    receiveTitle: 'Qué recibirás',
    receiveItems: [
      'Lanzamientos de nuevos productos',
      'Herramientas y recursos importantes',
      'Novedades ocasionales del estudio',
    ],
    promiseTitle: 'Nuestro compromiso',
    promiseBody: [
      'No rastreamos la apertura de correos electrónicos ni los clics en enlaces. No compartimos tu información y no llenaremos tu bandeja de entrada con correos promocionales habituales.',
      'Puedes pedir que te eliminemos de la lista en cualquier momento.',
    ],
  },
  fr: {
    metaDescription: 'Recevez des actualités occasionnelles de Plumera Studios, dans le respect de votre vie privée.',
    title: 'Actualités — Plumera Studios',
    eyebrow: 'Actualités de Plumera',
    heading: 'Des actualités utiles.',
    headingAccent: 'Sans encombrer votre boîte de réception.',
    intro: 'Découvrez les nouveaux outils linguistiques, les ressources pédagogiques, les jeux de lettres et les lancements marquants de Plumera Studios.',
    signupTitle: 'Actualités par e-mail',
    signupBeforeSubject: 'Envoyez un court message avec',
    signupSubject: 'Actualités',
    signupAfterSubject: 'en objet à l’adresse suivante :',
    emailAria: 'hello arobase plumerastudios point com',
    emailAt: 'arobase',
    emailDot: 'point',
    signupNote: 'Nous vous répondrons pour confirmer que vous souhaitez être ajouté à la liste.',
    receiveTitle: 'Ce que vous recevrez',
    receiveItems: [
      'Les lancements de nouveaux produits',
      'Des outils et ressources majeurs',
      'Des nouvelles occasionnelles du studio',
    ],
    promiseTitle: 'Notre engagement',
    promiseBody: [
      'Nous ne suivons ni l’ouverture des e-mails ni les clics sur les liens. Nous ne partageons pas vos informations et nous n’encombrerons pas votre boîte de réception d’e-mails promotionnels à répétition.',
      'Vous pouvez demander à être retiré de la liste à tout moment.',
    ],
  },
};
