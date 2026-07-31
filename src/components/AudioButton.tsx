import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';

interface AudioButtonProps {
  src: string;
  label: string;
  onPlayed?: () => void;
}

export type AudioButtonHandle = {
  play: () => void;
};

const AudioButton = forwardRef<AudioButtonHandle, AudioButtonProps>(function AudioButton(
  { src, label, onPlayed },
  ref,
) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    const audio = new Audio(src);
    audioRef.current = audio;

    const onEnded = () => setPlaying(false);
    const onPause = () => setPlaying(false);
    audio.addEventListener('ended', onEnded);
    audio.addEventListener('pause', onPause);

    return () => {
      audio.pause();
      audio.removeEventListener('ended', onEnded);
      audio.removeEventListener('pause', onPause);
      audioRef.current = null;
    };
  }, [src]);

  const play = () => {
    const audio = audioRef.current;
    if (!audio) return;
    audio.currentTime = 0;
    void audio
      .play()
      .then(() => {
        setPlaying(true);
        onPlayed?.();
      })
      .catch(() => setPlaying(false));
  };

  useImperativeHandle(ref, () => ({ play }), [onPlayed]);

  return (
    <button
      type="button"
      className={playing ? 'audio-button is-playing' : 'audio-button'}
      onClick={play}
      aria-label={`Play pronunciation: ${label}`}
    >
      <span aria-hidden="true">♪</span>
    </button>
  );
});

export default AudioButton;
