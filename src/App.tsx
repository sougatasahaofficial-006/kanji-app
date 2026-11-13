import type { JLPTLevelId, KanjiLesson, KanjiLessonItem } from './types/kanji';
import { N5_LESSONS } from './data/n5';
import { N4_LESSONS } from './data/n4';
import { N3_LESSONS } from './data/n3';
import { N2_LESSONS } from './data/n2';
import { N1_LESSONS } from './data/n1';
import { useAppStore } from './store/useAppStore';
import { HomeScreen } from './screens/HomeScreen';
import { LevelScreen } from './screens/LevelScreen';
import { CustomReviewScreen } from './screens/CustomReviewScreen';
import { SettingsScreen } from './screens/SettingsScreen';
import { SessionRunner } from './components/SessionRunner';
import { useState, useMemo, useEffect } from 'react';
import {
  ensureNotificationServiceWorker,
  checkAndNotifyDailyPracticeDue,
} from './utils/notifications';

type ActiveView =
  | { name: 'home' }
  | { name: 'level'; level: JLPTLevelId }
  | { name: 'custom-review'; level: JLPTLevelId }
  | { name: 'lesson-session'; level: JLPTLevelId; lesson: KanjiLesson }
  | { name: 'review-session'; level: JLPTLevelId; items: KanjiLessonItem[] };

