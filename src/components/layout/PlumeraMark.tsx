type Props = {
  compact?: boolean;
};

export function PlumeraMark({ compact = false }: Props) {
  return (
    <div className={`brand ${compact ? 'brand--compact' : ''}`}>
      <span className="brand__name">Plumera</span>
    </div>
  );
}
