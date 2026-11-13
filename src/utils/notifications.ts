import { Capacitor } from '@capacitor/core';
import { LocalNotifications } from '@capacitor/local-notifications';

const LAST_NOTIFIED_KEY = 'kanji_app_last_reminder_date';
const DAILY_REMINDER_ID = 1001;
const INSTANT_NOTIFICATION_BASE_ID = 2000;

function createKanjiNotificationIcon(size = 192, monochrome = false): string {
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  if (!ctx) return '';

  if (monochrome) {
    ctx.clearRect(0, 0, size, size);
    ctx.fillStyle = '#FFFFFF';
  } else {
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

async function ensureNativePermission(): Promise<boolean> {
  try {
    let status = await LocalNotifications.checkPermissions();
    if (status.display !== 'granted') {
      status = await LocalNotifications.requestPermissions();
    }
    return status.display === 'granted';
  } catch (err) {
    console.warn('Native notification permission failed:', err);
    return false;
  }
}

export async function scheduleDailyStudyReminder(hour = 9, minute = 0): Promise<boolean> {
  if (!Capacitor.isNativePlatform()) return true;

  const granted = await ensureNativePermission();
  if (!granted) return false;

  try {
    await LocalNotifications.cancel({ notifications: [{ id: DAILY_REMINDER_ID }] });

    await LocalNotifications.schedule({
      notifications: [
        {
          id: DAILY_REMINDER_ID,
          title: 'Daily Kanji Practice Due 漢',
          body: 'Your daily Kanji lessons & SRS reviews are waiting. Keep your streak alive!',
          schedule: {
            on: { hour, minute },
            repeats: true,
            allowWhileIdle: true,
          },
          smallIcon: 'ic_stat_icon_config_sample',
          iconColor: '#5DA9E9',
        },
      ],
    });
    return true;
  } catch (err) {
    console.warn('Failed to schedule daily native reminder:', err);
    return false;
  }
}

export async function cancelDailyStudyReminder(): Promise<void> {
  if (!Capacitor.isNativePlatform()) return;
  try {
    await LocalNotifications.cancel({ notifications: [{ id: DAILY_REMINDER_ID }] });
  } catch (err) {
    console.warn('Failed to cancel daily native reminder:', err);
  }
}

export async function requestAndTriggerStudyNotification(options: {
  title: string;
  body: string;
  tag?: string;
}): Promise<boolean> {
  // 1. Native Android / iOS path via Capacitor LocalNotifications
  if (Capacitor.isNativePlatform()) {
    const granted = await ensureNativePermission();
    if (!granted) return false;

    try {
      const id = INSTANT_NOTIFICATION_BASE_ID + (Math.floor(Date.now() / 1000) % 50000);
      await LocalNotifications.schedule({
        notifications: [
          {
            id,
            title: options.title,
            body: options.body,
            schedule: { at: new Date(Date.now() + 800), allowWhileIdle: true },
            iconColor: '#5DA9E9',
          },
        ],
      });
      return true;
    } catch (err) {
      console.warn('Native local notification failed:', err);
      return false;
    }
  }

  // 2. Web / Desktop PWA fallback
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