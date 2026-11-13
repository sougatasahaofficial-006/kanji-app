# Project Blueprint: Kanji Master (JLPT N5–N1)

## 1. Executive Summary
**Kanji Master** is a 100% offline-first, cross-platform Japanese Kanji and vocabulary study application covering the complete **JLPT N5 through N1 curriculum** (**1,275 structured lessons** and **2,128 unique root Kanji**). Built with React, TypeScript, Vite, Tailwind CSS, and Capacitor for Android, the application pairs build-time Python curriculum and neural TTS audio pipelines with a client-side SM-2 Spaced Repetition System (SRS), interactive stroke-writing drills, daily streak tracking, native notifications, and serverless cross-device JSON backup and restore.

---

## 2. Core Features
- **Complete JLPT N5–N1 Curriculum:** 1,275 sequential lessons spanning 2,128 unique root Kanji with On'yomi/Kun'yomi readings, meanings, and progressive unlock paths.
- **Adaptive Spaced Repetition System (SRS):** SM-2 inspired scheduling engine with customizable review frequency multipliers (`0.5x`–`2.0x`) and daily review caps (`10`–`200`).
- **Interactive Multi-Mode Study Drills:** Supports Kanji handwriting canvas (with toggleable writing guide lines), Kanji multiple-choice, Kana reading choices, and English meaning choices, plus customizable questions per word (`1`–`7`).
- **Zero-Latency Offline Neural Audio:** Bundled male (`ja-JP-KeitaNeural`) and female (`ja-JP-NanamiNeural`) MP3 pronunciations generated at build time for instant offline playback.
- **Canonical Root-Kanji Directory:** Global searchable/grouped directory displaying every unique root Kanji deduplicated across N5 → N1 in canonical learning order.
- **Daily Goals & Streak Calendar:** Interactive daily checklist (`Review` + `N` target lessons) paired with a monthly `S M T W T F S` completion calendar.
- **Native Study Reminders:** Scheduled local background notifications via Capacitor Local Notifications and Service Worker fallback.
- **Cross-Device JSON Backup & Restore:** Account-free state portability allowing users to export and restore their complete progress (learned lessons, SRS intervals, streaks, and settings) across Android and web browsers via `.json` snapshots.

---

## 3. Tech Stack & Native Integrations

| Layer | Technologies & Libraries |
| :--- | :--- |
| **Frontend Framework** | React 18, TypeScript (`verbatimModuleSyntax`), Vite |
| **Styling & UI** | Tailwind CSS (`#242933` dark slate study theme + `#F1F5F9` light settings surfaces), `lucide-react` |
| **Mobile Runtime (Android)** | Capacitor (`@capacitor/core`, `@capacitor/android`) |
| **Native Plugins** | `@capacitor/local-notifications`, `@capacitor/filesystem`, `@capacitor/share` |
| **Build-Time Data & Audio** | Python 3, `edge-tts` (neural Japanese TTS), `manifest.json` integrity tracking |
| **Client Persistence** | Browser `localStorage` (`kanji_app_state_v1`) + Service Worker (`public/sw.js`) |

---

## 4. Project Structure

