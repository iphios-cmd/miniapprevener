import { TOTAL_STEPS } from '../config/steps';

const STORAGE_KEY = 'ipa_install_guide_v1';

export type ProgressState = {
  warningAccepted: boolean;
  currentStep: number;
  completed: boolean;
};

const DEFAULT: ProgressState = {
  warningAccepted: false,
  currentStep: 1,
  completed: false,
};

export function loadProgress(): ProgressState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...DEFAULT };
    const parsed = JSON.parse(raw) as Partial<ProgressState>;
    return {
      warningAccepted: Boolean(parsed.warningAccepted),
      currentStep: Math.min(Math.max(Number(parsed.currentStep) || 1, 1), TOTAL_STEPS),
      completed: Boolean(parsed.completed),
    };
  } catch {
    return { ...DEFAULT };
  }
}

export function saveProgress(state: ProgressState): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    /* ignore quota / private mode */
  }
}

export function clearProgress(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    /* ignore */
  }
}
