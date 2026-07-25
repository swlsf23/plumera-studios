import {
  ArrowLeft,
  Leaf,
  Link2,
  MessageCircle,
  UserRound,
  X,
} from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { AppShell } from '../components/layout/AppShell';
import { PageSidebar } from '../components/layout/PageSidebar';
import { useActiveSection } from '../hooks/useActiveSection';
import { useDocumentMeta } from '../hooks/useDocumentMeta';
import type { Locale } from '../i18n/types';
import { votdPath } from '../lib/paths';

type Section = {
  id: string;
  label: string;
};

const sections: Section[] = [
  { id: 'introduction', label: 'Introduction' },
  { id: 'why-it-matters', label: 'Why thoughtful content matters' },
  { id: 'principles', label: 'Principles that guide us' },
  { id: 'looking-ahead', label: 'Looking ahead' },
];

type Props = {
  locale: Locale;
};

function HeroArtwork() {
  return (
    <div className="hero-art" aria-hidden="true">
      <div className="hero-art__arc" />
      <div className="hero-art__panel">
        <span className="hero-art__shape hero-art__shape--circle" />
        <span className="hero-art__shape hero-art__shape--bar" />
        <span className="hero-art__shape hero-art__shape--dot" />
      </div>
    </div>
  );
}

function PrincipleCard({ icon, title, text }: { icon: React.ReactNode; title: string; text: string }) {
  return (
    <article className="principle-card">
      <div className="principle-card__icon">{icon}</div>
      <h3>{title}</h3>
      <p>{text}</p>
    </article>
  );
}

export function ArticlePage({ locale }: Props) {
  const { slug = 'thoughtful-content' } = useParams();
  const activeSection = useActiveSection(sections.map((section) => section.id));

  useDocumentMeta(
    locale,
    'The future of thoughtful content — Plumera Studios',
    'Exploring how meaningful content builds trust, drives engagement, and creates lasting impact.',
    votdPath(locale, slug),
  );

  return (
    <AppShell
      locale={locale}
      active="votd"
      sidebar={<PageSidebar locale={locale} sections={sections} activeSection={activeSection} />}
    >
      <header className="article-header">
        <p className="eyebrow">Category</p>
        <h1>
          The future of
          <br />
          thoughtful content
        </h1>
        <p className="dek">
          Exploring how meaningful content builds trust, drives engagement, and creates lasting impact.
        </p>
        <div className="byline">
          <div>
            <strong>By Plumera Team</strong>
            <span>May 12, 2024 · 8 min read</span>
          </div>
        </div>
      </header>

      <HeroArtwork />

      <article className="article-body">
        <section id="introduction" className="article-section">
          <h2>Introduction</h2>
          <p>
            In a world overflowing with noise, thoughtful content stands out. It is not just about publishing more—it is about saying what matters.
          </p>
          <p>
            At Plumera, we believe the future belongs to content that informs, inspires, and builds real connections.
          </p>
        </section>

        <section id="why-it-matters" className="article-section">
          <h2>Why thoughtful content matters</h2>
          <p>
            Thoughtful content goes beyond surface-level engagement. It creates value for both readers and brands.
          </p>
          <ul className="feature-list">
            <li><strong>Builds trust</strong><span>Honest, helpful content earns credibility.</span></li>
            <li><strong>Drives engagement</strong><span>Readers stay longer and come back.</span></li>
            <li><strong>Creates impact</strong><span>Shareable ideas lead to real-world change.</span></li>
          </ul>
        </section>

        <section id="principles" className="article-section">
          <h2>Principles that guide us</h2>
          <p>Our approach is grounded in a few simple principles that shape everything we publish.</p>
          <div className="principles-grid">
            <PrincipleCard
              icon={<UserRound size={25} strokeWidth={1.55} />}
              title="Human first"
              text="We write for people, not algorithms."
            />
            <PrincipleCard
              icon={<Leaf size={25} strokeWidth={1.55} />}
              title="Substance over hype"
              text="We focus on depth, not clickbait."
            />
            <PrincipleCard
              icon={<MessageCircle size={25} strokeWidth={1.55} />}
              title="Open & clear"
              text="We communicate with clarity and honesty."
            />
          </div>
        </section>

        <section id="looking-ahead" className="article-section">
          <h2>Looking ahead</h2>
          <p>
            The future of content is not about more—it is about meaning. We are here to create it, together.
          </p>
        </section>

        <div className="article-end">
          <Link to={votdPath(locale)} className="back-link">
            <ArrowLeft size={17} /> Back to VOTD
          </Link>
          <div className="share-row">
            <span>Share this article</span>
            <button aria-label="Share on X" type="button"><X size={16} /></button>
            <button aria-label="Share on LinkedIn" type="button"><span className="linkedin-glyph">in</span></button>
            <button aria-label="Copy link" type="button"><Link2 size={16} /></button>
          </div>
        </div>
      </article>
    </AppShell>
  );
}
