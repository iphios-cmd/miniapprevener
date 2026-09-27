import { useCallback, useState } from 'react';
import {
  clearProgress,
  loadProgress,
  saveProgress,
  type ProgressState,
} from '../lib/storage';
import { TOTAL_STEPS } from '../config/steps';

export function useProgress() {
  const [state, setState] = useState<ProgressState>(() => loadProgress());

  const persist = useCallback((next: ProgressState) => {
    setState(next);
    saveProgress(next);
  }, []);

  const acceptAndStart = useCallback(() => {
    persist({
      warningAccepted: true,
      currentStep: 1,
      completed: false,
    });
  }, [persist]);

  const setStep = useCallback(
    (step: number) => {
      const clamped = Math.min(Math.max(step, 1), TOTAL_STEPS);
      setState((prev) => {
        const next = {
          ...prev,
          currentStep: clamped,
          completed: false,
          warningAccepted: true,
        };
        saveProgress(next);
        return next;
      });
    },
    [],
  );

  const complete = useCallback(() => {
    setState((prev) => {
      const next = {
        ...prev,
        completed: true,
        currentStep: TOTAL_STEPS,
        warningAccepted: true,
      };
      saveProgress(next);
      return next;
    });
  }, []);

  const reset = useCallback(() => {
    clearProgress();
    const fresh = {
      warningAccepted: false,
      currentStep: 1,
      completed: false,
    };
    setState(fresh);
    return fresh;
  }, []);

  const restartGuide = useCallback(() => {
    persist({
      warningAccepted: true,
      currentStep: 1,
      completed: false,
    });
  }, [persist]);

  return {
    ...state,
    acceptAndStart,
    setStep,
    complete,
    reset,
    restartGuide,
  };
}
