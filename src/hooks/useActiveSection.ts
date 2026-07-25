import { useEffect, useState } from 'react';

export function useActiveSection(sectionIds: readonly string[]) {
  const key = sectionIds.join('|');
  const [activeSection, setActiveSection] = useState(sectionIds[0] ?? '');

  useEffect(() => {
    const ids = key ? key.split('|') : [];
    if (ids.length === 0) return;

    setActiveSection(ids[0]);

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible?.target.id) setActiveSection(visible.target.id);
      },
      { rootMargin: '-18% 0px -68% 0px', threshold: [0.05, 0.2, 0.45] },
    );

    ids.forEach((id) => {
      const node = document.getElementById(id);
      if (node) observer.observe(node);
    });

    return () => observer.disconnect();
  }, [key]);

  return activeSection;
}
