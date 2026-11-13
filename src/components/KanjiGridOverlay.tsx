import React, { useState, useMemo } from 'react';
import { X, Settings, Search, Volume2 } from 'lucide-react';
import type {
  JLPTLevelId,
  KanjiLesson,
  KanjiLessonItem,
  CharacterStrokeData,
} from '../types/kanji';
import { KanjiCanvas } from './KanjiCanvas';

export interface LevelLessonsGroup {
  level: JLPTLevelId;
  lessons: KanjiLesson[];
  learnedLessonIds: string[];
}

interface KanjiGridOverlayProps {
  groups: LevelLessonsGroup[];
  allGroups?: LevelLessonsGroup[];
  onClose: () => void;
  onOpenSettings: () => void;
}

interface ExampleWordEntry {
  itemId: string;
  word: string;
  kana: string;
  meaning: string;
  lessonRef: string;
}

interface CoreKanjiEntry {
  char: string;
  kana: string;
  meaning: string;
  onyomi: string[];
  kunyomi: string[];
  strokeData: CharacterStrokeData;
  examples: ExampleWordEntry[];
  isLearned: boolean;
}

const LEVEL_NUM_MAP: Record<JLPTLevelId, number> = {
  N5: 1,
  N4: 2,
  N3: 3,
  N2: 4,
  N1: 5,
};

const N5_EXACT =
  '一二三四五六七八' +
  '九十口日白百千万' +
  '人分土時週月午年' +
  '今木田力前後先来' +
  '男女子供父火水金本' +
  '川山雨花耳手足目' +
  '北南東西上下中右' +
  '左私半母毎何友気' +
  '生魚大天空電車言' +
  '語名店馬駅道社国' +
  '外学校入見門間聞' +
  '書読舌話買行出休' +
  '食飲立会多小少古' +
  '新安高長円';

const N4_EXACT =
  '明朝曜昼夜夕去度' +
  '春夏秋冬色赤青黒' +
  '家族親姉兄弟妹主' +
  '体心風海銀肉牛鳥' +
  '茶味飯室通員犬歌' +
  '音文服医旅屋英字' +
  '用世仕院使町物正' +
  '館場地真紙画悪洋' +
  '代図工界堂病理漢' +
  '元意野京開歩走止' +
  '売計住待始起答持' +
  '着教動集借死習注' +
  '急建終試思考知写' +
  '映作働帰切者転貸' +
  '送別運重楽早広強' +
  '近公有不以同自方' +
  '研究題事特無品質' +
  '問的可料業発身台' +
  '験';

const CANONICAL_LEVEL_KANJI: Partial<Record<JLPTLevelId, string>> = {
  N5: Array.from(new Set(N5_EXACT.split(''))).join(''),
  N4: Array.from(new Set(N4_EXACT.split(''))).join(''),
};

function toHiragana(str: string): string {
  return str
    .replace(/[\u30a1-\u30f6]/g, (ch) => String.fromCharCode(ch.charCodeAt(0) - 0x60))
    .replace(/-/g, '');
}

