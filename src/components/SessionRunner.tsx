import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { X, Settings, Volume2 } from 'lucide-react';
import type { AppSettings, KanjiLessonItem } from '../types/kanji';
import { KanjiCanvas } from './KanjiCanvas';
import { speakJapanese as playJpVoice } from '../utils/speech';

type CardType =
  | 'memorize'
  | 'write-hinted'
  | 'write-unhinted'
  | 'mcq-kanji-to-kana'
  | 'mcq-kanji-kana-to-english'
  | 'mcq-english-to-kana';

interface QuestionCard {
  id: string;
  item: KanjiLessonItem;
  type: CardType;
  choices?: string[];
  correctAnswer?: string;
}

interface SessionRunnerProps {
  items: KanjiLessonItem[];
  allPoolItems: KanjiLessonItem[]; // Used to generate realistic MCQ distractors
  settings: AppSettings;
  isReviewMode: boolean;
  onOpenSettings: () => void;
  onExit: () => void;
  onItemResult?: (itemId: string, wasCorrect: boolean) => void;
  onSessionComplete: () => void;
}

// Helper to convert Hiragana to Katakana when Kana setting = 'katakana'
function formatKana(hiragana: string, mode: 'hiragana' | 'katakana'): string {
  if (mode === 'hiragana') return hiragana;
  return hiragana.replace(/[\u3041-\u3096]/g, (ch) =>
    String.fromCharCode(ch.charCodeAt(0) + 0x60)
  );
}

