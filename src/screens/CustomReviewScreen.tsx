import React, { useState } from 'react';
import { X, Settings, Plus } from 'lucide-react';
import type { JLPTLevelId, KanjiLessonItem } from '../types/kanji';

interface CustomReviewScreenProps {
  level: JLPTLevelId;
  learnedItems: KanjiLessonItem[];
  onBack: () => void;
  onOpenSettings: () => void;
  onStartReview: (selectedItems: KanjiLessonItem[]) => void;
}

export const CustomReviewScreen: React.FC<CustomReviewScreenProps> = ({
  level,
  learnedItems,
  onBack,
  onOpenSettings,
  onStartReview,
}) => {
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  const toggleItem = (id: string) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleAddAll = () => {
    if (selectedIds.length === learnedItems.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(learnedItems.map((i) => i.id));
    }
  };

  const handleStart = () => {
    const chosen = learnedItems.filter((i) => selectedIds.includes(i.id));
    if (chosen.length > 0) {
      onStartReview(chosen);
    }
  };

  return (
    <div className="min-h-screen bg-[#242933] text-white flex flex-col justify-between px-5 py-4 select-none">
      <div className="max-w-lg mx-auto w-full">
        {/* Top Bar */}
        <div className="flex items-center justify-between mb-6">
          <button
            type="button"
            onClick={onBack}
            aria-label="Close custom review"
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

        {/* Title */}
        <h1 className="text-center text-2xl font-bold text-[#F5B041] mb-8">
          Select Kanji For Review
        </h1>

        {/* Level Group */}
        <div className="mb-4 text-sm font-semibold text-slate-300">JLPT {level}</div>

        <div className="flex flex-wrap items-center gap-3 mb-5">
          <button
            type="button"
            onClick={handleAddAll}
            title="Select or deselect all"
            className="w-9 h-9 rounded-lg bg-[#333A48] hover:bg-[#3E4759] flex items-center justify-center text-slate-200"
          >
            <Plus className="w-5 h-5" />
          </button>

          {learnedItems.map((item) => {
            const isSelected = selectedIds.includes(item.id);
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => toggleItem(item.id)}
                className={`px-2.5 py-1 rounded-lg text-2xl font-serif transition ${
                  isSelected
                    ? 'bg-[#2ECC71]/20 text-[#2ECC71] ring-2 ring-[#2ECC71]'
                    : 'text-[#2ECC71]/80 hover:bg-[#333A48]'
                }`}
              >
                {item.word}
              </button>
            );
          })}
        </div>

        <button
          type="button"
          onClick={handleAddAll}
          className="px-6 py-2 rounded-lg bg-[#333A48] hover:bg-[#3E4759] text-sm font-medium text-slate-100 transition"
        >
          {selectedIds.length === learnedItems.length && learnedItems.length > 0
            ? 'Clear All'
            : 'Add All'}
        </button>
      </div>

      {/* Start Custom Review Button */}
      <div className="max-w-lg mx-auto w-full pb-3">
        <button
          type="button"
          disabled={selectedIds.length === 0}
          onClick={handleStart}
          className="w-full py-3.5 rounded-xl bg-[#2ECC71] hover:bg-[#27AE60] disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold text-lg shadow-md transition"
        >
          Start Review ({selectedIds.length})
        </button>
      </div>
    </div>
  );
};