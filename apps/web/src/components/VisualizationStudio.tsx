import React, { useState } from "react";
import Plot from "react-plotly.js";

interface VisualizationStudioProps {
  figures: any[];
  onGenerateChart?: (type: string) => void;
}

export const VisualizationStudio: React.FC<VisualizationStudioProps> = ({
  figures = [],
  onGenerateChart,
}) => {
  const [selectedChartIndex, setSelectedChartIndex] = useState(0);
  const [activeVisualType, setActiveVisualType] = useState("Heatmap");

  const hasFigures = figures.length > 0;
  const activeFigure = hasFigures ? figures[selectedChartIndex] || figures[0] : null;

  // Stitch obsidian Plotly theme layout
  const themedLayout = activeFigure
    ? {
        ...activeFigure.layout,
        autosize: true,
        paper_bgcolor: "#131314",
        plot_bgcolor: "#1c1b1c",
        font: {
          color: "#e5e2e3",
          family: "Geist, JetBrains Mono, sans-serif",
          size: 12,
          ...activeFigure.layout?.font,
        },
        margin: { t: 40, r: 24, l: 50, b: 50, ...activeFigure.layout?.margin },
        xaxis: {
          gridcolor: "#2a2a2b",
          linecolor: "#434751",
          tickfont: { color: "#c3c6d3" },
          ...activeFigure.layout?.xaxis,
        },
        yaxis: {
          gridcolor: "#2a2a2b",
          linecolor: "#434751",
          tickfont: { color: "#c3c6d3" },
          ...activeFigure.layout?.yaxis,
        },
      }
    : null;

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] w-full bg-surface overflow-hidden">
      {/* Top Studio Controls Strip */}
      <div className="px-space-md py-2.5 bg-surface-container-low border-b border-outline-variant/20 flex flex-wrap items-center justify-between gap-space-sm shrink-0">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container text-primary font-code-tabular text-[12px]">
            <span className="material-symbols-outlined text-[16px]">insert_chart</span>
            <span className="font-medium">Visualization Studio</span>
          </div>
          <span className="text-outline text-[12px]">•</span>
          <span className="text-tertiary font-code-tabular text-[12px] flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-tertiary"></span>
            WebGL Accelerated
          </span>
        </div>

        {/* Visual Type Switcher Pills */}
        <div className="flex items-center gap-1 bg-surface-container-lowest p-1 rounded-full border border-outline-variant/30">
          {["Heatmap", "Histogram", "Scatter", "Bar"].map((type) => (
            <button
              key={type}
              onClick={() => {
                setActiveVisualType(type);
                onGenerateChart?.(type);
              }}
              className={`px-3 py-1 rounded-full font-body-sm text-[12px] transition-all ${
                activeVisualType === type
                  ? "bg-surface-container-high text-primary font-medium shadow-sm"
                  : "text-on-surface-variant hover:text-on-surface"
              }`}
            >
              {type}
            </button>
          ))}
        </div>

        {/* Gallery indices */}
        {figures.length > 1 && (
          <div className="flex items-center gap-1">
            {figures.map((_, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedChartIndex(idx)}
                className={`w-7 h-7 rounded-full flex items-center justify-center font-code-tabular text-[11px] transition-all ${
                  selectedChartIndex === idx
                    ? "bg-primary text-surface-container-lowest font-bold"
                    : "bg-surface-container text-on-surface-variant hover:text-on-surface"
                }`}
              >
                #{idx + 1}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Main Studio Viewport */}
      <div className="flex-1 overflow-auto p-space-lg flex flex-col items-center justify-center relative">
        {/* Ambient Radial Glow behind the active visual */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-secondary/5 to-transparent pointer-events-none"></div>

        {hasFigures && activeFigure ? (
          <div className="w-full h-full max-w-6xl rounded-2xl bg-surface-container-lowest border border-outline-variant/20 p-space-md shadow-2xl flex flex-col z-10">
            <div className="flex items-center justify-between pb-2 border-b border-outline-variant/15 text-[12px] font-code-tabular text-on-surface-variant">
              <span>{activeFigure.layout?.title?.text || "Generated Visualization"}</span>
              <span className="text-tertiary">Interactive WebGL Canvas</span>
            </div>
            <div className="flex-1 w-full relative min-h-[400px]">
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
        ) : (
          /* Default Rich Correlation Matrix Mockup from Screen 09 */
          <div className="w-full max-w-3xl relative z-10 flex flex-col gap-space-md p-space-lg rounded-2xl bg-surface-container border border-outline-variant/25 shadow-2xl">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="material-symbols-outlined text-[18px] text-primary">grid_view</span>
                <span className="font-medium text-on-surface text-[14px]">
                  Normalized Pearson Correlation Matrix (4x4)
                </span>
              </div>
              <span className="font-code-tabular text-[11px] px-2 py-0.5 rounded-full bg-surface-container-high text-tertiary">
                Enterprise Cohort • n=842
              </span>
            </div>

            {/* Heatmap Matrix Grid */}
            <div className="grid grid-cols-5 gap-2 items-center font-code-tabular text-code-tabular text-[12px]">
              {/* Corner Label */}
              <div className="text-right pr-2 text-outline font-label-caps uppercase text-[10px]">
                Metrics
              </div>
              <div className="text-center font-medium text-on-surface-variant truncate">MRR Amount</div>
              <div className="text-center font-medium text-on-surface-variant truncate">Retry Count</div>
              <div className="text-center font-medium text-on-surface-variant truncate">Sub. Age</div>
              <div className="text-center font-medium text-on-surface-variant truncate">Churn Risk</div>

              {/* ROW 1: MRR Amount */}
              <div className="text-right pr-2 font-medium text-on-surface-variant truncate">MRR Amount</div>
              <div className="h-14 rounded-xl bg-[#7ca7ff] text-surface-container-lowest flex flex-col items-center justify-center font-bold shadow-sm">
                <span>1.00</span>
                <span className="text-[9px] opacity-80 font-normal">Identical</span>
              </div>
              <div className="h-14 rounded-xl bg-[#1c2438] text-on-surface flex flex-col items-center justify-center font-medium shadow-sm">
                <span>-0.12</span>
              </div>
              <div className="h-14 rounded-xl bg-[#2a3d66] text-primary-fixed flex flex-col items-center justify-center font-medium shadow-sm">
                <span>+0.48</span>
              </div>
              <div className="h-14 rounded-xl bg-[#1c2438] text-on-surface flex flex-col items-center justify-center font-medium shadow-sm">
                <span>-0.34</span>
              </div>

              {/* ROW 2: Retry Count */}
              <div className="text-right pr-2 font-medium text-on-surface-variant truncate">Retry Count</div>
              <div className="h-14 rounded-xl bg-[#1c2438] text-on-surface flex flex-col items-center justify-center font-medium shadow-sm">
                <span>-0.12</span>
              </div>
              <div className="h-14 rounded-xl bg-[#7ca7ff] text-surface-container-lowest flex flex-col items-center justify-center font-bold shadow-sm">
                <span>1.00</span>
              </div>
              <div className="h-14 rounded-xl bg-[#1a202c] text-on-surface flex flex-col items-center justify-center font-medium shadow-sm">
                <span>-0.08</span>
              </div>
              <div className="h-14 rounded-xl bg-[#a855f7] text-white flex flex-col items-center justify-center font-bold shadow-sm border border-secondary/40">
                <span>+0.74</span>
                <span className="text-[9px] opacity-90 font-normal">High Risk</span>
              </div>

              {/* ROW 3: Sub. Age */}
              <div className="text-right pr-2 font-medium text-on-surface-variant truncate">Sub. Age</div>
              <div className="h-14 rounded-xl bg-[#2a3d66] text-primary-fixed flex flex-col items-center justify-center font-medium shadow-sm">
                <span>+0.48</span>
              </div>
              <div className="h-14 rounded-xl bg-[#1a202c] text-on-surface flex flex-col items-center justify-center font-medium shadow-sm">
                <span>-0.08</span>
              </div>
              <div className="h-14 rounded-xl bg-[#7ca7ff] text-surface-container-lowest flex flex-col items-center justify-center font-bold shadow-sm">
                <span>1.00</span>
              </div>
              <div className="h-14 rounded-xl bg-[#162032] text-on-surface flex flex-col items-center justify-center font-medium shadow-sm">
                <span>-0.52</span>
              </div>

              {/* ROW 4: Churn Risk */}
              <div className="text-right pr-2 font-medium text-on-surface-variant truncate">Churn Risk</div>
              <div className="h-14 rounded-xl bg-[#1c2438] text-on-surface flex flex-col items-center justify-center font-medium shadow-sm">
                <span>-0.34</span>
              </div>
              <div className="h-14 rounded-xl bg-[#a855f7] text-white flex flex-col items-center justify-center font-bold shadow-sm">
                <span>+0.74</span>
              </div>
              <div className="h-14 rounded-xl bg-[#162032] text-on-surface flex flex-col items-center justify-center font-medium shadow-sm">
                <span>-0.52</span>
              </div>
              <div className="h-14 rounded-xl bg-[#7ca7ff] text-surface-container-lowest flex flex-col items-center justify-center font-bold shadow-sm">
                <span>1.00</span>
              </div>
            </div>

            {/* Predictive Insight Box */}
            <div className="p-space-sm rounded-xl bg-surface-container-low flex items-start gap-space-sm border border-outline-variant/15">
              <span className="material-symbols-outlined text-[20px] text-tertiary shrink-0">insights</span>
              <p className="text-body-sm font-body-sm text-on-surface-variant">
                <span className="text-tertiary font-medium">Predictive signal detected:</span> High positive covariance between <code className="font-code-tabular text-primary">retry_count</code> and <code className="font-code-tabular text-primary">churn_risk</code> (<strong className="text-on-surface">r = +0.74</strong>). Payment gateway failures trigger aggressive churn spikes in high-ACV seats.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