function shuffle<T>(arr: T[]): T[] {
  const copy = [...arr];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

export const SessionRunner: React.FC<SessionRunnerProps> = ({
  items,
  allPoolItems,
  settings,
  isReviewMode,
  onOpenSettings,
  onExit,
  onItemResult,
  onSessionComplete,
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAllReadings, setShowAllReadings] = useState(false);
  const [selectedChoice, setSelectedChoice] = useState<string | null>(null);
  const [mistakesByItem, setMistakesByItem] = useState<Record<string, boolean>>({});

  // Build the question queue based on settings.lessonQuestionsPerWord (1–7) and Answer Formats
  const queue = useMemo<QuestionCard[]>(() => {
    const cards: QuestionCard[] = [];
    const pool = allPoolItems.length >= 4 ? allPoolItems : items;

    const pickDistractors = (correct: string, field: 'kana' | 'meaning', count: number) => {
      const rawOptions = Array.from(
        new Set(
          pool
            .map((p) =>
              field === 'kana' ? formatKana(p.kana, settings.kana) : p.meaning
            )
            .filter((val) => val !== correct)
        )
      );
      const picked = shuffle(rawOptions).slice(0, count);
      return shuffle([correct, ...picked]);
    };

    items.forEach((item, idx) => {
      const formattedKana = formatKana(item.kana, settings.kana);

      // 1. In lesson mode, always start with the Memorize flashcard
      if (!isReviewMode) {
        cards.push({
          id: `${item.id}-mem-${idx}`,
          item,
          type: 'memorize',
        });
      }

      // Build drill sequence up to lessonQuestionsPerWord
      const drills: QuestionCard[] = [];

      // Guided writing (if Kanji format is 'writing')
      if (settings.kanjiAnswerFormat === 'writing') {
        drills.push({
          id: `${item.id}-wh-${idx}`,
          item,
          type: isReviewMode ? 'write-unhinted' : 'write-hinted',
        });
      }

      // MCQ 1: Kanji -> Kana (2 choices initially, matching screenshots)
      drills.push({
        id: `${item.id}-mcq1-${idx}`,
        item,
        type: 'mcq-kanji-to-kana',
        correctAnswer: formattedKana,
        choices: pickDistractors(formattedKana, 'kana', 1),
      });

      // MCQ 2: Kanji + Kana -> English meaning (2 choices)
      drills.push({
        id: `${item.id}-mcq2-${idx}`,
        item,
        type: 'mcq-kanji-kana-to-english',
        correctAnswer: item.meaning,
        choices: pickDistractors(item.meaning, 'meaning', 1),
      });

      // MCQ 3: English -> 4 Kana choices
      drills.push({
        id: `${item.id}-mcq3-${idx}`,
        item,
        type: 'mcq-english-to-kana',
        correctAnswer: formattedKana,
        choices: pickDistractors(formattedKana, 'kana', 3),
      });

      // Unhinted freehand writing drill
      if (settings.kanjiAnswerFormat === 'writing') {
        drills.push({
          id: `${item.id}-wu-${idx}`,
          item,
          type: 'write-unhinted',
        });
      }

      const limit = Math.max(1, Math.min(7, settings.lessonQuestionsPerWord));
      cards.push(...drills.slice(0, limit));
    });

    // Interleave cards gently while keeping each word's 'memorize' card before its drills
    return cards;
  }, [items, allPoolItems, settings, isReviewMode]);

  const currentCard = queue[currentIndex];
  const progressPercent = queue.length > 0 ? (currentIndex / queue.length) * 100 : 0;

  const speakJapanese = useCallback(
    (text: string) => {
      playJpVoice(text, settings.voice, currentCard?.item.id);
    },
    [settings.voice, currentCard?.item.id]
  );

  // Auto-play audio when card changes if enabled
  useEffect(() => {
    setSelectedChoice(null);
    setShowAllReadings(false);
    if (
      currentCard &&
      settings.autoPlayAudio &&
      (currentCard.type === 'memorize' ||
        currentCard.type === 'write-hinted' ||
        currentCard.type === 'write-unhinted')
    ) {
      speakJapanese(currentCard.item.kana);
    }
  }, [currentIndex, currentCard, settings.autoPlayAudio, speakJapanese]);

  const advanceNext = () => {
    if (currentIndex + 1 < queue.length) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      // Record SRS result for each unique item in this session
      items.forEach((it) => {
        onItemResult?.(it.id, !mistakesByItem[it.id]);
      });
      onSessionComplete();
    }
  };

  const handleChoiceSelect = (choice: string) => {
    if (selectedChoice || !currentCard?.correctAnswer) return;
    setSelectedChoice(choice);
    const isCorrect = choice === currentCard.correctAnswer;
    if (!isCorrect) {
      setMistakesByItem((prev) => ({ ...prev, [currentCard.item.id]: true }));
    }
    setTimeout(() => {
      advanceNext();
    }, 650);
  };

  if (!currentCard) return null;

  const fontClass = settings.font === 'stylized' ? 'font-serif' : 'font-sans';
  const displayKana = formatKana(currentCard.item.kana, settings.kana);

  return (
    <div className="min-h-screen bg-[#242933] text-white flex flex-col justify-between px-5 py-4 select-none">
      {/* Top Header: Close (X), Red Progress Bar, Settings Gear */}
      <div className="flex items-center gap-4 w-full max-w-lg mx-auto">
        <button
          type="button"
          onClick={onExit}
          aria-label="Exit session"
          className="text-slate-200 hover:text-white p-1"
        >
          <X className="w-7 h-7 stroke-[2.5]" />
        </button>

        <div className="flex-1 h-3.5 bg-[#333A48] rounded-full border border-slate-500/40 overflow-hidden">
          <div
            className="h-full bg-[#F24C4C] rounded-full transition-all duration-300"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        <button
          type="button"
          onClick={onOpenSettings}
          aria-label="Open settings"
          className="text-slate-200 hover:text-white p-1"
        >
          <Settings className="w-6 h-6" />
        </button>
      </div>

      {/* Main Card Content */}
      <div className="flex-1 flex flex-col items-center justify-between w-full max-w-lg mx-auto pt-4 pb-2">
        {/* 1. MEMORIZE FLASHCARD */}
        {currentCard.type === 'memorize' && (
          <>
            <div className="w-full text-left text-slate-300 text-lg">
              Memorize this word...
            </div>

            <div className="flex flex-col items-center text-center my-auto">
              <div className={`text-8xl sm:text-9xl font-normal tracking-wide mb-8 ${fontClass}`}>
                {currentCard.item.word}
              </div>
              <div className={`text-3xl text-slate-300 mb-6 ${fontClass}`}>
                {displayKana}
              </div>
              <div className="text-4xl font-bold text-white mb-8">
                {currentCard.item.meaning}
              </div>

              <button
                type="button"
                onClick={() => setShowAllReadings((v) => !v)}
                className="px-6 py-2 rounded-lg bg-[#3B4252] hover:bg-[#464F62] text-slate-100 text-sm font-medium transition"
              >
                All Readings
              </button>

              {showAllReadings && (
                <div className="mt-4 px-5 py-3 rounded-xl bg-[#2E3440] border border-slate-600/50 text-sm text-slate-200 space-y-1">
                  <div>
                    <span className="text-slate-400">On&apos;yomi: </span>
                    {currentCard.item.onyomi.length > 0
                      ? currentCard.item.onyomi.join('、 ')
                      : '—'}
                  </div>
                  <div>
                    <span className="text-slate-400">Kun&apos;yomi: </span>
                    {currentCard.item.kunyomi.length > 0
                      ? currentCard.item.kunyomi.join('、 ')
                      : '—'}
                  </div>
                </div>
              )}

              <button
                type="button"
                onClick={() => speakJapanese(currentCard.item.kana)}
                aria-label="Play audio"
                className="mt-7 w-14 h-14 rounded-full bg-[#5DA9E9] hover:bg-[#4A96D6] flex items-center justify-center text-white shadow-md transition"
              >
                <Volume2 className="w-7 h-7 fill-white" />
              </button>
            </div>

            <button
              type="button"
              onClick={advanceNext}
              className="w-full py-3.5 rounded-xl bg-[#2ECC71] hover:bg-[#27AE60] text-white font-semibold text-lg shadow-md transition"
            >
              OK
            </button>
          </>
        )}

        {/* 2. WRITING DRILLS (Hinted & Unhinted) */}
        {(currentCard.type === 'write-hinted' || currentCard.type === 'write-unhinted') && (
          <>
            <div className="w-full text-left text-slate-300 text-lg">
              Write this word...
            </div>

            <div className="flex flex-col items-center my-auto w-full">
              <div className="text-4xl font-bold text-white mb-2">
                {currentCard.item.meaning}
              </div>
              <div className={`text-3xl text-slate-300 mb-6 ${fontClass}`}>
                {displayKana}
              </div>

              <KanjiCanvas
                characters={currentCard.item.characters}
                initialHinted={currentCard.type === 'write-hinted'}
                showGuideLines={settings.writingGuideLines}
                onPlayAudio={() => speakJapanese(currentCard.item.kana)}
                onComplete={advanceNext}
              />
            </div>
          </>
        )}

        {/* 3. MULTIPLE CHOICE QUESTIONS */}
        {(currentCard.type === 'mcq-kanji-to-kana' ||
          currentCard.type === 'mcq-kanji-kana-to-english' ||
          currentCard.type === 'mcq-english-to-kana') && (
          <>
            <div className="w-full text-left text-slate-300 text-lg">
              Which of these is...
            </div>

            <div className="flex flex-col items-center text-center my-auto">
              {currentCard.type === 'mcq-kanji-to-kana' && (
                <div className={`text-8xl sm:text-9xl ${fontClass}`}>
                  {currentCard.item.word}
                </div>
              )}

              {currentCard.type === 'mcq-kanji-kana-to-english' && (
                <>
                  <div className={`text-8xl sm:text-9xl mb-8 ${fontClass}`}>
                    {currentCard.item.word}
                  </div>
                  <div className={`text-3xl text-slate-300 ${fontClass}`}>
                    {displayKana}
                  </div>
                </>
              )}

              {currentCard.type === 'mcq-english-to-kana' && (
                <div className="text-5xl font-bold text-white">
                  {currentCard.item.meaning}
                </div>
              )}
            </div>

            <div className="w-full space-y-3">
              {currentCard.choices?.map((choice, idx) => {
                const isSelected = selectedChoice === choice;
                const isCorrect = choice === currentCard.correctAnswer;
                let btnStyle =
                  'bg-[#333A48] hover:bg-[#3E4759] border-slate-500/50 text-white';

                if (selectedChoice) {
                  if (isCorrect) {
                    btnStyle = 'bg-[#2ECC71] border-[#2ECC71] text-white';
                  } else if (isSelected) {
                    btnStyle = 'bg-[#EF4444] border-[#EF4444] text-white';
                  }
                }

                return (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleChoiceSelect(choice)}
                    className={`w-full py-4 px-5 rounded-xl border text-2xl font-medium transition ${fontClass} ${btnStyle}`}
                  >
                    {choice}
                  </button>
                );
              })}
            </div>
          </>
        )}
      </div>
    </div>
  );
};