export const KanjiGridOverlay: React.FC<KanjiGridOverlayProps> = ({
  groups,
  allGroups,
  onClose,
  onOpenSettings,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [inspectedKanji, setInspectedKanji] = useState<CoreKanjiEntry | null>(null);

  const playWordAudio = (itemId: string, textFallback: string) => {
    const audio = new Audio(`/audio/${itemId}-female.mp3`);
    audio.play().catch(() => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(textFallback);
        utter.lang = 'ja-JP';
        window.speechSynthesis.speak(utter);
      }
    });
  };

  const groupedKanji = useMemo(() => {
    const sourceGroups = allGroups && allGroups.length > 0 ? allGroups : groups;
    const orderedLevels: JLPTLevelId[] = ['N5', 'N4', 'N3', 'N2', 'N1'];
    const groupByLevel = new Map<JLPTLevelId, LevelLessonsGroup>();
    sourceGroups.forEach((g) => groupByLevel.set(g.level, g));

    const globalCharMap = new Map<string, CoreKanjiEntry>();
    const levelFirstSeen = new Map<JLPTLevelId, string[]>();

    orderedLevels.forEach((lvl) => {
      const grp = groupByLevel.get(lvl);
      if (!grp || grp.lessons.length === 0) return;

      const levelNum = LEVEL_NUM_MAP[lvl];
      const seenInThisLevel: string[] = [];

      grp.lessons.forEach((lesson) => {
        const lessonLearned = grp.learnedLessonIds.includes(lesson.id);
        const lessonRef = `${levelNum}-${lesson.lessonNumber}`;

        lesson.items.forEach((item: KanjiLessonItem) => {
          item.characters.forEach((charObj) => {
            const ch = charObj.char;
            if (!/[\u4e00-\u9faf]/.test(ch)) return;

            if (!seenInThisLevel.includes(ch)) {
              seenInThisLevel.push(ch);
            }

            const existing = globalCharMap.get(ch);
            if (!existing) {
              globalCharMap.set(ch, {
                char: ch,
                kana: item.kana,
                meaning: item.meaning,
                onyomi: item.onyomi,
                kunyomi: item.kunyomi,
                strokeData: charObj,
                examples: [
                  {
                    itemId: item.id,
                    word: item.word,
                    kana: item.kana,
                    meaning: item.meaning,
                    lessonRef,
                  },
                ],
                isLearned: lessonLearned,
              });
            } else {
              if (lessonLearned) existing.isLearned = true;
              if (!existing.examples.some((ex) => ex.word === item.word)) {
                existing.examples.push({
                  itemId: item.id,
                  word: item.word,
                  kana: item.kana,
                  meaning: item.meaning,
                  lessonRef,
                });
              }
              if (item.word === ch) {
                existing.kana = item.kana;
                existing.meaning = item.meaning;
                if (item.onyomi.length > 0) existing.onyomi = item.onyomi;
                if (item.kunyomi.length > 0) existing.kunyomi = item.kunyomi;
              }
            }
          });
        });
      });

      levelFirstSeen.set(lvl, seenInThisLevel);
    });

    const claimedKanji = new Set<string>();
    const levelEntriesMap = new Map<JLPTLevelId, CoreKanjiEntry[]>();

    orderedLevels.forEach((lvl) => {
      const canonical = CANONICAL_LEVEL_KANJI[lvl];
      if (canonical) {
        canonical.split('').forEach((ch) => {
          if (globalCharMap.has(ch)) claimedKanji.add(ch);
        });
      }
    });

    orderedLevels.forEach((lvl) => {
      const canonical = CANONICAL_LEVEL_KANJI[lvl];
      const entries: CoreKanjiEntry[] = [];

      if (canonical) {
        canonical.split('').forEach((ch) => {
          const entry = globalCharMap.get(ch);
          if (entry) {
            entries.push(entry);
          }
        });
      } else {
        const candidates = levelFirstSeen.get(lvl) || [];
        candidates.forEach((ch) => {
          if (!claimedKanji.has(ch)) {
            claimedKanji.add(ch);
            const entry = globalCharMap.get(ch);
            if (entry) entries.push(entry);
          }
        });
      }

      levelEntriesMap.set(lvl, entries);
    });

    return groups
      .filter((g) => g.lessons.length > 0)
      .map((g) => ({
        level: g.level,
        entries: levelEntriesMap.get(g.level) || [],
      }))
      .filter((g) => g.entries.length > 0);
  }, [groups, allGroups]);

  const filteredGroups = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    return groupedKanji
      .map(({ level, entries }) => ({
        level,
        entries: !q
          ? entries
          : entries.filter(
              (k) =>
                k.char.includes(searchQuery) ||
                k.kana.includes(searchQuery) ||
                k.meaning.toLowerCase().includes(q) ||
                k.onyomi.some((o) => o.includes(searchQuery)) ||
                k.kunyomi.some((ku) => ku.includes(searchQuery))
            ),
      }))
      .filter((g) => g.entries.length > 0);
  }, [groupedKanji, searchQuery]);

  const buildReadingGroups = (entry: CoreKanjiEntry) => {
    const readingGroups: {
      reading: string;
      type: "on'yomi" | "kun'yomi";
      words: ExampleWordEntry[];
    }[] = [];

    const assignedWords = new Set<string>();

    entry.onyomi.forEach((rawOn) => {
      const hiraOn = toHiragana(rawOn);
      const matching = entry.examples.filter((ex) => {
        if (assignedWords.has(ex.word)) return false;
        if (ex.kana.includes(hiraOn) && ex.word.length > 1 && !/[\u3041-\u3096]/.test(ex.word)) {
          assignedWords.add(ex.word);
          return true;
        }
        return false;
      });
      readingGroups.push({ reading: hiraOn, type: "on'yomi", words: matching });
    });

    entry.kunyomi.forEach((rawKun) => {
      const cleanKun = rawKun.replace(/\./g, '').replace(/-/g, '');
      const stem = rawKun.split('.')[0].replace(/-/g, '');
      const matching = entry.examples.filter((ex) => {
        if (assignedWords.has(ex.word)) return false;
        if (ex.kana.includes(cleanKun) || (stem && ex.kana.includes(stem))) {
          assignedWords.add(ex.word);
          return true;
        }
        return false;
      });
      readingGroups.push({ reading: cleanKun, type: "kun'yomi", words: matching });
    });

    const leftovers = entry.examples.filter((ex) => !assignedWords.has(ex.word));
    if (leftovers.length > 0) {
      if (readingGroups.length > 0) {
        readingGroups[0].words.push(...leftovers);
      } else {
        readingGroups.push({ reading: entry.kana, type: "kun'yomi", words: leftovers });
      }
    }

    return readingGroups.filter((g, idx) => g.words.length > 0 || idx < 2);
  };

  if (inspectedKanji) {
    const readingGroups = buildReadingGroups(inspectedKanji);

    return (
      <div className="min-h-screen bg-[#242933] text-white flex flex-col px-5 py-4 pb-12 select-none">
        <div className="max-w-md mx-auto w-full flex-1 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <button
              type="button"
              onClick={() => setInspectedKanji(null)}
              aria-label="Back to Kanji grid"
              className="text-slate-200 hover:text-white p-1"
            >
              <X className="w-7 h-7 stroke-[2.5]" />
            </button>
            <button
              type="button"
              onClick={onOpenSettings}
              aria-label="Open settings"
              className="text-slate-200 hover:text-white p-1"
            >
              <Settings className="w-6 h-6" />
            </button>
          </div>

          <div className="mb-6">
            <KanjiCanvas
              key={inspectedKanji.char}
              characters={[inspectedKanji.strokeData]}
              initialHinted={true}
              showGuideLines={false}
              practiceMode={true}
            />
          </div>

          <div>
            <div className="text-base font-bold text-white mb-2.5">Readings:</div>

            <div className="space-y-4">
              {readingGroups.map((group, gIdx) => (
                <div key={gIdx} className="space-y-2">
                  <div
                    className={`w-full px-4 py-2.5 rounded-lg flex items-center justify-between font-bold text-white shadow-sm ${
                      group.type === "on'yomi" ? 'bg-[#F59E0B]' : 'bg-[#7CC4FA]'
                    }`}
                  >
                    <span className="text-xl tracking-wide">{group.reading}</span>
                    <span className="text-sm font-semibold">{group.type}</span>
                  </div>

                  {group.words.map((w, wIdx) => (
                    <div
                      key={wIdx}
                      onClick={() => playWordAudio(w.itemId, w.kana)}
                      className="w-full px-4 py-3 rounded-lg bg-[#2E3440] border border-slate-600/40 hover:border-slate-500/70 flex items-center justify-between gap-4 cursor-pointer transition"
                    >
                      <div className="flex flex-col items-center min-w-[72px]">
                        <span className="text-2xl font-serif text-white leading-tight">
                          {w.word}
                        </span>
                        <span className="text-xs text-slate-300 mt-1 tracking-wider">
                          {w.kana}
                        </span>
                      </div>

                      <div className="flex-1 text-left">
                        <div className="text-sm font-bold text-white">{w.meaning}</div>
                        <div className="text-xs text-slate-400 mt-0.5">
                          Lesson: {w.lessonRef}
                        </div>
                      </div>

                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          playWordAudio(w.itemId, w.kana);
                        }}
                        aria-label={`Listen to ${w.word}`}
                        title="Listen"
                        className="p-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-700/60 shrink-0 transition"
                      >
                        <Volume2 className="w-5 h-5" />
                      </button>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#242933] text-white flex flex-col justify-between px-5 py-4 select-none">
      <div className="max-w-md mx-auto w-full flex-1 flex flex-col">
        <div className="flex items-center justify-between mb-6">
          <button
            type="button"
            onClick={onClose}
            aria-label="Close kanji grid"
            className="text-slate-200 hover:text-white p-1"
          >
            <X className="w-7 h-7 stroke-[2.5]" />
          </button>
          <button
            type="button"
            onClick={onOpenSettings}
            aria-label="Open settings"
            className="text-slate-200 hover:text-white p-1"
          >
            <Settings className="w-6 h-6" />
          </button>
        </div>

        <div className="space-y-8 pb-6">
          {filteredGroups.map(({ level, entries }) => (
            <div key={level}>
              <div className="text-sm font-bold text-slate-400 mb-3 tracking-wide">
                JLPT {level}
              </div>

              <div className="grid grid-cols-8 gap-y-3 text-center">
                {entries.map((entry) => (
                  <button
                    key={`${level}-${entry.char}`}
                    type="button"
                    onClick={() => setInspectedKanji(entry)}
                    className={`text-2xl sm:text-3xl font-serif py-1 rounded transition hover:bg-white/10 ${
                      entry.isLearned ? 'text-[#2ECC71]' : 'text-slate-100'
                    }`}
                  >
                    {entry.char}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="sticky bottom-0 bg-[#242933]/95 backdrop-blur max-w-md mx-auto w-full pt-3 pb-3">
        <div className="relative">
          <Search className="w-5 h-5 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder=""
            aria-label="Search Kanji"
            className="w-full pl-11 pr-4 py-2.5 rounded-lg bg-[#333A48] text-white border border-slate-500/40 focus:outline-none focus:border-slate-300"
          />
        </div>
      </div>
    </div>
  );
};