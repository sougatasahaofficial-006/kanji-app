import React, { useEffect } from 'react';
import { X } from 'lucide-react';
import type { AppSettings } from '../types/kanji';
import {
  requestAndTriggerStudyNotification,
  scheduleDailyStudyReminder,
  cancelDailyStudyReminder,
} from '../utils/notifications';

interface SettingsScreenProps {
  settings: AppSettings;
  onUpdate: (partial: Partial<AppSettings>) => void;
  onClose: () => void;
}

export const SettingsScreen: React.FC<SettingsScreenProps> = ({
  settings,
  onUpdate,
  onClose,
}) => {
  useEffect(() => {
    if (settings.kanaAnswerFormat !== 'choices' || settings.englishAnswerFormat !== 'choices') {
      onUpdate({
        kanaAnswerFormat: 'choices',
        englishAnswerFormat: 'choices',
      });
    }
  }, [settings.kanaAnswerFormat, settings.englishAnswerFormat, onUpdate]);

  const handleToggleReminders = async () => {
  const nextValue = !settings.dailyStudyReminders;
  if (nextValue) {
    const granted = await requestAndTriggerStudyNotification({
      title: 'Daily Kanji Practice Due 漢',
      body: 'Daily study reminders are active! We will remind you every day at 9:00 AM.',
      tag: 'kanji-reminder-enabled',
    });
    if (granted) {
      await scheduleDailyStudyReminder(9, 0);
    }
    onUpdate({ dailyStudyReminders: granted });
  } else {
    await cancelDailyStudyReminder();
    onUpdate({ dailyStudyReminders: false });
  }
};

  return (
    <div className="min-h-screen bg-[#F1F5F9] text-slate-800 pb-12 px-4 pt-4 select-none">
      <div className="max-w-md mx-auto">
        {/* Top Handle & Close */}
        <div className="flex items-center justify-between mb-4">
          <div className="w-8" />
          <div className="w-10 h-1 rounded-full bg-slate-400" />
          <button
            type="button"
            onClick={onClose}
            aria-label="Close settings"
            className="p-1.5 rounded-full hover:bg-slate-200 text-slate-700"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* GENERAL */}
        <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 px-1">
          General
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-4 space-y-5 mb-6">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Auto play audio</span>
            <button
              type="button"
              onClick={() => onUpdate({ autoPlayAudio: !settings.autoPlayAudio })}
              className={`w-12 h-7 rounded-full transition p-1 ${
                settings.autoPlayAudio ? 'bg-[#242933]' : 'bg-slate-200'
              }`}
            >
              <div
                className={`w-5 h-5 rounded-full bg-white shadow transition-transform ${
                  settings.autoPlayAudio ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">Voice</div>
            <div className="grid grid-cols-2 bg-slate-100 rounded-lg p-1">
              {(['male', 'female'] as const).map((v) => (
                <button
                  key={v}
                  type="button"
                  onClick={() => onUpdate({ voice: v })}
                  className={`py-1.5 rounded-md text-xs font-semibold capitalize transition ${
                    settings.voice === v ? 'bg-[#242933] text-white' : 'text-slate-600'
                  }`}
                >
                  {v}
                </button>
              ))}
            </div>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">Font</div>
            <div className="grid grid-cols-2 bg-slate-100 rounded-lg p-1">
              {(['simple', 'stylized'] as const).map((f) => (
                <button
                  key={f}
                  type="button"
                  onClick={() => onUpdate({ font: f })}
                  className={`py-1.5 rounded-md text-xs font-semibold capitalize transition ${
                    settings.font === f ? 'bg-[#242933] text-white' : 'text-slate-600'
                  }`}
                >
                  {f}
                </button>
              ))}
            </div>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">Kana</div>
            <div className="grid grid-cols-2 bg-slate-100 rounded-lg p-1">
              {(['hiragana', 'katakana'] as const).map((k) => (
                <button
                  key={k}
                  type="button"
                  onClick={() => onUpdate({ kana: k })}
                  className={`py-1.5 rounded-md text-xs font-semibold capitalize transition ${
                    settings.kana === k ? 'bg-[#242933] text-white' : 'text-slate-600'
                  }`}
                >
                  {k}
                </button>
              ))}
            </div>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">Lesson questions per word</div>
            <div className="grid grid-cols-7 bg-slate-100 rounded-lg p-1 gap-1">
              {[1, 2, 3, 4, 5, 6, 7].map((num) => (
                <button
                  key={num}
                  type="button"
                  onClick={() => onUpdate({ lessonQuestionsPerWord: num })}
                  className={`py-1.5 rounded-md text-xs font-semibold transition ${
                    settings.lessonQuestionsPerWord === num
                      ? 'bg-[#242933] text-white'
                      : 'text-slate-600'
                  }`}
                >
                  {num}
                </button>
              ))}
            </div>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Writing guide lines</span>
            <button
              type="button"
              onClick={() => onUpdate({ writingGuideLines: !settings.writingGuideLines })}
              className={`w-12 h-7 rounded-full transition p-1 ${
                settings.writingGuideLines ? 'bg-[#242933]' : 'bg-slate-200'
              }`}
            >
              <div
                className={`w-5 h-5 rounded-full bg-white shadow transition-transform ${
                  settings.writingGuideLines ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>
        </div>

        {/* REVIEWS */}
        <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 px-1">
          Reviews
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-4 space-y-5 mb-6">
          <div>
            <div className="text-sm font-medium">Review</div>
            <div className="text-xs text-slate-400">English and Japanese</div>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">Review frequency</div>
            <div className="flex items-center gap-3">
              <span className="text-[11px] text-slate-400">Less</span>
              <input
                type="range"
                min={0.5}
                max={2.0}
                step={0.1}
                value={settings.reviewFrequency}
                onChange={(e) => onUpdate({ reviewFrequency: parseFloat(e.target.value) })}
                className="flex-1 accent-[#242933]"
              />
              <span className="text-[11px] text-slate-400">More</span>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-sm font-medium mb-2">
              <span>Maximum reviews per day:</span>
              <span>{settings.maxReviewsPerDay}</span>
            </div>
            <input
              type="range"
              min={10}
              max={200}
              step={10}
              value={settings.maxReviewsPerDay}
              onChange={(e) => onUpdate({ maxReviewsPerDay: parseInt(e.target.value, 10) })}
              className="w-full accent-[#242933]"
            />
          </div>
        </div>

        {/* ANSWER FORMATS */}
        <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 px-1">
          Answer Formats
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-4 space-y-4 mb-6">
          <div>
            <div className="text-sm font-medium mb-2">Kanji</div>
            <div className="grid grid-cols-2 bg-slate-100 rounded-lg p-1">
              {(['writing', 'choices'] as const).map((fmt) => (
                <button
                  key={fmt}
                  type="button"
                  onClick={() => onUpdate({ kanjiAnswerFormat: fmt })}
                  className={`py-1.5 rounded-md text-xs font-semibold capitalize transition ${
                    settings.kanjiAnswerFormat === fmt ? 'bg-[#242933] text-white' : 'text-slate-600'
                  }`}
                >
                  {fmt}
                </button>
              ))}
            </div>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">Kana</div>
            <div className="bg-slate-100 rounded-lg p-1">
              <button
                type="button"
                onClick={() => onUpdate({ kanaAnswerFormat: 'choices' })}
                className="w-full py-1.5 rounded-md text-xs font-semibold bg-[#242933] text-white transition"
              >
                Choices
              </button>
            </div>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">English</div>
            <div className="bg-slate-100 rounded-lg p-1">
              <button
                type="button"
                onClick={() => onUpdate({ englishAnswerFormat: 'choices' })}
                className="w-full py-1.5 rounded-md text-xs font-semibold bg-[#242933] text-white transition"
              >
                Choices
              </button>
            </div>
          </div>
        </div>

        {/* DAILY GOALS */}
        <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 px-1">
          Daily Goals
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-4 space-y-5 mb-6">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Show Daily Goals</span>
            <button
              type="button"
              onClick={() => onUpdate({ showDailyGoals: !settings.showDailyGoals })}
              className={`w-12 h-7 rounded-full transition p-1 ${
                settings.showDailyGoals ? 'bg-[#242933]' : 'bg-slate-200'
              }`}
            >
              <div
                className={`w-5 h-5 rounded-full bg-white shadow transition-transform ${
                  settings.showDailyGoals ? 'translate-x-5' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          {settings.showDailyGoals && (
            <>
              <div>
                <div className="text-sm font-medium mb-2">Daily lesson goal</div>
                <div className="grid grid-cols-10 bg-slate-100 rounded-lg p-1 gap-0.5">
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                    <button
                      key={num}
                      type="button"
                      onClick={() => onUpdate({ dailyLessonGoal: num })}
                      className={`py-1.5 rounded-md text-xs font-semibold transition ${
                        (settings.dailyLessonGoal ?? 2) === num
                          ? 'bg-[#242933] text-white'
                          : 'text-slate-600'
                      }`}
                    >
                      {num}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Daily Study Reminders</span>
                <button
                  type="button"
                  onClick={handleToggleReminders}
                  className={`w-12 h-7 rounded-full transition p-1 ${
                    settings.dailyStudyReminders ? 'bg-[#242933]' : 'bg-slate-200'
                  }`}
                >
                  <div
                    className={`w-5 h-5 rounded-full bg-white shadow transition-transform ${
                      settings.dailyStudyReminders ? 'translate-x-5' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>
            </>
          )}
        </div>

        {/* OTHER */}
        <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 px-1">
          Other
        </div>
        <div className="bg-white rounded-2xl shadow-sm p-4 mb-4">
          <div className="text-sm font-medium">App Language</div>
          <div className="text-xs text-slate-400">{settings.appLanguage}</div>
        </div>
      </div>
    </div>
  );
};