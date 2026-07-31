/** Site URL for a deck-relative audio path under data/ (copied into dist at build). */
export function resolveAudioUrl(
  audioPath: string | undefined,
  locale: string | undefined,
  target: string | undefined,
): string | null {
  if (!audioPath || !locale || !target) return null;
  const relative = audioPath.replace(/^\/+/, '');
  return `/data/${locale}/${target}/${relative}`;
}
