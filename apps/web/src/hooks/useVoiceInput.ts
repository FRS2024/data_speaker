import { useState, useRef, useCallback, useEffect } from "react";
import { AudioTranscribeResponse } from "@/lib/types";

interface UseVoiceInputOptions {
  onTranscriptUpdate?: (transcript: string) => void;
  onFinalTranscript?: (transcript: string) => void;
}

export function useVoiceInput(options: UseVoiceInputOptions = {}) {
  const [isListening, setIsListening] = useState<boolean>(false);
  const [transcript, setTranscript] = useState<string>("");
  const [interimTranscript, setInterimTranscript] = useState<string>("");
  const [elapsedSeconds, setElapsedSeconds] = useState<number>(0);
  const [audioLevel, setAudioLevel] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);

  const recognitionRef = useRef<any>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const animFrameRef = useRef<number | null>(null);
  const isWebSpeechSupported =
    typeof window !== "undefined" &&
    ("SpeechRecognition" in window || "webkitSpeechRecognition" in window);

  // Timer while listening
  useEffect(() => {
    if (isListening) {
      setElapsedSeconds(0);
      timerRef.current = setInterval(() => {
        setElapsedSeconds((prev) => prev + 1);
      }, 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
      setElapsedSeconds(0);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isListening]);

  // Audio waveform pulse simulation
  useEffect(() => {
    if (isListening) {
      const simulateWave = () => {
        // Random level between 25 and 95
        const level = Math.floor(Math.random() * 70) + 25;
        setAudioLevel(level);
        animFrameRef.current = requestAnimationFrame(simulateWave);
      };
      animFrameRef.current = requestAnimationFrame(simulateWave);
    } else {
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
      setAudioLevel(0);
    }
    return () => {
      if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    };
  }, [isListening]);

  const startListening = useCallback(async () => {
    setError(null);
    setTranscript("");
    setInterimTranscript("");

    // 1. Try Browser Web Speech API first (Zero latency client-side)
    if (isWebSpeechSupported) {
      try {
        const SpeechRecognition =
          (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onstart = () => {
          setIsListening(true);
        };

        recognition.onresult = (event: any) => {
          let currentInterim = "";
          let finalAccumulated = "";

          for (let i = event.resultIndex; i < event.results.length; ++i) {
            const part = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
              finalAccumulated += part;
            } else {
              currentInterim += part;
            }
          }

          if (finalAccumulated) {
            setTranscript((prev) => {
              const updated = (prev ? `${prev} ` : "") + finalAccumulated.trim();
              options.onTranscriptUpdate?.(updated);
              return updated;
            });
          }
          setInterimTranscript(currentInterim);
        };

        recognition.onerror = (event: any) => {
          // If browser speech recognition fails (e.g. network/not-allowed), fallback to MediaRecorder
          if (event.error !== "no-speech") {
            setError(`Speech recognition notice: ${event.error}`);
          }
        };

        recognition.onend = () => {
          setIsListening(false);
        };

        recognition.start();
        recognitionRef.current = recognition;
        return;
      } catch (err: any) {
        console.warn("Web Speech API init failed, using MediaRecorder fallback", err);
      }
    }

    // 2. MediaRecorder Server Fallback
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported("audio/webm")
          ? "audio/webm"
          : "audio/ogg",
      });

      audioChunksRef.current = [];
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        if (audioBlob.size > 0) {
          try {
            const formData = new FormData();
            formData.append("file", audioBlob, "recording.webm");
            const res = await fetch("/api/v1/audio/transcribe", {
              method: "POST",
              body: formData,
            });
            if (res.ok) {
              const data: AudioTranscribeResponse = await res.json();
              if (data.text) {
                setTranscript(data.text);
                options.onTranscriptUpdate?.(data.text);
                options.onFinalTranscript?.(data.text);
              }
            }
          } catch (uploadErr: any) {
            setError(`Transcription error: ${uploadErr.message}`);
          }
        }
        setIsListening(false);
      };

      mediaRecorder.start(250);
      mediaRecorderRef.current = mediaRecorder;
      setIsListening(true);
    } catch (err: any) {
      setError(`Microphone access error: ${err.message || "Permission denied"}`);
      setIsListening(false);
    }
  }, [isWebSpeechSupported, options]);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch {}
      recognitionRef.current = null;
    }
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      try {
        mediaRecorderRef.current.stop();
      } catch {}
      mediaRecorderRef.current = null;
    }
    setIsListening(false);
    if (transcript) {
      options.onFinalTranscript?.(transcript);
    }
  }, [options, transcript]);

  const cancelListening = useCallback(() => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch {}
      recognitionRef.current = null;
    }
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      try {
        mediaRecorderRef.current.stop();
      } catch {}
      mediaRecorderRef.current = null;
    }
    setIsListening(false);
    setTranscript("");
    setInterimTranscript("");
    audioChunksRef.current = [];
  }, []);

  return {
    isListening,
    transcript,
    interimTranscript,
    elapsedSeconds,
    audioLevel,
    error,
    startListening,
    stopListening,
    cancelListening,
  };
}
