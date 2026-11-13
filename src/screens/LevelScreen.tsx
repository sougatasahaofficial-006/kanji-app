import React, { useState, useMemo, useEffect } from 'react';
import { X, List, Settings } from 'lucide-react';
import {
  JLPT_LEVELS,
  JLPT_SUBSECTIONS,
  type JLPTLevelId,
  type JLPTSubsectionInfo,
  type KanjiLesson,
} from '../types/kanji';
import { KanjiGridOverlay, type LevelLessonsGroup } from '../components/KanjiGridOverlay';

interface LevelScreenProps {
  level: JLPTLevelId;
  lessons: KanjiLesson[];
  learnedLessonIds: string[];
  allLevelGroups: LevelLessonsGroup[];
  dueCount: number;
  dailyReviewsCompleted: number;
  dailyLessonGoal: number;
  dailyTargetLessonIds: string[];
  goalCompletedDates: string[];
  showDailyGoals: boolean;
  onEnsureDailyTargets: (level: JLPTLevelId, orderedLessonIds: string[]) => void;
  onBack: () => void;
  onOpenSettings: () => void;
  onStartLesson: (lesson: KanjiLesson) => void;
  onStartPastDueReview: () => void;
  onOpenCustomReview: () => void;
}

export const LevelScreen: React.FC<LevelScreenProps> = ({
  level,
  lessons,
  learnedLessonIds,
  allLevelGroups,
  dueCount,
  dailyReviewsCompleted,
  dailyLessonGoal,
  dailyTargetLessonIds,
  goalCompletedDates,
  showDailyGoals,
  onEnsureDailyTargets,
  onBack,
  onOpenSettings,
  onStartLesson,
  onStartPastDueReview,
  onOpenCustomReview,
}) => {
  const [selectedSubsection, setSelectedSubsection] = useState<JLPTSubsectionInfo | null>(null);
  const [showAllKanjiGrid, setShowAllKanjiGrid] = useState(false);

  const subsections = JLPT_SUBSECTIONS[level] || [];
  const levelInfo = JLPT_LEVELS.find((l) => l.id === level);
  const badgeColor = levelInfo?.badgeColor || '#5DA9E9';

  const visibleLessons = useMemo(() => {
    if (!selectedSubsection) return lessons;
    return lessons.filter(
      (l) =>
        l.lessonNumber >= selectedSubsection.startLesson &&
        l.lessonNumber <= selectedSubsection.endLesson
    );
  }, [lessons, selectedSubsection]);

  useEffect(() => {
    if (showDailyGoals && lessons.length > 0) {
      onEnsureDailyTargets(
        level,
        lessons.map((l) => l.id)
      );
    }
  }, [showDailyGoals, level, lessons, dailyLessonGoal, onEnsureDailyTargets]);

  const isLessonUnlocked = (lesson: KanjiLesson) => {
    const globalIndex = lessons.findIndex((l) => l.id === lesson.id);
    if (globalIndex <= 0) return true;
    if (learnedLessonIds.includes(lesson.id)) return true;
    const prevLesson = lessons[globalIndex - 1];
    return prevLesson ? learnedLessonIds.includes(prevLesson.id) : false;
  };

  const targetLessons = useMemo(() => {
    const goalCount = dailyLessonGoal || 2;
    if (dailyTargetLessonIds.length > 0) {
      return dailyTargetLessonIds
        .slice(0, goalCount)
        .map((id) => lessons.find((l) => l.id === id))
        .filter((l): l is KanjiLesson => Boolean(l));
    }
    return lessons.filter((l) => !learnedLessonIds.includes(l.id)).slice(0, goalCount);
  }, [dailyTargetLessonIds, dailyLessonGoal, lessons, learnedLessonIds]);

  const isReviewGoalDone =
    learnedLessonIds.length === 0 ? dailyReviewsCompleted > 0 : dueCount === 0 || dailyReviewsCompleted > 0;

  const calendarData = useMemo(() => {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    const todayDate = now.getDate();
    const monthName = now.toLocaleString('en-US', { month: 'long' });
    const firstWeekday = new Date(year, month, 1).getDay();

    const cells: { key: string; day: number | null; completed: boolean; isToday: boolean }[] = [];

    for (let i = 0; i < firstWeekday; i++) {
      cells.push({ key: `pad-${i}`, day: null, completed: false, isToday: false });
    }

    for (let d = 1; d <= todayDate; d++) {
      const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      const isToday = d === todayDate;
      const allLessonsTodayDone =
        targetLessons.length > 0 && targetLessons.every((l) => learnedLessonIds.includes(l.id));
      const completed =
        goalCompletedDates.includes(dateStr) || (isToday && isReviewGoalDone && allLessonsTodayDone);

      cells.push({
        key: dateStr,
        day: d,
        completed,
        isToday,
      });
    }

    return { monthName, cells };
  }, [goalCompletedDates, targetLessons, learnedLessonIds, isReviewGoalDone]);

  if (showAllKanjiGrid) {
    return (
      <KanjiGridOverlay
        groups={allLevelGroups}
        allGroups={allLevelGroups}
        onClose={() => setShowAllKanjiGrid(false)}
        onOpenSettings={onOpenSettings}
      />
    );
  }

  // Sub-section Selector View
  if (subsections.length > 0 && !selectedSubsection) {
    return (
      <div className="min-h-screen bg-[#242933] text-white flex flex-col select-none">
        <div className="sticky top-0 z-10 bg-[#242933]/95 backdrop-blur px-5 py-4 flex items-center justify-between max-w-lg mx-auto w-full">
          <button
            type="button"
            onClick={onBack}
            aria-label="Back to levels"
            className="text-slate-200 hover:text-white p-1"
          >
            <X className="w-7 h-7 stroke-[2.5]" />
          </button>

          <div className="flex items-center gap-4">
            <button
              type="button"
              onClick={() => setShowAllKanjiGrid(true)}
              title="View all Kanji (N5 - N1)"
              aria-label="View all Kanji"
              className="text-slate-200 hover:text-white p-1"
            >
              <List className="w-6 h-6" />
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
        </div>

        <div className="flex-1 flex flex-col items-center justify-center gap-10 py-8 px-5">
          {subsections.map((sub) => (
            <button
              key={sub.id}
              type="button"
              onClick={() => setSelectedSubsection(sub)}
              className="flex flex-col items-center group focus:outline-none"
            >
              <div
                style={{ backgroundColor: badgeColor }}
                className="w-40 h-40 sm:w-44 sm:h-44 rounded-full flex items-center justify-center text-7xl sm:text-8xl font-serif text-white shadow-lg transition-transform group-hover:scale-105 group-active:scale-95"
              >
                {sub.badgeKanji}
              </div>
              <div className="mt-3 text-base font-bold text-white tracking-wide">
                {sub.label}
              </div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  // Main Lesson Roadmap View
  return (
    <div className="min-h-screen bg-[#242933] text-white flex flex-col justify-between select-none">
      <div className="sticky top-0 z-10 bg-[#242933]/95 backdrop-blur px-5 py-4 flex items-center justify-between max-w-lg mx-auto w-full">
        <button
          type="button"
          onClick={() => {
            if (selectedSubsection) {
              setSelectedSubsection(null);
            } else {
              onBack();
            }
          }}
          aria-label="Back"
          className="text-slate-200 hover:text-white p-1"
        >
          <X className="w-7 h-7 stroke-[2.5]" />
        </button>

        <div className="flex items-center gap-4">
          <button
            type="button"
            onClick={() => setShowAllKanjiGrid(true)}
            title="View all Kanji (N5 - N1)"
            aria-label="View all Kanji"
            className="text-slate-200 hover:text-white p-1"
          >
            <List className="w-6 h-6" />
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
      </div>

      {/* Original-style Daily Goals Card */}
      {showDailyGoals && (
        <div className="max-w-lg mx-auto w-full px-5 mb-5">
          <div className="bg-[#343C48] border border-slate-500/40 rounded-2xl px-5 py-4 shadow-md flex items-start justify-between gap-4">
            {/* Left: Daily Goals Checklist */}
            <div className="min-w-0">
              <div className="text-base font-bold text-white mb-2.5 tracking-tight">
                Daily Goals
              </div>
              <div className="space-y-2">
                <button
                  type="button"
                  disabled={learnedLessonIds.length === 0}
                  onClick={onStartPastDueReview}
                  className="flex items-center gap-2.5 text-left group disabled:cursor-default"
                >
                  <span
                    className={`w-3.5 h-3.5 rounded-[4px] shrink-0 transition ${
                      isReviewGoalDone
                        ? 'bg-[#5DA9E9]'
                        : 'bg-[#4B5565] group-hover:bg-[#5B6678]'
                    }`}
                  />
                  <span
                    className={`text-sm font-semibold ${
                      isReviewGoalDone ? 'text-white' : 'text-slate-200'
                    }`}
                  >
                    Review
                  </span>
                </button>

                {targetLessons.map((lesson) => {
                  const done = learnedLessonIds.includes(lesson.id);
                  const unlocked = isLessonUnlocked(lesson);
                  return (
                    <button
                      key={lesson.id}
                      type="button"
                      disabled={!unlocked}
                      onClick={() => onStartLesson(lesson)}
                      className="flex items-center gap-2.5 text-left group disabled:cursor-default"
                    >
                      <span
                        className={`w-3.5 h-3.5 rounded-[4px] shrink-0 transition ${
                          done ? 'bg-[#5DA9E9]' : 'bg-[#4B5565]'
                        }`}
                      />
                      <span
                        className={`text-sm font-semibold ${
                          done ? 'text-white' : 'text-slate-200'
                        }`}
                      >
                        Lesson {lesson.lessonNumber}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Right: Monthly S M T W T F S Progress Grid */}
            <div className="shrink-0">
              <div className="text-[11px] font-bold text-white text-center mb-1.5">
                {calendarData.monthName}
              </div>
              <div className="grid grid-cols-7 gap-1 text-center mb-1">
                {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((dayLetter, idx) => (
                  <span
                    key={idx}
                    className="w-4 text-[9px] font-bold text-slate-300 leading-none"
                  >
                    {dayLetter}
                  </span>
                ))}
              </div>
              <div className="grid grid-cols-7 gap-1">
                {calendarData.cells.map((cell) =>
                  cell.day === null ? (
                    <div key={cell.key} className="w-4 h-4" />
                  ) : (
                    <div
                      key={cell.key}
                      title={`${calendarData.monthName} ${cell.day}`}
                      className={`w-4 h-4 rounded-[4px] border transition ${
                        cell.completed
                          ? 'bg-[#5DA9E9] border-[#5DA9E9]'
                          : cell.isToday
                          ? 'border-slate-300/80 bg-transparent'
                          : 'border-slate-400/50 bg-transparent'
                      }`}
                    />
                  )
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="flex-1 max-w-lg mx-auto w-full px-5 pb-36">
        {visibleLessons.length === 0 ? (
          <div className="text-center text-slate-400 py-20">
            Curriculum data for {selectedSubsection ? selectedSubsection.label : level} is ready to be imported.
          </div>
        ) : (
          <div className="space-y-5 pt-1">
            {visibleLessons.map((lesson) => {
              const learned = learnedLessonIds.includes(lesson.id);
              const unlocked = isLessonUnlocked(lesson);
              const firstWord = lesson.items[0]?.word || '一';
              const previewWords = lesson.items.map((i) => i.word).join(', ');

              return (
                <button
                  key={lesson.id}
                  type="button"
                  disabled={!unlocked}
                  onClick={() => onStartLesson(lesson)}
                  className={`w-full flex items-center gap-4 text-left group transition ${
                    unlocked ? 'cursor-pointer' : 'cursor-not-allowed'
                  }`}
                >
                  <div
                    className={`w-16 h-16 shrink-0 rounded-full flex items-center justify-center font-serif text-white shadow transition-transform whitespace-nowrap overflow-hidden px-1 ${
                      firstWord.length >= 3
                        ? 'text-sm'
                        : firstWord.length === 2
                        ? 'text-lg'
                        : 'text-3xl'
                    } ${
                      learned
                        ? 'bg-[#5DA9E9] group-hover:scale-105'
                        : unlocked
                        ? 'bg-[#5DA9E9]/85 ring-2 ring-sky-300 group-hover:scale-105'
                        : 'bg-[#7A818E]'
                    }`}
                  >
                    {firstWord}
                  </div>

                  <div className="min-w-0 flex-1">
                    <div className="text-base font-bold text-white">
                      Lesson {lesson.lessonNumber}
                    </div>
                    <div className="text-xs text-slate-300 truncate mt-0.5">{previewWords}</div>
                    <div className="text-xs text-slate-400 mt-0.5">
                      {learned ? 'Learned' : unlocked ? 'Ready to Learn' : 'Locked'}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </div>

      <div className="fixed bottom-0 inset-x-0 bg-gradient-to-t from-[#242933] via-[#242933] to-transparent pt-4 pb-5 px-5">
        <div className="max-w-lg mx-auto space-y-2.5">
          <button
            type="button"
            disabled={learnedLessonIds.length === 0}
            onClick={onStartPastDueReview}
            className="w-full py-3.5 rounded-xl bg-[#F59E0B] hover:bg-[#D97706] disabled:opacity-45 disabled:cursor-not-allowed text-white font-semibold text-lg shadow-lg transition"
          >
            Review Past Due {dueCount > 0 ? `(${dueCount})` : ''}
          </button>
          <button
            type="button"
            disabled={learnedLessonIds.length === 0}
            onClick={onOpenCustomReview}
            className="w-full py-3.5 rounded-xl bg-[#7CC4FA] hover:bg-[#5DA9E9] disabled:opacity-45 disabled:cursor-not-allowed text-white font-semibold text-lg shadow-lg transition"
          >
            Custom Review
          </button>
        </div>
      </div>
    </div>
  );
};