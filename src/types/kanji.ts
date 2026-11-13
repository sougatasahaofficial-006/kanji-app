export type JLPTLevelId = 'N5' | 'N4' | 'N3' | 'N2' | 'N1';

export interface CharacterStrokeData {
  char: string;
  strokes: string[]; // SVG path 'd' attributes on a 109x109 KanjiVG viewBox
}

export interface KanjiLessonItem {
  id: string;
  level?: JLPTLevelId;
  word: string; // e.g., "一", "白い", "今日"
  kana: string; // Primary hiragana reading, e.g., "いち", "しろい", "きょう"
  meaning: string; // Primary English meaning, e.g., "one", "white", "today"
  onyomi: string[]; // Katakana readings, e.g., ["イチ", "イツ"]
  kunyomi: string[]; // Hiragana readings, e.g., ["ひと-", "ひと.つ"]
  characters: CharacterStrokeData[]; // Supports single Kanji, okurigana conjugations, and compounds
}

export interface KanjiLesson {
  id: string;
  lessonNumber: number;
  level: JLPTLevelId;
  items: KanjiLessonItem[]; // Strictly 5 items per lesson
}

export interface JLPTLevelInfo {
  id: JLPTLevelId;
  levelNumber: number;
  label: string;
  badgeKanji: string;
  badgeColor: string;
  totalKanjiCount: number;
}

export interface AppSettings {
  autoPlayAudio: boolean;
  voice: 'male' | 'female';
  font: 'simple' | 'stylized';
  kana: 'hiragana' | 'katakana';
  lessonQuestionsPerWord: number; // 1 to 7
  writingGuideLines: boolean;
  reviewFrequency: number; // 0.5 (Less) to 2.0 (More)
  maxReviewsPerDay: number; // Default 100
  kanjiAnswerFormat: 'writing' | 'choices';
  kanaAnswerFormat: 'choices' | 'selfGrade';
  englishAnswerFormat: 'choices' | 'selfGrade';
  showDailyGoals: boolean;
  appLanguage: string;
}

export interface SRSItemProgress {
  itemId: string;
  level: JLPTLevelId;
  intervalDays: number;
  easeFactor: number;
  nextReviewTimestamp: number;
  repetitions: number;
}
export const JLPT_LEVELS: JLPTLevelInfo[] = [
  {
    id: 'N5',
    levelNumber: 1,
    label: 'JLPT N5',
    badgeKanji: '雨',
    badgeColor: '#5DA9E9',
    totalKanjiCount: 110,
  },
  {
    id: 'N4',
    levelNumber: 2,
    label: 'JLPT N4',
    badgeKanji: '風',
    badgeColor: '#F59E0B',
    totalKanjiCount: 170,
  },
  {
    id: 'N3',
    levelNumber: 3,
    label: 'JLPT N3',
    badgeKanji: '桜',
    badgeColor: '#2ECC71',
    totalKanjiCount: 370,
  },
  {
    id: 'N2',
    levelNumber: 4,
    label: 'JLPT N2',
    badgeKanji: '島',
    badgeColor: '#F24949',
    totalKanjiCount: 380,
  },
  {
    id: 'N1',
    levelNumber: 5,
    label: 'JLPT N1',
    badgeKanji: '藤',
    badgeColor: '#4DB6AC',
    totalKanjiCount: 1100,
  },
];
export interface JLPTSubsectionInfo {
  id: string;
  startLesson: number;
  endLesson: number;
  label: string;
  badgeKanji: string;
}

