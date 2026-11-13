# Kanji Study App (JLPT N5–N1) 漢

A complete, offline-capable Japanese Kanji and vocabulary learning application covering **JLPT N5 through N1** (**1,275 lessons** and **2,128 unique root Kanji**). Built from the ground up with React, TypeScript, Vite, Tailwind CSS, and Python-generated native Japanese neural audio.

---

## 📖 Project Documentary: From Scratch to Completion

### Phase 1: Architecture & Core Learning Engine
The project began with designing a clean, distraction-free study experience modeled around structured JLPT progression:
- **Scaffolded the React + TypeScript + Vite architecture** with Tailwind CSS styling, state persistence in `localStorage`, and modular screens (`HomeScreen`, `LevelScreen`, `SessionRunner`, `CustomReviewScreen`, and `SettingsScreen`).
- **Built the Spaced Repetition System (SRS)** in `useAppStore.ts`, tracking ease factors, repetition streaks, and dynamic review intervals (`Review frequency` scaling from `0.5x` to `2.0x` and `Maximum reviews per day` batch limits).
- **Implemented multi-mode testing** in `SessionRunner.tsx`, supporting interactive Kanji handwriting canvases (with toggleable writing guide lines), multiple-choice drills for Kana and English meanings, and customizable questions per word (`1–7`).

### Phase 2: Compiling the Complete JLPT N5–N1 Curriculum
To make the app genuinely comprehensive for every JLPT tier, the entire curriculum dataset was digitized, structured, and verified lesson by lesson:
- **JLPT N5 (`src/data/n5.ts`):** 54 lessons covering 111 foundational root Kanji (`一` to `円`).
- **JLPT N4 (`src/data/n4.ts`):** 95 lessons covering 146 elementary root Kanji (`明` to `遠`).
- **JLPT N3 (`src/data/n3.ts`):** 345 lessons covering 379 intermediate root Kanji (`笑` to `乾`).
- **JLPT N2 (`src/data/n2.ts`):** 222 lessons covering 377 pre-advanced root Kanji (`軍` to `撮`).
- **JLPT N1 (`src/data/n1.ts`):** Compiled all 559 advanced lessons covering 1,115 root Kanji (`視` to `遜`).
- **Canonical Directory Deduplication (`KanjiGridOverlay.tsx`):** Engineered the three-line Kanji directory to extract and deduplicate root Kanji in canonical order (N5 → N1), resulting in **2,128 unique root Kanji** (99.6% of the official 2,136 Jōyō Kanji standard).

### Phase 3: Offline Neural Audio Pipeline
Rather than relying on inconsistent browser speech synthesis, a dedicated Python audio generation pipeline (`generate_audio.py`) was built using `edge-tts`:
- Synthesizes two native Japanese voices for every single vocabulary item across N5–N1: **Male (`ja-JP-KeitaNeural`)** and **Female (`ja-JP-NanamiNeural`)**.
- Generates pronunciation directly from each word's exact `kana` reading to prevent Kanji homograph mispronunciations, backed by a `manifest.json` integrity tracker inside `public/audio/`.

### Phase 4: Daily Goals, Calendar Streaks & Push Notifications
To support consistent daily study habits on both desktop and mobile devices:
- **Daily Goals Card (`LevelScreen.tsx`):** Added a two-column dashboard card pairing an interactive daily checklist (`Review` + `1–10` daily target lessons) with a live monthly `S M T W T F S` progress calendar grid that highlights completed study days.
- **Service Worker Notifications (`public/sw.js` & `src/utils/notifications.ts`):** Built a Service Worker notification system with dynamically generated Canvas Kanji icons, vibration patterns, and action buttons (`Start Practice` / `Later`) to alert learners when daily reviews or target lessons are due.
- **Full System Audit:** Verified all 1,275 lessons, 2,128 root Kanji, offline audio assets, SRS calculations, and Service Worker notification permissions.

---

## 📊 Curriculum Breakdown

| JLPT Level | App Level | Lessons | Unique Root Kanji | First → Last Kanji |
| :--- | :--- | :---: | :---: | :---: |
| **JLPT N5** | Level 1 | 54 | 111 | `一` → `円` |
| **JLPT N4** | Level 2 | 95 | 146 | `明` → `遠` |
| **JLPT N3** | Level 3 | 345 | 379 | `笑` → `乾` |
| **JLPT N2** | Level 4 | 222 | 377 | `軍` → `撮` |
| **JLPT N1** | Level 5 | 559 | 1,115 | `視` → `遜` |
| **Total** | **All Levels** | **1,275** | **2,128** | **Full Jōyō Coverage** |

---

## 🚀 Getting Started (Local Development)

### Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Python 3.10+](https://www.python.org/) (only required if regenerating audio files)

### 1. Install Dependencies & Run
```bash
npm install
npm run dev
Open http://localhost:5173 in your browser.

2. Regenerate Offline Audio (Optional)
If you add or edit lessons in src/data/*.ts, run the audio generator to update any new or modified .mp3 clips:

Bash
pip install edge-tts
python generate_audio.py
📁 Project Structure
Plaintext
kanji-app/
├── public/
│   ├── audio/              # Offline male & female MP3 pronunciations + manifest.json
│   └── sw.js               # Service Worker for Android/Desktop study notifications
├── src/
│   ├── components/
│   │   ├── KanjiGridOverlay.tsx   # Deduplicated N5–N1 root Kanji directory
│   │   └── SessionRunner.tsx      # Interactive lesson & SRS review engine
│   ├── data/
│   │   ├── n5.ts ... n1.ts        # Complete 1,275-lesson JLPT curriculum
│   ├── screens/
│   │   ├── HomeScreen.tsx         # Level 1–5 selector
│   │   ├── LevelScreen.tsx        # Daily Goals card, calendar & lesson roadmap
│   │   ├── CustomReviewScreen.tsx # Targeted review builder
│   │   └── SettingsScreen.tsx     # Audio, typography, SRS & Daily Goals settings
│   ├── store/
│   │   └── useAppStore.ts         # localStorage persistence, SRS & Daily Goals logic
│   ├── types/
│   │   └── kanji.ts               # Core TypeScript interfaces & JLPT metadata
│   └── utils/
│       ├── notifications.ts       # Service Worker notification dispatcher
│       └── speech.ts              # Offline MP3 audio player with fallback
├── BLUEPRINT.md            # Technical architecture & feature blueprint
├── generate_audio.py       # Batch neural TTS audio generator
└── package.json