# Project Blueprint: Kanji Study App (JLPT N5–N1)

## 1. Overview & Purpose
An offline-first, interactive Japanese Kanji and vocabulary learning application covering the complete **JLPT N5 through N1 curriculum** (**1,275 lessons** and **2,128 unique root Kanji**). Built with React, TypeScript, Vite, and Tailwind CSS, featuring native offline neural audio, an SM-2 Spaced Repetition System (SRS), handwriting/multiple-choice drills, a canonical root-Kanji directory, Daily Goals with calendar streak tracking, and Service Worker push reminders.

---

## 2. Tech Stack & Dependencies
- **Frontend Framework:** React 18 + TypeScript + Vite
- **Styling:** Tailwind CSS (dark slate `#242933` primary study theme + crisp `#F1F5F9` settings surfaces)
- **Icons:** `lucide-react`
- **Offline Audio Generation:** Python + `edge-tts` (`ja-JP-KeitaNeural` male & `ja-JP-NanamiNeural` female voices)
- **Persistence & Background:** Browser `localStorage` (`kanji_app_state_v1`) + Service Worker (`public/sw.js`)

---

## 3. Curriculum Dataset Architecture (`src/data/`)
All lessons follow a unified `KanjiLesson` schema (`id`, `lessonNumber`, `items[]` with `id`, `word`, `kana`, `meaning`):
- **`src/data/n5.ts`**: 54 lessons | 111 unique root Kanji (`一` → `円`)
- **`src/data/n4.ts`**: 95 lessons | 146 unique root Kanji (`明` → `遠`)
- **`src/data/n3.ts`**: 345 lessons | 379 unique root Kanji (`笑` → `乾`)
- **`src/data/n2.ts`**: 222 lessons | 377 unique root Kanji (`軍` → `撮`)
- **`src/data/n1.ts`**: 559 lessons | 1,115 unique root Kanji (`視` → `遜`)
- **Total:** **1,275 lessons** | **2,128 unique root Kanji**

---

## 4. Core Modules & Screens

### A. State & Spaced Repetition Engine (`src/store/useAppStore.ts`)
- **SRS Scheduling:** SM-2 inspired algorithm tracking `intervalDays`, `easeFactor`, `repetitions`, and `nextReviewTimestamp`, scaled dynamically by `reviewFrequency` (`0.5x` – `2.0x`) and capped per session by `maxReviewsPerDay` (`10` – `200`).
- **Daily Goals Engine:** Locks in `N` target lessons per level each day (`dailyTargetLessonIds`), tracks daily review completion (`dailyReviewsCompleted`), and marks calendar dates (`goalCompletedDates`) once both daily reviews and target lessons are finished.

### B. Views & Components (`src/screens/` & `src/components/`)
- **`HomeScreen.tsx`**: JLPT Level 1 (N5) through Level 5 (N1) circular Kanji badges with progress rings and quick access to the global Kanji directory and Settings.
- **`LevelScreen.tsx`**:
  - Sub-section selector for large levels (N3, N2, N1).
  - **Daily Goals Card**: Two-column card with interactive checklist (`Review` + today's target lessons) and a monthly `S M T W T F S` progress calendar grid.
  - Sequential lesson roadmap with unlock progression, **Review Past Due (X)**, and **Custom Review** triggers.
- **`KanjiGridOverlay.tsx`**: Three-line directory view displaying every unique root Kanji grouped by its canonical JLPT level (deduplicated across N5 → N1 in canonical order).
- **`SessionRunner.tsx`**: Multi-question study and review engine supporting Kanji (`Writing` with optional guide lines or `Choices`), Kana (`Choices`), and English (`Choices`), plus auto-playing male/female audio.
- **`CustomReviewScreen.tsx`**: Filterable review builder allowing targeted practice of learned vocabulary per level.
- **`SettingsScreen.tsx`**: Controls for Audio (`Auto play`, `Voice`), Typography (`Simple`/`Stylized` font, `Hiragana`/`Katakana`), Lesson length (`1–7` questions/word), Writing guide lines, SRS tuning (`Review frequency`, `Maximum reviews per day`), Answer formats, and Daily Goals (`Show Daily Goals`, `Daily lesson goal 1–10`, `Daily Study Reminders`, and `Send Test Notification`).

### C. Offline Audio & Notifications (`public/` & `src/utils/`)
- **`generate_audio.py` & `public/audio/`**: Generates `<id>-male.mp3` and `<id>-female.mp3` directly from exact `kana` readings, tracked via `public/audio/manifest.json` to prevent stale audio mismatches.
- **`public/sw.js` & `src/utils/notifications.ts`**: Registers the Service Worker, renders dynamic Canvas Kanji notification icons, and dispatches rich desktop/Android study reminder notifications.