```text
kanji-app/
├── android/                        # Native Android Capacitor project & Gradle configs
├── public/
│   ├── audio/
│   │   ├── male/                   # Offline neural male MP3 pronunciations (<id>-male.mp3)
│   │   ├── female/                 # Offline neural female MP3 pronunciations (<id>-female.mp3)
│   │   └── manifest.json           # Checksum/kana manifest preventing stale audio mismatches
│   └── sw.js                       # Service Worker for web/desktop study reminder notifications
├── src/
│   ├── components/
│   │   ├── KanjiCanvas.tsx         # Interactive touch/mouse handwriting pad with guide lines
│   │   ├── KanjiGridOverlay.tsx    # Deduplicated N5–N1 canonical root-Kanji directory
│   │   └── SessionRunner.tsx       # Multi-step lesson & SRS review quiz engine
│   ├── data/
│   │   ├── n5.ts                   # JLPT N5 dataset (54 lessons | 111 root Kanji)
│   │   ├── n4.ts                   # JLPT N4 dataset (95 lessons | 146 root Kanji)
│   │   ├── n3.ts                   # JLPT N3 dataset (345 lessons | 379 root Kanji)
│   │   ├── n2.ts                   # JLPT N2 dataset (222 lessons | 377 root Kanji)
│   │   └── n1.ts                   # JLPT N1 dataset (559 lessons | 1,115 root Kanji)
│   ├── screens/
│   │   ├── HomeScreen.tsx          # Level 1–5 circular Kanji selector with progress rings
│   │   ├── LevelScreen.tsx         # Daily Goals card, monthly streak calendar & lesson roadmap
│   │   ├── CustomReviewScreen.tsx  # Targeted review builder for learned vocabulary
│   │   └── SettingsScreen.tsx      # Audio, typography, SRS, Daily Goals & Backup/Restore UI
│   ├── store/
│   │   └── useAppStore.ts          # Centralized localStorage state, SRS & Daily Goals engine
│   ├── types/
│   │   └── kanji.ts                # Core TypeScript schemas (KanjiLesson, AppSettings, KanjiBackupFile)
│   └── utils/
│       ├── backup.ts               # Cross-platform JSON state export, validation & atomic restore
│       ├── notifications.ts        # Capacitor & Service Worker notification scheduler
│       └── speech.ts               # Dual-voice offline MP3 audio player with Web Speech fallback
├── BLUEPRINT.md                    # Technical architecture & system documentation
├── README.md                       # Repository overview, setup & usage guide
├── capacitor.config.ts             # Capacitor native app configuration
├── generate_audio.py               # Batch neural TTS audio & manifest generator
└── package.json

## 5. System Architecture & Workflows

### A. Static Build-Time Data & Audio Pipeline
* **Curriculum Datasets (`src/data/`):** Each level (`n5.ts` – `n1.ts`) exports an array of `KanjiLesson` objects (`id`, `lessonNumber`, `items[]` containing `id`, `word`, `kana`, and `meaning`).
* **Neural Audio Synthesis (`generate_audio.py`):** Iterates across all vocabulary items, generates `<id>-male.mp3` and `<id>-female.mp3` directly from exact `kana` readings using `edge-tts`, and records generated entries in `public/audio/manifest.json` to prevent stale pronunciations.
* **Runtime Playback (`speech.ts`):** Plays bundled local MP3s instantaneously based on the selected voice (`male` or `female`) and `autoPlayAudio` setting, with Web Speech fallback.

### B. State Management & SM-2 SRS Engine (`src/store/useAppStore.ts`)
* **Spaced Repetition Scheduling:** Tracks `intervalDays`, `easeFactor`, `repetitions`, and `nextReviewTimestamp` per item. Successful recalls scale intervals by `easeFactor` and `reviewFrequency` (`0.5x` – `2.0x`), while missed items reset to short-term re-learning queues within `maxReviewsPerDay` (`10` – `200`).
* **Daily Goals & Streaks:** Locks `N` target lessons per level each day (`dailyTargetLessonIds`), tracks review completion (`dailyReviewsCompleted`), and marks calendar dates (`goalCompletedDates`) once daily reviews and target lessons finish.

### C. Study Views & Navigation (`src/screens/` & `src/components/`)
* **Level & Roadmap Flow:** `HomeScreen.tsx` displays JLPT Level 1–5 progress rings; `LevelScreen.tsx` renders sub-section selectors (N3–N1), the **Daily Goals & Monthly Calendar Card**, **Review Past Due**, **Custom Review**, and sequential lesson nodes.
* **Quiz & Canvas Engine:** `SessionRunner.tsx` builds dynamic question queues (`1`–`7` per item) across Kanji (`KanjiCanvas.tsx` writing pad or multiple-choice), Kana, and English meanings.
* **Root-Kanji Directory:** `KanjiGridOverlay.tsx` deduplicates all Kanji characters across N5 → N1 in canonical order into a grouped reference grid.

### D. Native Android Integration & Notifications (`src/utils/notifications.ts` & `public/sw.js`)
* **Android (Capacitor):** Schedules daily local reminders via `@capacitor/local-notifications` (defaulting to 9:00 AM daily) and handles display cutout safe areas alongside hierarchical hardware back-button navigation.
* **Web/Desktop:** Uses `public/sw.js` with dynamic Canvas-rendered Kanji icons for desktop/browser reminders.

### E. Cross-Device JSON Backup & Restore (`src/utils/backup.ts`)
* **Export (`exportAppBackup`):** Serializes all `localStorage` entries into a versioned `KanjiBackupFile` envelope (`app: "KanjiMaster"`, `schemaVersion: 1`, `exportedAt`, and `data`). On Android, it writes `kanji-master-backup-YYYY-MM-DD.json` to `Directory.Cache` via `@capacitor/filesystem` and opens the native Share sheet via `@capacitor/share`; on web browsers, it triggers a direct `.json` file download.
* **Restore (`importAppBackup`):** Parses user-selected `.json` files, validates the `"KanjiMaster"` signature and payload structure prior to mutating storage, restores all `localStorage` keys atomically, and reloads the application state.