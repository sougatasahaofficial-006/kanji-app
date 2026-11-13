import { Capacitor } from '@capacitor/core';
import { Filesystem, Directory, Encoding } from '@capacitor/filesystem';
import { Share } from '@capacitor/share';
import type { KanjiBackupFile } from '../types/kanji';

export async function exportAppBackup(): Promise<void> {
  const data: Record<string, unknown> = {};

  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (!key) continue;
    const raw = localStorage.getItem(key);
    if (raw === null) continue;
    try {
      data[key] = JSON.parse(raw);
    } catch {
      data[key] = raw;
    }
  }

  const payload: KanjiBackupFile = {
    app: 'KanjiMaster',
    schemaVersion: 1,
    exportedAt: new Date().toISOString(),
    data,
  };

  const jsonString = JSON.stringify(payload, null, 2);
  const fileName = `kanji-master-backup-${new Date().toISOString().slice(0, 10)}.json`;

  if (Capacitor.isNativePlatform()) {
    const written = await Filesystem.writeFile({
      path: fileName,
      data: jsonString,
      directory: Directory.Cache,
      encoding: Encoding.UTF8,
    });

    await Share.share({
      title: 'Kanji Master Progress Backup',
      files: [written.uri],
      dialogTitle: 'Save or Send Backup File',
    });
  } else {
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = fileName;
    link.click();
    URL.revokeObjectURL(url);
  }
}

export async function importAppBackup(file: File): Promise<{ ok: boolean; error?: string }> {
  try {
    const text = await file.text();
    const parsed = JSON.parse(text) as Partial<KanjiBackupFile>;

    if (parsed.app !== 'KanjiMaster' || typeof parsed.data !== 'object' || parsed.data === null) {
      return { ok: false, error: 'Invalid file. Please select a valid Kanji Master backup (.json).' };
    }

    localStorage.clear();
    for (const [key, value] of Object.entries(parsed.data)) {
      localStorage.setItem(key, typeof value === 'string' ? value : JSON.stringify(value));
    }

    return { ok: true };
  } catch {
    return { ok: false, error: 'Could not read the backup file. Make sure it is not corrupted.' };
  }
}