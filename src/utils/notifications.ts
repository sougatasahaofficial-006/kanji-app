const LAST_NOTIFIED_KEY = 'kanji_app_last_reminder_date';

function createKanjiNotificationIcon(size = 192, monochrome = false): string {
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  if (!ctx) return '';

  if (monochrome) {
    // Transparent background + white Kanji for Android top status-bar small icon
    ctx.clearRect(0, 0, size, size);
    ctx.fillStyle = '#FFFFFF';
  } else {
    // Rounded sky-blue badge with crisp white Kanji for Android notification shade
    const radius = size * 0.24;
    ctx.fillStyle = '#5DA9E9';
    ctx.beginPath();
    ctx.roundRect(0, 0, size, size, radius);
    ctx.fill();
    ctx.fillStyle = '#FFFFFF';
  }

  ctx.font = `bold ${Math.round(size * 0.58)}px serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('漢', size / 2, size / 2 + size * 0.04);

  return canvas.toDataURL('image/png');
}

export async function ensureNotificationServiceWorker(): Promise<ServiceWorkerRegistration | null> {
  if (!('serviceWorker' in navigator)) return null;
  try {
    const reg = await navigator.serviceWorker.register('/sw.js');
    await navigator.serviceWorker.ready;
    return reg;
  } catch (err) {
    console.warn('Service worker registration failed:', err);
    return null;
  }
}

export async function requestAndTriggerStudyNotification(options: {
  title: string;
  body: string;
  tag?: string;
}): Promise<boolean> {
  if (!('Notification' in window)) return false;

  let permission = Notification.permission;
  if (permission === 'default') {
    permission = await Notification.requestPermission();
  }
  if (permission !== 'granted') return false;

  const icon = createKanjiNotificationIcon(192, false);
  const badge = createKanjiNotificationIcon(96, true);

  const notificationOptions: NotificationOptions & {
    renotify?: boolean;
    vibrate?: number[];
    actions?: { action: string; title: string }[];
  } = {
    body: options.body,
    icon,
    badge,
    tag: options.tag || 'kanji-daily-practice',
    renotify: true,
    vibrate: [120, 60, 120],
    actions: [
      { action: 'practice', title: 'Start Practice' },
      { action: 'dismiss', title: 'Later' },
    ],
  };

  const reg = await ensureNotificationServiceWorker();
  if (reg && 'showNotification' in reg) {
    await reg.showNotification(options.title, notificationOptions);
    return true;
  }

  // Fallback for desktop browsers without Service Worker
  new Notification(options.title, {
    body: options.body,
    icon,
    tag: options.tag || 'kanji-daily-practice',
  });
  return true;
}

export async function checkAndNotifyDailyPracticeDue(params: {
  enabled: boolean;
  dueCount: number;
  remainingLessons: number;
  isGoalCompleteToday: boolean;
}) {
  if (!params.enabled || params.isGoalCompleteToday) return;
  if (params.dueCount === 0 && params.remainingLessons === 0) return;

  const today = new Date().toISOString().split('T')[0];
  const lastNotified = window.localStorage.getItem(LAST_NOTIFIED_KEY);
  if (lastNotified === today) return;

  const parts: string[] = [];
  if (params.dueCount > 0) {
    parts.push(`${params.dueCount} Kanji review${params.dueCount === 1 ? '' : 's'} due`);
  }
  if (params.remainingLessons > 0) {
    parts.push(`${params.remainingLessons} lesson${params.remainingLessons === 1 ? '' : 's'} left for today's goal`);
  }

  const sent = await requestAndTriggerStudyNotification({
    title: 'Daily Kanji Practice Due 漢',
    body: `${parts.join(' • ')}. Tap to keep your streak alive!`,
    tag: 'kanji-daily-practice',
  });

  if (sent) {
    window.localStorage.setItem(LAST_NOTIFIED_KEY, today);
  }
}