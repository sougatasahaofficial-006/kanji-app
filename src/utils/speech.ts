let currentAudio: HTMLAudioElement | null = null;

export function speakJapanese(
  text: string,
  voiceGender: 'male' | 'female' = 'male',
  itemId?: string
) {
  if (typeof window === 'undefined') return;

  if (currentAudio) {
    currentAudio.pause();
    currentAudio = null;
  }
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }

  // 1. Play bundled offline MP3 if itemId is provided (works on all Android/PC devices without OS voice packs)
  if (itemId) {
    const audio = new Audio(`/audio/${itemId}-${voiceGender}.mp3`);
    currentAudio = audio;
    audio.play().catch(() => {
      fallbackSpeechSynthesis(text, voiceGender);
    });
    return;
  }

  // 2. Fallback to device SpeechSynthesis
  fallbackSpeechSynthesis(text, voiceGender);
}

function fallbackSpeechSynthesis(text: string, voiceGender: 'male' | 'female') {
  if (!text || !('speechSynthesis' in window)) return;
  const voices = window.speechSynthesis
    .getVoices()
    .filter((v) => v.lang.toLowerCase().includes('ja'));

  if (voices.length === 0) return;

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'ja-JP';
  utterance.rate = 0.88;
  utterance.pitch = voiceGender === 'female' ? 1.12 : 0.88;
  utterance.voice = voices[0];
  window.speechSynthesis.speak(utterance);
}