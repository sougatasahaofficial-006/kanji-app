import React from 'react';
import { List, Settings } from 'lucide-react';
import type { JLPTLevelId, JLPTLevelInfo } from '../types/kanji';
import { JLPT_LEVELS } from '../types/kanji';

interface HomeScreenProps {
  onSelectLevel: (level: JLPTLevelId) => void;
  onOpenAllKanji: () => void;
  onOpenSettings: () => void;
}

export const HomeScreen: React.FC<HomeScreenProps> = ({
  onSelectLevel,
  onOpenAllKanji,
  onOpenSettings,
}) => {
  return (
    <div className="min-h-screen bg-[#242933] text-white flex flex-col select-none">
      {/* Top Bar with Three-Line List Icon & Settings Gear */}
      <div className="sticky top-0 z-10 bg-[#242933]/95 backdrop-blur px-5 py-4 flex items-center justify-end max-w-lg mx-auto w-full">
        <div className="flex items-center gap-4">
          <button
            type="button"
            onClick={onOpenAllKanji}
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

      {/* Level Badges */}
      <div className="flex-1 flex flex-col items-center pb-10 px-4">
        <div className="flex flex-col items-center space-y-8 w-full max-w-sm">
          {JLPT_LEVELS.map((lvl: JLPTLevelInfo) => (
            <button
              key={lvl.id}
              type="button"
              onClick={() => onSelectLevel(lvl.id)}
              className="group flex flex-col items-center focus:outline-none"
            >
              <div
                className="w-36 h-36 rounded-full flex items-center justify-center shadow-lg transition-transform duration-200 group-hover:scale-105 group-active:scale-95"
                style={{ backgroundColor: lvl.badgeColor }}
              >
                <span className="text-7xl font-serif text-white leading-none">
                  {lvl.badgeKanji}
                </span>
              </div>
              <span className="mt-2.5 text-sm font-bold text-white tracking-wide">
                Level {lvl.levelNumber}
              </span>
              <span className="text-xs text-slate-300">{lvl.label}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};