export function App() {
  const {
    settings,
    learnedLessons,
    srsProgress,
    dailyReviewsCompleted,
    dailyTargetLessonIdsByLevel,
    goalCompletedDates,
    updateSettings,
    ensureDailyTargetLessons,
    completeLesson,
    recordItemReview,
  } = useAppStore();

  const [view, setView] = useState<ActiveView>({ name: 'home' });
  const [settingsOpen, setSettingsOpen] = useState(false);

  function getLessonsForLevel(level: JLPTLevelId): KanjiLesson[] {
    switch (level) {
      case 'N5':
        return N5_LESSONS;
      case 'N4':
        return N4_LESSONS;
      case 'N3':
        return N3_LESSONS;
      case 'N2':
        return N2_LESSONS;
      case 'N1':
        return N1_LESSONS;
      default:
        return [];
    }
  }

  const allLevelGroups = useMemo(
    () => [
      { level: 'N5' as JLPTLevelId, lessons: N5_LESSONS, learnedLessonIds: learnedLessons.N5 || [] },
      { level: 'N4' as JLPTLevelId, lessons: N4_LESSONS, learnedLessonIds: learnedLessons.N4 || [] },
      { level: 'N3' as JLPTLevelId, lessons: N3_LESSONS, learnedLessonIds: learnedLessons.N3 || [] },
      { level: 'N2' as JLPTLevelId, lessons: N2_LESSONS, learnedLessonIds: learnedLessons.N2 || [] },
      { level: 'N1' as JLPTLevelId, lessons: N1_LESSONS, learnedLessonIds: learnedLessons.N1 || [] },
    ],
    [learnedLessons]
  );

  const activeLevel: JLPTLevelId =
    view.name === 'home' ? 'N5' : view.level;

  const levelLessons = useMemo(
    () => getLessonsForLevel(activeLevel),
    [activeLevel]
  );

  const allLevelItems = useMemo(
    () => levelLessons.flatMap((l) => l.items),
    [levelLessons]
  );

  const learnedItemsForLevel = useMemo(() => {
    const completedIds = learnedLessons[activeLevel] || [];
    return levelLessons
      .filter((l) => completedIds.includes(l.id))
      .flatMap((l) => l.items);
  }, [levelLessons, learnedLessons, activeLevel]);

  const pastDueItemsForLevel = useMemo(() => {
    const now = Date.now();
    const due = learnedItemsForLevel.filter((item) => {
      const record = srsProgress[item.id];
      return !record || record.nextReviewTimestamp <= now;
    });
    return due.length > 0 ? due : learnedItemsForLevel;
  }, [learnedItemsForLevel, srsProgress]);
  useEffect(() => {
    if (settings.dailyStudyReminders) {
      ensureNotificationServiceWorker();
    }
  }, [settings.dailyStudyReminders]);

  useEffect(() => {
    if (!settings.dailyStudyReminders) return;

    const now = Date.now();
    const allLearnedItems = (Object.keys(learnedLessons) as JLPTLevelId[]).flatMap((lvl) => {
      const lessons = getLessonsForLevel(lvl);
      const completed = learnedLessons[lvl] || [];
      return lessons.filter((l) => completed.includes(l.id)).flatMap((l) => l.items);
    });

    const totalDueCount = allLearnedItems.filter((item) => {
      const rec = srsProgress[item.id];
      return !rec || rec.nextReviewTimestamp <= now;
    }).length;

    const todayStr = new Date().toISOString().split('T')[0];
    const isGoalCompleteToday = goalCompletedDates.includes(todayStr);

    checkAndNotifyDailyPracticeDue({
      enabled: settings.dailyStudyReminders,
      dueCount: totalDueCount,
      remainingLessons: isGoalCompleteToday ? 0 : (settings.dailyLessonGoal ?? 2),
      isGoalCompleteToday,
    });
  }, [
    settings.dailyStudyReminders,
    settings.dailyLessonGoal,
    learnedLessons,
    srsProgress,
    goalCompletedDates,
  ]);

  if (settingsOpen) {
    return (
      <SettingsScreen
        settings={settings}
        onUpdate={updateSettings}
        onClose={() => setSettingsOpen(false)}
      />
    );
  }

  if (view.name === 'home') {
    return (
      <HomeScreen
        allLevelGroups={allLevelGroups}
        onSelectLevel={(level) => setView({ name: 'level', level })}
        onOpenSettings={() => setSettingsOpen(true)}
      />
    );
  }

  if (view.name === 'level') {
    const dueCount = learnedItemsForLevel.filter((item) => {
      const record = srsProgress[item.id];
      return !record || record.nextReviewTimestamp <= Date.now();
    }).length;

    return (
      <LevelScreen
        level={view.level}
        lessons={levelLessons}
        learnedLessonIds={learnedLessons[view.level] || []}
        allLevelGroups={allLevelGroups}
        dueCount={dueCount}
        dailyReviewsCompleted={dailyReviewsCompleted}
        dailyLessonGoal={settings.dailyLessonGoal ?? 2}
        dailyTargetLessonIds={dailyTargetLessonIdsByLevel[view.level] || []}
        goalCompletedDates={goalCompletedDates}
        showDailyGoals={settings.showDailyGoals}
        onEnsureDailyTargets={ensureDailyTargetLessons}
        onBack={() => setView({ name: 'home' })}
        onOpenSettings={() => setSettingsOpen(true)}
        onStartLesson={(lesson) =>
          setView({ name: 'lesson-session', level: view.level, lesson })
        }
        onStartPastDueReview={() => {
          const batch = [...pastDueItemsForLevel]
            .sort(() => Math.random() - 0.5)
            .slice(0, settings.maxReviewsPerDay);
          if (batch.length > 0) {
            setView({ name: 'review-session', level: view.level, items: batch });
          }
        }}
        onOpenCustomReview={() =>
          setView({ name: 'custom-review', level: view.level })
        }
      />
    );
  }

  if (view.name === 'custom-review') {
    return (
      <CustomReviewScreen
        level={view.level}
        learnedItems={learnedItemsForLevel}
        onBack={() => setView({ name: 'level', level: view.level })}
        onOpenSettings={() => setSettingsOpen(true)}
        onStartReview={(selectedItems) =>
          setView({ name: 'review-session', level: view.level, items: selectedItems })
        }
      />
    );
  }

  if (view.name === 'lesson-session') {
    return (
      <SessionRunner
        items={view.lesson.items}
        allPoolItems={allLevelItems}
        settings={settings}
        isReviewMode={false}
        onOpenSettings={() => setSettingsOpen(true)}
        onExit={() => setView({ name: 'level', level: view.level })}
        onItemResult={(itemId, wasCorrect) =>
          recordItemReview(itemId, view.level, wasCorrect)
        }
        onSessionComplete={() => {
          completeLesson(
            view.level,
            view.lesson.id,
            view.lesson.items.map((i) => i.id)
          );
          setView({ name: 'level', level: view.level });
        }}
      />
    );
  }

  if (view.name === 'review-session') {
    return (
      <SessionRunner
        items={view.items}
        allPoolItems={allLevelItems}
        settings={settings}
        isReviewMode={true}
        onOpenSettings={() => setSettingsOpen(true)}
        onExit={() => setView({ name: 'level', level: view.level })}
        onItemResult={(itemId, wasCorrect) =>
          recordItemReview(itemId, view.level, wasCorrect)
        }
        onSessionComplete={() => setView({ name: 'level', level: view.level })}
      />
    );
  }

  return null;
}

export default App;