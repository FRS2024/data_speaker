import React from "react";

interface AudioWaveVisualizerProps {
  isActive: boolean;
  barCount?: number;
  height?: number;
  colorClass?: string;
}

export const AudioWaveVisualizer: React.FC<AudioWaveVisualizerProps> = ({
  isActive,
  barCount = 12,
  height = 24,
  colorClass = "bg-gradient-to-t from-indigo-500 to-cyan-400",
}) => {
  // Pre-configured relative heights for wave variation
  const baseDelays = [0.1, 0.3, 0.15, 0.45, 0.25, 0.5, 0.2, 0.35, 0.15, 0.4, 0.2, 0.3];

  return (
    <div
      className="flex items-center gap-[3px] px-2 py-1 justify-center"
      style={{ height: `${height}px` }}
    >
      {Array.from({ length: barCount }).map((_, idx) => {
        const delay = baseDelays[idx % baseDelays.length];
        return (
          <div
            key={idx}
            className={`w-[3px] rounded-full transition-all duration-150 ${colorClass} ${
              isActive ? "animate-pulse" : "opacity-30"
            }`}
            style={{
              height: isActive ? `${Math.floor(20 + Math.sin(idx + delay * 10) * 12 + 10)}px` : "4px",
              animationDuration: `${0.4 + delay}s`,
              animationDelay: `${delay}s`,
            }}
          />
        );
      })}
    </div>
  );
};
