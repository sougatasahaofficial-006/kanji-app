import { useState, useEffect, useCallback } from 'react';
import type { AppSettings, JLPTLevelId, SRSItemProgress } from '../types/kanji';

const STORAGE_KEY = 'kanji_app_state_v1';

export const DEFAULT_SETTINGS: AppSettings = {
  autoPlayAudio: true,
  voice: 'male',
  font: 'stylized',
  kana: 'hiragana',
  lessonQuestionsPerWord: 5,
  writingGuideLines: false,
  reviewFrequency: 1.0,
  maxReviewsPerDay: 100,
  kanjiAnswerFormat: 'writing',
  kanaAnswerFormat: 'choices',
  englishAnswerFormat: 'choices',
  showDailyGoals: false,
  dailyLessonGoal: 2,
  dailyStudyReminders: false,
  appLanguage: 'System Default',
};

interface StoredState {
  settings: AppSettings;
  learnedLessons: Record<JLPTLevelId, string[]>;
  srsProgress: Record<string, SRSItemProgress>;
  dailyReviewsCompleted: { date: string; count: number };
  dailyLessonsCompleted: { date: string; lessonIds: string[] };
  dailyTargetLessonIds: { date: string; byLevel: Partial<Record<JLPTLevelId, string[]>> };
  goalCompletedDates: string[];
}

const getTodayString = () => {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
};

const INITIAL_STATE: StoredState = {
  settings: DEFAULT_SETTINGS,
  learnedLessons: {
    N5: [],
    N4: [],
    N3: [],
    N2: [],
    N1: [],
  },
  srsProgress: {},
  dailyReviewsCompleted: { date: getTodayString(), count: 0 },
  dailyLessonsCompleted: { date: getTodayString(), lessonIds: [] },
  dailyTargetLessonIds: { date: getTodayString(), byLevel: {} },
  goalCompletedDates: [],
};

