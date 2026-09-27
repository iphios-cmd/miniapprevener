import { useEffect, useState } from 'react';
import { Home } from './components/Home';
import { Wizard } from './components/Wizard';
import { Success } from './components/Success';
import { ResumeModal } from './components/ResumeModal';
import { Loading } from './components/Loading';
import { ScreenTransition } from './components/ScreenTransition';
import { useTelegram } from './hooks/useTelegram';
import { useProgress } from './hooks/useProgress';
import { TOTAL_STEPS } from './config/steps';

type Screen = 'home' | 'wizard' | 'success';

export default function App() {
  const { haptic, hapticSuccess, openBot } = useTelegram();
  const progress = useProgress();

  const [loading, setLoading] = useState(true);
  const [screen, setScreen] = useState<Screen>('home');
  const [resumeOpen, setResumeOpen] = useState(false);

  useEffect(() => {
    const t = window.setTimeout(() => setLoading(false), 1250);
    return () => window.clearTimeout(t);
  }, []);

  useEffect(() => {
    if (loading) return;

    // После завершения всегда остаёмся на главной при повторном входе
    if (progress.completed) {
      progress.restartGuide();
      return;
    }

    const hasPartial =
      progress.currentStep > 1 && progress.currentStep <= TOTAL_STEPS;

    if (hasPartial) {
      setResumeOpen(true);
    }
  }, [loading]); // eslint-disable-line react-hooks/exhaustive-deps

  const startFlow = () => {
    if (progress.completed) {
      progress.restartGuide();
      setScreen('wizard');
      return;
    }
    if (progress.currentStep > 1 && !progress.completed) {
      setScreen('wizard');
      return;
    }
    progress.acceptAndStart();
    setScreen('wizard');
  };

  const goHome = () => {
    // Сбрасываем флаг завершения, чтобы следующий заход был с главной
    if (progress.completed) {
      progress.restartGuide();
    }
    setScreen('home');
  };

  const handleNext = () => {
    if (progress.currentStep >= TOTAL_STEPS) {
      progress.complete();
      hapticSuccess();
      setScreen('success');
      return;
    }
    progress.setStep(progress.currentStep + 1);
  };

  const handleBack = () => {
    if (progress.currentStep <= 1) return;
    progress.setStep(progress.currentStep - 1);
  };

  return (
    <>
      <Loading visible={loading} />

      {!loading && (
        <div id="app" className={`ready app-${screen}`}>
          <ScreenTransition screen={screen}>
            {screen === 'home' && (
              <Home onStart={startFlow} onSupport={openBot} haptic={haptic} />
            )}
            {screen === 'wizard' && (
              <Wizard
                step={progress.currentStep}
                onBack={handleBack}
                onNext={handleNext}
                onAction={openBot}
                haptic={haptic}
              />
            )}
            {screen === 'success' && (
              <Success
                onHome={goHome}
                onRestart={() => {
                  progress.restartGuide();
                  setScreen('wizard');
                }}
                onSupport={openBot}
                haptic={haptic}
                hapticSuccess={hapticSuccess}
              />
            )}
          </ScreenTransition>
        </div>
      )}

      <ResumeModal
        open={resumeOpen}
        step={progress.currentStep}
        onContinue={() => {
          setResumeOpen(false);
          setScreen('wizard');
        }}
        onRestart={() => {
          progress.restartGuide();
          setResumeOpen(false);
          setScreen('wizard');
        }}
        haptic={haptic}
      />
    </>
  );
}
