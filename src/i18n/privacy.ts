import type { Locale } from './types';

export type PrivacyBlock =
  | { type: 'p'; text: string }
  | { type: 'ul'; items: string[] }
  | { type: 'h3'; text: string };

export type PrivacySection = {
  id: string;
  title: string;
  blocks: PrivacyBlock[];
};

export type PrivacyCopy = {
  metaDescription: string;
  title: string;
  eyebrow: string;
  heading: string;
  summary: string;
  effectiveDate: string;
  sections: PrivacySection[];
};

export const privacy: Record<Locale, PrivacyCopy> = {
  en: {
    metaDescription: 'Learn how Plumera Studios handles personal information and protects your privacy.',
    title: 'Privacy — Plumera Studios',
    eyebrow: 'Data privacy',
    heading: 'Privacy at Plumera Studios',
    summary: 'We collect only the information needed to operate our site, understand how it is used, receive feedback, and send updates people have requested.',
    effectiveDate: 'Effective July 22, 2026',
    sections: [
      {
        id: 'who-we-are',
        title: 'Who we are',
        blocks: [
          { type: 'p', text: 'Plumera Studios is responsible for the personal information described in this policy.' },
          { type: 'p', text: 'Questions or privacy requests can be sent to hello@plumerastudios.com.' },
        ],
      },
      {
        id: 'information-we-process',
        title: 'Information we process',
        blocks: [
          { type: 'h3', text: 'Website visits and analytics' },
          { type: 'p', text: 'We use Umami Cloud to understand general site activity. Umami collects information such as pages viewed, referring pages, browser, operating system, device type, and country. It does not use cookies or track people across different websites.' },
          { type: 'p', text: 'An IP address may be processed briefly to determine approximate country-level location, but Umami states that the address is not stored. We do not send names, email addresses, feedback messages, or other directly identifying information to Umami.' },
          { type: 'h3', text: 'Feedback' },
          { type: 'p', text: 'If you submit feedback, we process the message and any reply address you choose to provide. Our AWS infrastructure may also process limited technical information, such as an IP address and request details, to deliver the form and prevent abuse.' },
          { type: 'h3', text: 'Email updates' },
          { type: 'p', text: 'If you ask to receive updates, we process your email address, subscription choice, and related correspondence. We do not track email opens or link clicks, and we do not add feedback addresses to the updates list without a separate request.' },
        ],
      },
      {
        id: 'how-we-use',
        title: 'How we use information',
        blocks: [
          {
            type: 'ul',
            items: [
              'Operate, secure, and improve the website and its tools.',
              'Understand aggregate site usage.',
              'Review and respond to feedback.',
              'Send updates that a recipient has requested.',
              'Prevent spam, fraud, and technical abuse.',
              'Meet legal obligations and protect our rights.',
            ],
          },
          { type: 'p', text: 'We do not sell personal information, use it for behavioral advertising, or build profiles about individual visitors.' },
        ],
      },
      {
        id: 'legal-bases',
        title: 'Legal bases',
        blocks: [
          { type: 'p', text: 'Where the General Data Protection Regulation or similar law applies, we rely on:' },
          {
            type: 'ul',
            items: [
              'Consent to send requested email updates. Consent can be withdrawn at any time.',
              'Legitimate interests to operate and secure the site, measure aggregate usage, receive feedback, respond to requests, and improve our products.',
              'Legal obligations when processing is required by law.',
            ],
          },
        ],
      },
      {
        id: 'cookies',
        title: 'Cookies and browser storage',
        blocks: [
          { type: 'p', text: 'Our analytics does not use cookies. We do not use advertising cookies or cross-site tracking technologies. If a Plumera tool uses local browser storage for a user-requested feature, such as remembering preferences or saved items, that information remains on the device unless the feature clearly says otherwise.' },
        ],
      },
      {
        id: 'providers',
        title: 'Service providers',
        blocks: [
          { type: 'p', text: 'We use a limited number of providers to operate Plumera Studios:' },
          {
            type: 'ul',
            items: [
              'Amazon Web Services for website hosting, content delivery, security, and feedback processing.',
              'Umami Cloud for privacy-focused website analytics.',
              'Email delivery providers to receive messages and send requested replies or updates.',
            ],
          },
          { type: 'p', text: 'These providers process information on our behalf under their applicable data-protection terms. We may also disclose information when legally required or when necessary to protect the security and rights of Plumera Studios or others.' },
        ],
      },
      {
        id: 'transfers',
        title: 'International transfers',
        blocks: [
          { type: 'p', text: 'Our providers may process information in the United States, the European Economic Area, or other locations where they operate. When data-protection law requires safeguards for an international transfer, we use applicable contractual protections or another recognized transfer mechanism.' },
        ],
      },
      {
        id: 'retention',
        title: 'How long we keep information',
        blocks: [
          {
            type: 'ul',
            items: [
              'Aggregate analytics data is retained for up to 12 months.',
              'Feedback and related correspondence are retained for up to 12 months after the matter is resolved.',
              'Update subscription information is retained until the recipient unsubscribes or the list is discontinued.',
              'Operational and security logs are retained for up to 30 days unless a longer period is needed to investigate abuse or meet a legal obligation.',
            ],
          },
          { type: 'p', text: 'Information may be deleted sooner when it is no longer needed.' },
        ],
      },
      {
        id: 'security',
        title: 'Security',
        blocks: [
          { type: 'p', text: 'We use reasonable technical and organizational measures to protect information, including restricted access, encrypted connections, input validation, and controls intended to limit abusive submissions. No system can guarantee absolute security.' },
        ],
      },
      {
        id: 'rights',
        title: 'Your privacy rights',
        blocks: [
          { type: 'p', text: 'Depending on where you live, you may have the right to:' },
          {
            type: 'ul',
            items: [
              'Request access to personal information about you.',
              'Correct inaccurate or incomplete information.',
              'Request deletion or restriction of processing.',
              'Object to processing based on legitimate interests.',
              'Receive portable information where applicable.',
              'Withdraw consent without affecting earlier lawful processing.',
            ],
          },
          { type: 'p', text: 'Send a request to hello@plumerastudios.com. We may need to verify that a request relates to you. People in the EEA or United Kingdom may also complain to their local data-protection authority.' },
        ],
      },
      {
        id: 'children',
        title: 'Children’s privacy',
        blocks: [
          { type: 'p', text: 'Plumera tools may be useful to learners of different ages, but we do not knowingly request personal information from children who cannot provide valid consent under their local law. A child should not submit an email address or feedback without permission from a parent or guardian when that permission is required.' },
        ],
      },
      {
        id: 'changes',
        title: 'Changes to this policy',
        blocks: [
          { type: 'p', text: 'We may update this policy when our services or data practices change. We will post the revised version here and change the effective date at the top of the page.' },
        ],
      },
    ],
  },
  es: {
    metaDescription: 'Conoce cómo Plumera Studios trata la información personal y protege tu privacidad.',
    title: 'Privacidad — Plumera Studios',
    eyebrow: 'Privacidad de los datos',
    heading: 'Privacidad en Plumera Studios',
    summary: 'Recopilamos únicamente la información necesaria para gestionar nuestro sitio, comprender cómo se utiliza, recibir comentarios y enviar las novedades que las personas hayan solicitado.',
    effectiveDate: 'En vigor desde el 22 de julio de 2026',
    sections: [
      {
        id: 'who-we-are',
        title: 'Quiénes somos',
        blocks: [
          { type: 'p', text: 'Plumera Studios es responsable de la información personal descrita en esta política.' },
          { type: 'p', text: 'Las preguntas o solicitudes relacionadas con la privacidad pueden enviarse a hello@plumerastudios.com.' },
        ],
      },
      {
        id: 'information-we-process',
        title: 'Información que tratamos',
        blocks: [
          { type: 'h3', text: 'Visitas al sitio web y analítica' },
          { type: 'p', text: 'Utilizamos Umami Cloud para comprender la actividad general del sitio. Umami recopila información como las páginas visitadas, las páginas de referencia, el navegador, el sistema operativo, el tipo de dispositivo y el país. No utiliza cookies ni rastrea a las personas en distintos sitios web.' },
          { type: 'p', text: 'Podemos tratar brevemente una dirección IP para determinar una ubicación aproximada a nivel de país, pero Umami afirma que no almacena la dirección. No enviamos a Umami nombres, direcciones de correo electrónico, comentarios enviados ni otra información que permita identificar directamente a una persona.' },
          { type: 'h3', text: 'Comentarios' },
          { type: 'p', text: 'Si envías comentarios, tratamos el mensaje y cualquier dirección de respuesta que decidas proporcionar. Nuestra infraestructura de AWS también puede tratar información técnica limitada, como una dirección IP y detalles de la solicitud, para transmitir el formulario y evitar abusos.' },
          { type: 'h3', text: 'Novedades por correo electrónico' },
          { type: 'p', text: 'Si solicitas recibir novedades, tratamos tu dirección de correo electrónico, tu elección de suscripción y la correspondencia relacionada. No rastreamos la apertura de correos electrónicos ni los clics en enlaces, y no añadimos las direcciones proporcionadas para enviar comentarios a la lista de novedades sin una solicitud independiente.' },
        ],
      },
      {
        id: 'how-we-use',
        title: 'Cómo utilizamos la información',
        blocks: [
          {
            type: 'ul',
            items: [
              'Gestionar, proteger y mejorar el sitio web y sus herramientas.',
              'Comprender el uso agregado del sitio.',
              'Revisar los comentarios y responder a ellos.',
              'Enviar las novedades a quien las haya solicitado.',
              'Evitar el spam, el fraude y los abusos técnicos.',
              'Cumplir obligaciones legales y proteger nuestros derechos.',
            ],
          },
          { type: 'p', text: 'No vendemos información personal, no la utilizamos para publicidad conductual ni creamos perfiles de visitantes individuales.' },
        ],
      },
      {
        id: 'legal-bases',
        title: 'Bases jurídicas',
        blocks: [
          { type: 'p', text: 'Cuando sean aplicables el Reglamento General de Protección de Datos o leyes similares, nos basamos en:' },
          {
            type: 'ul',
            items: [
              'El consentimiento para enviar las novedades por correo electrónico solicitadas. El consentimiento puede retirarse en cualquier momento.',
              'Los intereses legítimos para gestionar y proteger el sitio, medir el uso agregado, recibir comentarios, responder a solicitudes y mejorar nuestros productos.',
              'Las obligaciones legales cuando la ley exige el tratamiento.',
            ],
          },
        ],
      },
      {
        id: 'cookies',
        title: 'Cookies y almacenamiento del navegador',
        blocks: [
          { type: 'p', text: 'Nuestro servicio de analítica no utiliza cookies. No utilizamos cookies publicitarias ni tecnologías de rastreo entre sitios. Si una herramienta de Plumera utiliza el almacenamiento local del navegador para una función solicitada por la persona usuaria, como recordar preferencias o elementos guardados, esa información permanece en el dispositivo a menos que la función indique claramente lo contrario.' },
        ],
      },
      {
        id: 'providers',
        title: 'Proveedores de servicios',
        blocks: [
          { type: 'p', text: 'Utilizamos un número limitado de proveedores para gestionar Plumera Studios:' },
          {
            type: 'ul',
            items: [
              'Amazon Web Services para el alojamiento del sitio web, la distribución de contenido, la seguridad y el tratamiento de comentarios.',
              'Umami Cloud para la analítica del sitio web centrada en la privacidad.',
              'Proveedores de servicios de correo electrónico para recibir mensajes y enviar las respuestas o novedades solicitadas.',
            ],
          },
          { type: 'p', text: 'Estos proveedores tratan información en nuestro nombre de acuerdo con las condiciones de protección de datos que les sean aplicables. También podemos divulgar información cuando lo exija la ley o cuando sea necesario para proteger la seguridad y los derechos de Plumera Studios o de otras personas.' },
        ],
      },
      {
        id: 'transfers',
        title: 'Transferencias internacionales',
        blocks: [
          { type: 'p', text: 'Nuestros proveedores pueden tratar información en Estados Unidos, el Espacio Económico Europeo u otros lugares donde operen. Cuando la legislación sobre protección de datos exija garantías para una transferencia internacional, utilizamos las protecciones contractuales aplicables u otro mecanismo de transferencia reconocido.' },
        ],
      },
      {
        id: 'retention',
        title: 'Durante cuánto tiempo conservamos la información',
        blocks: [
          {
            type: 'ul',
            items: [
              'Los datos analíticos agregados se conservan hasta 12 meses.',
              'Los comentarios y la correspondencia relacionada se conservan hasta 12 meses después de que se resuelva el asunto.',
              'La información de suscripción a las novedades se conserva hasta que se cancele la suscripción o se suspenda la lista.',
              'Los registros operativos y de seguridad se conservan hasta 30 días, salvo que sea necesario un periodo más largo para investigar abusos o cumplir una obligación legal.',
            ],
          },
          { type: 'p', text: 'La información puede eliminarse antes cuando ya no sea necesaria.' },
        ],
      },
      {
        id: 'security',
        title: 'Seguridad',
        blocks: [
          { type: 'p', text: 'Utilizamos medidas técnicas y organizativas razonables para proteger la información, como el acceso restringido, las conexiones cifradas, la validación de datos de entrada y controles destinados a limitar los envíos abusivos. Ningún sistema puede garantizar una seguridad absoluta.' },
        ],
      },
      {
        id: 'rights',
        title: 'Tus derechos de privacidad',
        blocks: [
          { type: 'p', text: 'Según el lugar donde vivas, puedes tener derecho a:' },
          {
            type: 'ul',
            items: [
              'Solicitar acceso a la información personal sobre ti.',
              'Corregir información inexacta o incompleta.',
              'Solicitar la eliminación o la limitación del tratamiento.',
              'Oponerte al tratamiento basado en intereses legítimos.',
              'Recibir la información en un formato portátil cuando corresponda.',
              'Retirar el consentimiento sin que ello afecte al tratamiento lícito realizado anteriormente.',
            ],
          },
          { type: 'p', text: 'Envía una solicitud a hello@plumerastudios.com. Es posible que debamos verificar que la solicitud se refiere a ti. Las personas que se encuentren en el EEE o el Reino Unido también pueden presentar una reclamación ante su autoridad local de protección de datos.' },
        ],
      },
      {
        id: 'children',
        title: 'Privacidad infantil',
        blocks: [
          { type: 'p', text: 'Las herramientas de Plumera pueden ser útiles para estudiantes de distintas edades, pero no solicitamos deliberadamente información personal de menores que no puedan prestar un consentimiento válido según la legislación local. Los menores no deben enviar una dirección de correo electrónico ni comentarios sin el permiso de su padre, madre o tutor legal cuando dicho permiso sea necesario.' },
        ],
      },
      {
        id: 'changes',
        title: 'Cambios en esta política',
        blocks: [
          { type: 'p', text: 'Podemos actualizar esta política cuando cambien nuestros servicios o nuestras prácticas relativas a los datos. Publicaremos aquí la versión revisada y cambiaremos la fecha de entrada en vigor que figura en la parte superior de la página.' },
        ],
      },
    ],
  },
  fr: {
    metaDescription: 'Découvrez comment Plumera Studios traite les données personnelles et protège votre vie privée.',
    title: 'Confidentialité — Plumera Studios',
    eyebrow: 'Protection des données',
    heading: 'La confidentialité chez Plumera Studios',
    summary: 'Nous recueillons uniquement les informations nécessaires pour exploiter notre site, comprendre son utilisation, recevoir des commentaires et envoyer les actualités demandées.',
    effectiveDate: 'En vigueur le 22 juillet 2026',
    sections: [
      {
        id: 'who-we-are',
        title: 'Qui sommes-nous ?',
        blocks: [
          { type: 'p', text: 'Plumera Studios est responsable des données à caractère personnel décrites dans la présente politique.' },
          { type: 'p', text: 'Pour toute question ou demande relative à la confidentialité, écrivez à hello@plumerastudios.com.' },
        ],
      },
      {
        id: 'information-we-process',
        title: 'Informations que nous traitons',
        blocks: [
          { type: 'h3', text: 'Visites du site et données d’analyse' },
          { type: 'p', text: 'Nous utilisons Umami Cloud pour comprendre l’activité générale du site. Umami recueille des informations telles que les pages consultées, les pages de provenance, le navigateur, le système d’exploitation, le type d’appareil et le pays. Umami n’utilise pas de cookies et ne suit pas les personnes sur différents sites web.' },
          { type: 'p', text: 'Une adresse IP peut être traitée brièvement afin de déterminer une localisation approximative à l’échelle du pays, mais Umami indique que cette adresse n’est pas conservée. Nous ne transmettons à Umami ni noms, ni adresses e-mail, ni commentaires, ni aucune autre information permettant une identification directe.' },
          { type: 'h3', text: 'Commentaires' },
          { type: 'p', text: 'Si vous envoyez un commentaire, nous traitons son contenu ainsi que toute adresse de réponse que vous choisissez de fournir. Notre infrastructure AWS peut également traiter des informations techniques limitées, telles qu’une adresse IP et les détails de la requête, afin d’acheminer le formulaire et de prévenir les abus.' },
          { type: 'h3', text: 'Actualités par e-mail' },
          { type: 'p', text: 'Si vous demandez à recevoir nos actualités, nous traitons votre adresse e-mail, votre choix d’abonnement et la correspondance associée. Nous ne suivons ni l’ouverture des e-mails ni les clics sur les liens, et nous n’ajoutons pas les adresses fournies avec des commentaires à la liste d’envoi des actualités sans demande distincte.' },
        ],
      },
      {
        id: 'how-we-use',
        title: 'Comment nous utilisons les informations',
        blocks: [
          {
            type: 'ul',
            items: [
              'Exploiter, sécuriser et améliorer le site web et ses outils.',
              'Comprendre l’utilisation globale du site.',
              'Examiner les commentaires et y répondre.',
              'Envoyer les actualités demandées par leur destinataire.',
              'Prévenir le spam, la fraude et les abus techniques.',
              'Respecter nos obligations légales et protéger nos droits.',
            ],
          },
          { type: 'p', text: 'Nous ne vendons pas de données à caractère personnel, ne les utilisons pas à des fins de publicité comportementale et n’établissons pas de profils sur les visiteurs individuels.' },
        ],
      },
      {
        id: 'legal-bases',
        title: 'Bases juridiques',
        blocks: [
          { type: 'p', text: 'Lorsque le Règlement général sur la protection des données ou une législation similaire s’applique, nous nous appuyons sur les bases suivantes :' },
          {
            type: 'ul',
            items: [
              'Le consentement pour envoyer les actualités demandées par e-mail. Le consentement peut être retiré à tout moment.',
              'Les intérêts légitimes pour exploiter et sécuriser le site, mesurer son utilisation globale, recevoir des commentaires, répondre aux demandes et améliorer nos produits.',
              'Les obligations légales lorsque le traitement est exigé par la loi.',
            ],
          },
        ],
      },
      {
        id: 'cookies',
        title: 'Cookies et stockage dans le navigateur',
        blocks: [
          { type: 'p', text: 'Notre outil d’analyse n’utilise pas de cookies. Nous n’utilisons ni cookies publicitaires ni technologies de suivi entre différents sites. Si un outil Plumera utilise le stockage local du navigateur pour une fonctionnalité demandée par l’utilisateur, par exemple pour mémoriser des préférences ou des éléments enregistrés, ces informations restent sur l’appareil, sauf indication contraire explicite de la fonctionnalité.' },
        ],
      },
      {
        id: 'providers',
        title: 'Prestataires de services',
        blocks: [
          { type: 'p', text: 'Nous faisons appel à un nombre limité de prestataires pour exploiter Plumera Studios :' },
          {
            type: 'ul',
            items: [
              'Amazon Web Services pour l’hébergement du site web, la diffusion de contenu, la sécurité et le traitement des commentaires.',
              'Umami Cloud pour l’analyse du site web respectueuse de la vie privée.',
              'Des prestataires de messagerie électronique pour recevoir des messages et envoyer les réponses ou actualités demandées.',
            ],
          },
          { type: 'p', text: 'Ces prestataires traitent les informations pour notre compte conformément aux conditions de protection des données qui leur sont applicables. Nous pouvons également divulguer des informations lorsque la loi l’exige ou lorsque cela est nécessaire pour protéger la sécurité et les droits de Plumera Studios ou de tiers.' },
        ],
      },
      {
        id: 'transfers',
        title: 'Transferts internationaux',
        blocks: [
          { type: 'p', text: 'Nos prestataires peuvent traiter des informations aux États-Unis, dans l’Espace économique européen ou dans d’autres territoires où ils exercent leurs activités. Lorsque la législation sur la protection des données exige des garanties pour un transfert international, nous recourons aux protections contractuelles applicables ou à un autre mécanisme de transfert reconnu.' },
        ],
      },
      {
        id: 'retention',
        title: 'Durée de conservation des informations',
        blocks: [
          {
            type: 'ul',
            items: [
              'Les données d’analyse agrégées sont conservées pendant une durée maximale de 12 mois.',
              'Les commentaires et la correspondance associée sont conservés pendant une durée maximale de 12 mois après la résolution de la question.',
              'Les informations relatives à l’abonnement aux actualités sont conservées jusqu’à ce que le destinataire se désabonne ou que la liste soit supprimée.',
              'Les journaux d’exploitation et de sécurité sont conservés pendant une durée maximale de 30 jours, sauf si une période plus longue est nécessaire pour enquêter sur un abus ou respecter une obligation légale.',
            ],
          },
          { type: 'p', text: 'Les informations peuvent être supprimées plus tôt lorsqu’elles ne sont plus nécessaires.' },
        ],
      },
      {
        id: 'security',
        title: 'Sécurité',
        blocks: [
          { type: 'p', text: 'Nous mettons en œuvre des mesures techniques et organisationnelles raisonnables pour protéger les informations, notamment un accès restreint, des connexions chiffrées, la validation des données saisies et des contrôles visant à limiter les envois abusifs. Aucun système ne peut garantir une sécurité absolue.' },
        ],
      },
      {
        id: 'rights',
        title: 'Vos droits en matière de confidentialité',
        blocks: [
          { type: 'p', text: 'Selon votre lieu de résidence, vous pouvez avoir le droit de :' },
          {
            type: 'ul',
            items: [
              'Demander l’accès aux données à caractère personnel vous concernant.',
              'Rectifier les informations inexactes ou incomplètes.',
              'Demander l’effacement des informations ou la limitation de leur traitement.',
              'Vous opposer au traitement fondé sur des intérêts légitimes.',
              'Recevoir les informations dans un format portable, le cas échéant.',
              'Retirer votre consentement sans porter atteinte à la licéité du traitement antérieur.',
            ],
          },
          { type: 'p', text: 'Envoyez votre demande à hello@plumerastudios.com. Nous pouvons être amenés à vérifier qu’une demande vous concerne. Les personnes résidant dans l’EEE ou au Royaume-Uni peuvent également introduire une réclamation auprès de leur autorité locale de protection des données.' },
        ],
      },
      {
        id: 'children',
        title: 'Confidentialité des enfants',
        blocks: [
          { type: 'p', text: 'Les outils Plumera peuvent être utiles aux apprenants de différents âges, mais nous ne demandons pas sciemment de données à caractère personnel aux enfants qui ne peuvent pas donner un consentement valable en vertu de leur législation locale. Un enfant ne doit pas fournir d’adresse e-mail ni envoyer de commentaire sans l’autorisation d’un parent ou d’un tuteur lorsque cette autorisation est requise.' },
        ],
      },
      {
        id: 'changes',
        title: 'Modifications de la présente politique',
        blocks: [
          { type: 'p', text: 'Nous pouvons mettre à jour la présente politique lorsque nos services ou nos pratiques en matière de données évoluent. Nous publierons ici la version révisée et modifierons la date d’entrée en vigueur figurant en haut de la page.' },
        ],
      },
    ],
  },
};
