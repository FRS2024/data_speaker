import { useState, useRef, useCallback, useEffect } from "react";

interface UseVoiceOutputOptions {
  onStart?: () => void;
  onEnd?: () => void;
  onError?: (err: string) => void;
}

export function useVoiceOutput(options: UseVoiceOutputOptions = {}) {
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [isPaused, setIsPaused] = useState<boolean>(false);
  const [rate, setRate] = useState<number>(1.0);
  const [progress, setProgress] = useState<number>(0);
  const [speakingTextId, setSpeakingTextId] = useState<string | null>(null);

  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);
  const audioElRef = useRef<HTMLAudioElement | null>(null);
  const progressIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const durationEstRef = useRef<number>(10);

  const isSpeechSynthesisSupported =
    typeof window !== "undefined" && "speechSynthesis" in window;

  const cleanTextForSpeech = (text: string): string => {
    return text
      .replace(/```[\s\S]*?```/g, " ")
      .replace(/`[^`]+`/g, " ")
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      .replace(/[#*_\->]/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  };

  const stop = useCallback(() => {
    if (isSpeechSynthesisSupported) {
      window.speechSynthesis.cancel();
    }
    if (audioElRef.current) {
      audioElRef.current.pause();
      audioElRef.current = null;
    }
    if (progressIntervalRef.current) {
      clearInterval(progressIntervalRef.current);
    }
    setIsPlaying(false);
    setIsPaused(false);
    setProgress(0);
    setSpeakingTextId(null);
  }, [isSpeechSynthesisSupported]);

  const speak = useCallback(
    async (text: string, textId: string = "audio_turn", speechRate: number = 1.0) => {
      stop();
      setRate(speechRate);
      setSpeakingTextId(textId);

      const cleaned = cleanTextForSpeech(text);
      if (!cleaned) return;

      const words = cleaned.split(" ").length;
      const estimatedSeconds = Math.max(3, (words / (2.5 * speechRate)));
      durationEstRef.current = estimatedSeconds;

      // 1. Browser Native SpeechSynthesis
      if (isSpeechSynthesisSupported) {
        try {
          const utterance = new SpeechSynthesisUtterance(cleaned);
          utterance.rate = speechRate;
          utterance.pitch = 1.0;
          utterance.lang = "en-US";

          // Select natural modern voice if available
          const voices = window.speechSynthesis.getVoices();
          const preferredVoice = voices.find(
            (v) =>
              v.lang.startsWith("en") &&
              (v.name.includes("Google") || v.name.includes("Natural") || v.name.includes("Siri"))
          );
          if (preferredVoice) {
            utterance.voice = preferredVoice;
          }

          utterance.onstart = () => {
            setIsPlaying(true);
            setIsPaused(false);
            setProgress(0);
            options.onStart?.();

            let elapsed = 0;
            progressIntervalRef.current = setInterval(() => {
              elapsed += 0.2;
              const pct = Math.min(100, Math.round((elapsed / durationEstRef.current) * 100));
              setProgress(pct);
            }, 200);
          };

          utterance.onend = () => {
            stop();
            options.onEnd?.();
          };

          utterance.onerror = (e) => {
            console.warn("SpeechSynthesis error, falling back to server audio", e);
            stop();
            // Fallback to server audio
            playServerAudio(cleaned, textId, speechRate);
          };

          utteranceRef.current = utterance;
          window.speechSynthesis.speak(utterance);
          return;
        } catch (err: any) {
          console.warn("Native TTS failed, falling back to server synthesis", err);
        }
      }

      // 2. Server Audio Fallback
      playServerAudio(cleaned, textId, speechRate);
    },
    [isSpeechSynthesisSupported, options, stop]
  );

  const playServerAudio = async (text: string, textId: string, speechRate: number) => {
    try {
      const res = await fetch("/api/v1/audio/synthesize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, speed: speechRate }),
      });
      if (!res.ok) throw new Error("Server audio synthesis failed");

      const blob = await res.blob();
      const audioUrl = URL.createObjectURL(blob);
      const audio = new Audio(audioUrl);
      audioElRef.current = audio;

      audio.onplay = () => {
        setIsPlaying(true);
        setIsPaused(false);
        options.onStart?.();
      };

      audio.ontimeupdate = () => {
        if (audio.duration) {
          setProgress(Math.round((audio.currentTime / audio.duration) * 100));
        }
      };

      audio.onended = () => {
        stop();
        options.onEnd?.();
      };

      audio.play();
    } catch (err: any) {
      options.onError?.(err.message);
      stop();
    }
  };

  const pause = useCallback(() => {
    if (isSpeechSynthesisSupported && window.speechSynthesis.speaking) {
      window.speechSynthesis.pause();
    }
    if (audioElRef.current) {
      audioElRef.current.pause();
    }
    setIsPaused(true);
  }, [isSpeechSynthesisSupported]);

  const resume = useCallback(() => {
    if (isSpeechSynthesisSupported && window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
    }
    if (audioElRef.current) {
      audioElRef.current.play();
    }
    setIsPaused(false);
  }, [isSpeechSynthesisSupported]);

  useEffect(() => {
    return () => {
      stop();
    };
  }, [stop]);

  return {
    isPlaying,
    isPaused,
    rate,
    progress,
    speakingTextId,
    speak,
    pause,
    resume,
    stop,
    setRate,
  };
}