export function useAppStore() {
  const [state, setState] = useState<StoredState>(() => {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) return INITIAL_STATE;
      const parsed = JSON.parse(raw);
      return {
        ...INITIAL_STATE,
        ...parsed,
        settings: { ...DEFAULT_SETTINGS, ...(parsed.settings || {}) },
        learnedLessons: { ...INITIAL_STATE.learnedLessons, ...(parsed.learnedLessons || {}) },
        dailyLessonsCompleted: parsed.dailyLessonsCompleted || INITIAL_STATE.dailyLessonsCompleted,
        dailyTargetLessonIds: parsed.dailyTargetLessonIds || INITIAL_STATE.dailyTargetLessonIds,
        goalCompletedDates: Array.isArray(parsed.goalCompletedDates) ? parsed.goalCompletedDates : [],
      };
    } catch {
      return INITIAL_STATE;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (err) {
      console.error('Failed to save progress to localStorage:', err);
    }
  }, [state]);

  const updateSettings = useCallback((partial: Partial<AppSettings>) => {
    setState((prev) => ({
      ...prev,
      settings: { ...prev.settings, ...partial },
    }));
  }, []);

  const ensureDailyTargetLessons = useCallback(
    (level: JLPTLevelId, orderedLessonIds: string[]) => {
      setState((prev) => {
        const today = getTodayString();
        const currentByLevel =
          prev.dailyTargetLessonIds.date === today ? prev.dailyTargetLessonIds.byLevel : {};
        const existingTargets = currentByLevel[level];
        const goalCount = prev.settings.dailyLessonGoal || 2;

        if (existingTargets && existingTargets.length === goalCount) {
          return prev;
        }

        const learnedSet = new Set(prev.learnedLessons[level] || []);
        const todayCompletedSet = new Set(
          prev.dailyLessonsCompleted.date === today ? prev.dailyLessonsCompleted.lessonIds : []
        );

        const completedTodayInLevel = orderedLessonIds.filter((id) => todayCompletedSet.has(id));
        const unlearned = orderedLessonIds.filter((id) => !learnedSet.has(id));
        const combined = Array.from(new Set([...completedTodayInLevel, ...unlearned])).slice(
          0,
          goalCount
        );

        return {
          ...prev,
          dailyTargetLessonIds: {
            date: today,
            byLevel: {
              ...currentByLevel,
              [level]: combined,
            },
          },
        };
      });
    },
    []
  );

  const checkAndMarkTodayGoalComplete = (
    nextState: StoredState,
    level: JLPTLevelId,
    today: string
  ): string[] => {
    const targets =
      nextState.dailyTargetLessonIds.date === today
        ? nextState.dailyTargetLessonIds.byLevel[level] || []
        : [];
    const learnedSet = new Set(nextState.learnedLessons[level] || []);
    const allLessonsDone = targets.length > 0 && targets.every((id) => learnedSet.has(id));

    const now = Date.now();
    const anyDueForLevel = Object.values(nextState.srsProgress).some(
      (rec) => rec.level === level && rec.nextReviewTimestamp <= now
    );
    const reviewedToday =
      nextState.dailyReviewsCompleted.date === today && nextState.dailyReviewsCompleted.count > 0;
    const reviewDone = !anyDueForLevel || reviewedToday;

    if (allLessonsDone && reviewDone && !nextState.goalCompletedDates.includes(today)) {
      return [...nextState.goalCompletedDates, today];
    }
    return nextState.goalCompletedDates;
  };

  const completeLesson = useCallback(
    (level: JLPTLevelId, lessonId: string, itemIds: string[]) => {
      setState((prev) => {
        const today = getTodayString();
        const existingLessons = prev.learnedLessons[level] || [];
        const updatedLessons = existingLessons.includes(lessonId)
          ? existingLessons
          : [...existingLessons, lessonId];

        const prevTodayLessons =
          prev.dailyLessonsCompleted.date === today ? prev.dailyLessonsCompleted.lessonIds : [];
        const updatedTodayLessons = prevTodayLessons.includes(lessonId)
          ? prevTodayLessons
          : [...prevTodayLessons, lessonId];

        const now = Date.now();
        const oneDayMs = 24 * 60 * 60 * 1000;
        const updatedSrs = { ...prev.srsProgress };

        itemIds.forEach((id) => {
          if (!updatedSrs[id]) {
            updatedSrs[id] = {
              itemId: id,
              level,
              intervalDays: 1,
              easeFactor: 2.5,
              nextReviewTimestamp: now + oneDayMs / prev.settings.reviewFrequency,
              repetitions: 1,
            };
          }
        });

        const nextState: StoredState = {
          ...prev,
          learnedLessons: {
            ...prev.learnedLessons,
            [level]: updatedLessons,
          },
          dailyLessonsCompleted: {
            date: today,
            lessonIds: updatedTodayLessons,
          },
          srsProgress: updatedSrs,
        };

        nextState.goalCompletedDates = checkAndMarkTodayGoalComplete(nextState, level, today);
        return nextState;
      });
    },
    []
  );

  const recordItemReview = useCallback((itemId: string, level: JLPTLevelId, wasCorrect: boolean) => {
    setState((prev) => {
      const now = Date.now();
      const oneDayMs = 24 * 60 * 60 * 1000;
      const current = prev.srsProgress[itemId] || {
        itemId,
        level,
        intervalDays: 1,
        easeFactor: 2.5,
        nextReviewTimestamp: now,
        repetitions: 0,
      };

      let nextInterval = 1;
      let nextEase = current.easeFactor;
      let nextReps = current.repetitions;

      if (wasCorrect) {
        nextReps += 1;
        if (nextReps === 1) nextInterval = 1;
        else if (nextReps === 2) nextInterval = 3;
        else nextInterval = Math.round(current.intervalDays * nextEase);
        nextEase = Math.min(3.0, nextEase + 0.1);
      } else {
        nextReps = 0;
        nextInterval = 0.5;
        nextEase = Math.max(1.3, nextEase - 0.2);
      }

      const adjustedDays = nextInterval / prev.settings.reviewFrequency;
      const today = getTodayString();
      const prevDailyCount =
        prev.dailyReviewsCompleted.date === today ? prev.dailyReviewsCompleted.count : 0;

      const nextState: StoredState = {
        ...prev,
        srsProgress: {
          ...prev.srsProgress,
          [itemId]: {
            ...current,
            intervalDays: nextInterval,
            easeFactor: nextEase,
            repetitions: nextReps,
            nextReviewTimestamp: now + adjustedDays * oneDayMs,
          },
        },
        dailyReviewsCompleted: {
          date: today,
          count: prevDailyCount + 1,
        },
      };

      nextState.goalCompletedDates = checkAndMarkTodayGoalComplete(nextState, level, today);
      return nextState;
    });
  }, []);

  const today = getTodayString();

  return {
    settings: state.settings,
    learnedLessons: state.learnedLessons,
    srsProgress: state.srsProgress,
    dailyReviewsCompleted:
      state.dailyReviewsCompleted.date === today ? state.dailyReviewsCompleted.count : 0,
    dailyTargetLessonIdsByLevel:
      state.dailyTargetLessonIds.date === today ? state.dailyTargetLessonIds.byLevel : {},
    goalCompletedDates: state.goalCompletedDates,
    updateSettings,
    ensureDailyTargetLessons,
    completeLesson,
    recordItemReview,
  };
}