export const JLPT_SUBSECTIONS: Record<JLPTLevelId, JLPTSubsectionInfo[]> = {
  N5: [],
  N4: [
    { id: 'n4-1', startLesson: 1, endLesson: 50, label: 'Lessons 1 - 50', badgeKanji: '明' },
    { id: 'n4-2', startLesson: 51, endLesson: 95, label: 'Lessons 51 - 95', badgeKanji: '動' },
  ],
  N3: [
    { id: 'n3-1', startLesson: 1, endLesson: 50, label: 'Lessons 1 - 50', badgeKanji: '笑' },
    { id: 'n3-2', startLesson: 51, endLesson: 100, label: 'Lessons 51 - 100', badgeKanji: '礼' },
    { id: 'n3-3', startLesson: 101, endLesson: 150, label: 'Lessons 101 - 150', badgeKanji: '必' },
    { id: 'n3-4', startLesson: 151, endLesson: 200, label: 'Lessons 151 - 200', badgeKanji: '誰' },
    { id: 'n3-5', startLesson: 201, endLesson: 250, label: 'Lessons 201 - 250', badgeKanji: '非' },
    { id: 'n3-6', startLesson: 251, endLesson: 300, label: 'Lessons 251 - 300', badgeKanji: '易' },
    { id: 'n3-7', startLesson: 301, endLesson: 345, label: 'Lessons 301 - 345', badgeKanji: '者' },
  ],
  N2: [
    { id: 'n2-1', startLesson: 1, endLesson: 50, label: 'Lessons 1 - 50', badgeKanji: '軍' },
    { id: 'n2-2', startLesson: 51, endLesson: 100, label: 'Lessons 51 - 100', badgeKanji: '森' },
    { id: 'n2-3', startLesson: 101, endLesson: 150, label: 'Lessons 101 - 150', badgeKanji: '固' },
    { id: 'n2-4', startLesson: 151, endLesson: 200, label: 'Lessons 151 - 200', badgeKanji: '狙' },
    { id: 'n2-5', startLesson: 201, endLesson: 222, label: 'Lessons 201 - 222', badgeKanji: '枯' },
  ],
  N1: [
    { id: 'n1-1', startLesson: 1, endLesson: 50, label: 'Lessons 1 - 50', badgeKanji: '視' },
    { id: 'n1-2', startLesson: 51, endLesson: 100, label: 'Lessons 51 - 100', badgeKanji: '街' },
    { id: 'n1-3', startLesson: 101, endLesson: 150, label: 'Lessons 101 - 150', badgeKanji: '郷' },
    { id: 'n1-4', startLesson: 151, endLesson: 200, label: 'Lessons 151 - 200', badgeKanji: '摘' },
    { id: 'n1-5', startLesson: 201, endLesson: 250, label: 'Lessons 201 - 250', badgeKanji: '誠' },
    { id: 'n1-6', startLesson: 251, endLesson: 300, label: 'Lessons 251 - 300', badgeKanji: '罰' },
    { id: 'n1-7', startLesson: 301, endLesson: 350, label: 'Lessons 301 - 350', badgeKanji: '蓋' },
    { id: 'n1-8', startLesson: 351, endLesson: 400, label: 'Lessons 351 - 400', badgeKanji: '桟' },
    { id: 'n1-9', startLesson: 401, endLesson: 450, label: 'Lessons 401 - 450', badgeKanji: '媛' },
    { id: 'n1-10', startLesson: 451, endLesson: 500, label: 'Lessons 451 - 500', badgeKanji: '梨' },
    { id: 'n1-11', startLesson: 501, endLesson: 550, label: 'Lessons 501 - 550', badgeKanji: '熊' },
    { id: 'n1-12', startLesson: 551, endLesson: 559, label: 'Lessons 551 - 559', badgeKanji: '闘' },
  ],
};
export interface AppSettings {
  autoPlayAudio: boolean;
  voice: 'male' | 'female';
  font: 'simple' | 'stylized';
  kana: 'hiragana' | 'katakana';
  lessonQuestionsPerWord: number;
  writingGuideLines: boolean;
  reviewFrequency: number;
  maxReviewsPerDay: number;
  kanjiAnswerFormat: 'writing' | 'choices';
  kanaAnswerFormat: 'choices' | 'selfGrade';
  englishAnswerFormat: 'choices' | 'selfGrade';
  showDailyGoals: boolean;
  dailyLessonGoal: number;
  dailyStudyReminders: boolean;
  appLanguage: string;
}