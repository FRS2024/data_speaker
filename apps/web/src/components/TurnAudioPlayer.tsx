import React, { useState } from "react";
import { useVoiceOutput } from "@/hooks/useVoiceOutput";
import { AudioWaveVisualizer } from "./AudioWaveVisualizer";
import { ExecutiveRecapResponse } from "@/lib/types";
import {
  Volume2,
  VolumeX,
  Play,
  Pause,
  Square,
  Sparkles,
  FileText,
  Clock,
  FastForward,
} from "lucide-react";

interface TurnAudioPlayerProps {
  sessionId: string;
  turnId: string;
  content: string;
  metrics?: Record<string, any>;
}

export const TurnAudioPlayer: React.FC<TurnAudioPlayerProps> = ({
  sessionId,
  turnId,
  content,
  metrics,
}) => {
  const [activeMode, setActiveMode] = useState<"recap" | "full">("recap");
  const [recapData, setRecapData] = useState<ExecutiveRecapResponse | null>(null);
  const [isLoadingRecap, setIsLoadingRecap] = useState<boolean>(false);
  const [selectedRate, setSelectedRate] = useState<number>(1.0);

  const {
    isPlaying,
    isPaused,
    progress,
    speakingTextId,
    speak,
    pause,
    resume,
    stop,
  } = useVoiceOutput();

  const isCurrentTurnPlaying = isPlaying && speakingTextId === turnId;
  const isCurrentTurnPaused = isPaused && speakingTextId === turnId;

  const fetchRecapIfNeeded = async (): Promise<string> => {
    if (recapData?.recap_text) return recapData.recap_text;
    setIsLoadingRecap(true);
    try {
      const res = await fetch("/api/v1/audio/recap", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          turn_id: turnId,
          content,
          metrics,
        }),
      });
      if (res.ok) {
        const data: ExecutiveRecapResponse = await res.json();
        setRecapData(data);
        return data.recap_text;
      }
    } catch (e) {
      console.warn("Failed to fetch executive recap", e);
    } finally {
      setIsLoadingRecap(false);
    }
    return content;
  };

  const handleTogglePlay = async () => {
    if (isCurrentTurnPlaying) {
      pause();
      return;
    }
    if (isCurrentTurnPaused) {
      resume();
      return;
    }

    let textToSpeak = content;
    if (activeMode === "recap") {
      textToSpeak = await fetchRecapIfNeeded();
    }
    speak(textToSpeak, turnId, selectedRate);
  };

  const handleRateChange = (newRate: number) => {
    setSelectedRate(newRate);
    if (isCurrentTurnPlaying || isCurrentTurnPaused) {
      stop();
      const textToSpeak = activeMode === "recap" && recapData ? recapData.recap_text : content;
      speak(textToSpeak, turnId, newRate);
    }
  };

  return (
    <div className="w-full bg-[#18191a]/95 border border-[#3c4043]/60 rounded-xl p-2.5 my-2 shadow-md text-zinc-200">
      <div className="flex flex-wrap items-center justify-between gap-2">
        {/* Mode Selector Tabs */}
        <div className="flex items-center gap-1 bg-[#131314] p-1 rounded-lg border border-zinc-800 text-[11px]">
          <button
            type="button"
            onClick={() => {
              if (activeMode !== "recap") {
                stop();
                setActiveMode("recap");
              }
            }}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-all font-medium ${
              activeMode === "recap"
                ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            <Sparkles className="w-3 h-3 text-indigo-400" />
            <span>20s Executive Recap</span>
          </button>

          <button
            type="button"
            onClick={() => {
              if (activeMode !== "full") {
                stop();
                setActiveMode("full");
              }
            }}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-all font-medium ${
              activeMode === "full"
                ? "bg-primary/20 text-primary border border-primary/30"
                : "text-zinc-400 hover:text-zinc-200"
            }`}
          >
            <FileText className="w-3 h-3 text-primary" />
            <span>Full Analysis</span>
          </button>
        </div>

        {/* Playback & Visualizer Controls */}
        <div className="flex items-center gap-2">
          {/* Audio Wave Visualizer */}
          <AudioWaveVisualizer
            isActive={isCurrentTurnPlaying}
            barCount={8}
            height={18}
            colorClass={activeMode === "recap" ? "bg-indigo-400" : "bg-cyan-400"}
          />

          {/* Speed Selector Chips */}
          <div className="flex items-center gap-1 bg-[#131314] px-1.5 py-0.5 rounded-lg border border-zinc-800 text-[10px] font-mono">
            {[1.0, 1.25, 1.5].map((s) => (
              <button
                key={s}
                type="button"
                onClick={() => handleRateChange(s)}
                className={`px-1.5 py-0.5 rounded transition-all ${
                  selectedRate === s
                    ? "bg-zinc-700 text-white font-bold"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                {s}x
              </button>
            ))}
          </div>

          {/* Play/Pause Button */}
          <button
            type="button"
            onClick={handleTogglePlay}
            disabled={isLoadingRecap}
            className={`h-7 px-3 rounded-lg flex items-center gap-1.5 text-xs font-medium transition-all ${
              isCurrentTurnPlaying
                ? "bg-amber-500/20 text-amber-300 border border-amber-500/40 hover:bg-amber-500/30"
                : "bg-indigo-600 hover:bg-indigo-500 text-white shadow-md active:scale-95"
            }`}
          >
            {isLoadingRecap ? (
              <span className="text-[11px] animate-pulse">Drafting recap...</span>
            ) : isCurrentTurnPlaying ? (
              <>
                <Pause className="w-3.5 h-3.5" />
                <span>Pause</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-current" />
                <span>Listen</span>
              </>
            )}
          </button>

          {/* Stop Button */}
          {(isCurrentTurnPlaying || isCurrentTurnPaused) && (
            <button
              type="button"
              onClick={stop}
              className="w-7 h-7 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center justify-center transition-colors"
              title="Stop Narration"
            >
              <Square className="w-3 h-3 fill-current" />
            </button>
          )}
        </div>
      </div>

      {/* Progress Bar when Active */}
      {(isCurrentTurnPlaying || isCurrentTurnPaused) && (
        <div className="w-full mt-2 pt-1.5 border-t border-zinc-800/80 flex items-center gap-2 text-[10px] text-zinc-400 font-mono">
          <div className="flex-1 bg-zinc-800 h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-indigo-500 h-full rounded-full transition-all duration-200"
              style={{ width: `${progress}%` }}
            />
          </div>
          <span>{progress}%</span>
        </div>
      )}

      {/* Spoken Recap Preview Card if available */}
      {activeMode === "recap" && recapData?.recap_text && (
        <div className="mt-2 p-2 rounded-lg bg-indigo-950/20 border border-indigo-500/20 text-[11px] text-indigo-200/90 leading-relaxed animate-in fade-in duration-200">
          <span className="font-semibold text-indigo-300 mr-1 uppercase font-mono text-[10px]">
            Audio Script:
          </span>
          {recapData.recap_text}
        </div>
      )}
    </div>
  );
};
