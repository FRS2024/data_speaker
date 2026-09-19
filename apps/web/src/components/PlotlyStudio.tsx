"use client";

import React, { useState } from "react";
import dynamic from "next/dynamic";
import { BarChart3, Maximize2, Minimize2, Download, Layers, Sparkles } from "lucide-react";

// Dynamically import Plotly with SSR disabled
const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

interface PlotlyStudioProps {
  figures: any[];
}

export const PlotlyStudio: React.FC<PlotlyStudioProps> = ({ figures }) => {
  const [selectedChartIndex, setSelectedChartIndex] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);

  if (!figures || figures.length === 0) {
    return (
      <div className="h-full flex flex-col items-center justify-center p-8 text-center text-studio-muted font-mono space-y-3">
        <BarChart3 className="w-10 h-10 text-studio-muted/50" />
        <div className="text-sm font-bold text-studio-highlight">No Visualizations Generated Yet</div>
        <p className="text-xs max-w-sm">
          Ask the Autonomous Analyst to visualize your data (e.g. <em>&quot;Plot a histogram of revenue&quot;</em> or <em>&quot;Show correlation heatmap&quot;</em>).
        </p>
      </div>
    );
  }

  const activeFigure = figures[selectedChartIndex] || figures[figures.length - 1];

  // Deep clone and inject dark studio theme properties
  const themedLayout = {
    ...activeFigure.layout,
    autosize: true,
    paper_bgcolor: "#090d16",
    plot_bgcolor: "#0d1117",
    font: {
      color: "#c9d1d9",
      family: "JetBrains Mono, monospace",
      size: 11,
      ...activeFigure.layout?.font,
    },
    margin: { t: 40, r: 20, l: 50, b: 50, ...activeFigure.layout?.margin },
    xaxis: {
      gridcolor: "#21262d",
      linecolor: "#30363d",
      tickfont: { color: "#8b949e" },
      ...activeFigure.layout?.xaxis,
    },
    yaxis: {
      gridcolor: "#21262d",
      linecolor: "#30363d",
      tickfont: { color: "#8b949e" },
      ...activeFigure.layout?.yaxis,
    },
  };

  return (
    <div
      className={`flex flex-col h-full bg-studio-bg font-mono select-none ${
        isFullscreen ? "fixed inset-0 z-50 p-6 bg-black/95 backdrop-blur-md" : ""
      }`}
    >
      {/* Studio Toolbar */}
      <div className="h-10 bg-studio-surface border-b border-studio-border px-4 flex items-center justify-between shrink-0">
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-4 h-4 text-studio-amber" />
          <span className="text-xs font-bold text-studio-highlight">
            INTERACTIVE PLOTLY CANVAS
          </span>
          <span className="text-[10px] text-studio-muted px-1.5 py-0.5 rounded bg-studio-card border border-studio-border">
            WebGL ACCELERATED
          </span>
        </div>

        {/* Gallery Selector & Actions */}
        <div className="flex items-center space-x-2">
          {figures.length > 1 && (
            <div className="flex items-center space-x-1 bg-studio-card p-0.5 rounded border border-studio-border text-xs mr-2">
              {figures.map((_, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedChartIndex(idx)}
                  className={`px-2 py-0.5 rounded text-[11px] transition ${
                    selectedChartIndex === idx
                      ? "bg-studio-amber text-studio-bg font-bold"
                      : "text-studio-muted hover:text-studio-highlight"
                  }`}
                >
                  Chart #{idx + 1}
                </button>
              ))}
            </div>
          )}

          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="p-1.5 rounded bg-studio-card border border-studio-border text-studio-muted hover:text-studio-highlight transition"
            title={isFullscreen ? "Exit Fullscreen" : "Expand Fullscreen"}
          >
            {isFullscreen ? <Minimize2 className="w-3.5 h-3.5" /> : <Maximize2 className="w-3.5 h-3.5" />}
          </button>
        </div>
      </div>

      {/* Plotly Canvas Container */}
      <div className="flex-1 w-full h-full relative p-2 overflow-hidden flex items-center justify-center">
        <Plot
          data={activeFigure.data || []}
          layout={themedLayout}
          config={{
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ["lasso2d", "select2d"],
          }}
          useResizeHandler={true}
          className="w-full h-full"
          style={{ width: "100%", height: "100%" }}
        />
      </div>
    </div>
  );
};
