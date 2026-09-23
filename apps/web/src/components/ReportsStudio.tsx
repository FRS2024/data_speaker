import React, { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { reportsApi, reportsPreviewQueryOptions } from "@/lib/api";
import { DeckSlidePreview } from "@/lib/types";
import {
  FileText,
  Presentation,
  Download,
  Sparkles,
  Palette,
  CheckCircle2,
  ChevronRight,
  BarChart3,
  Activity,
  GitBranch,
  Layers,
  ArrowRight,
  Loader2,
} from "lucide-react";

interface ReportsStudioProps {
  sessionId: string;
}

export const ReportsStudio: React.FC<ReportsStudioProps> = ({ sessionId }) => {
  const [selectedTheme, setSelectedTheme] = useState<"dark" | "light" | "navy">("dark");
  const [activeSlideIndex, setActiveSlideIndex] = useState<number>(0);
  const [isExportingPptx, setIsExportingPptx] = useState<boolean>(false);
  const [isExportingPdf, setIsExportingPdf] = useState<boolean>(false);
  const [polishedSlideId, setPolishedSlideId] = useState<string | null>(null);

  // Fetch slide preview
  const { data: previewData, isLoading, refetch } = useQuery(
    reportsPreviewQueryOptions(sessionId, selectedTheme)
  );

  // AI Polish mutation
  const polishMutation = useMutation({
    mutationFn: (slideId: string) => reportsApi.requestAIPolish(sessionId, slideId),
    onSuccess: (data) => {
      setPolishedSlideId(data.slide_id);
    },
  });

  const slides: DeckSlidePreview[] = previewData?.slides || [];
  const currentSlide = slides[activeSlideIndex] || null;

  const handleDownloadPptx = async () => {
    setIsExportingPptx(true);
    try {
      await reportsApi.downloadDeckPptx(sessionId, { theme: selectedTheme });
    } catch (err) {
      console.error("PPTX export failed:", err);
      alert("Failed to export PowerPoint presentation.");
    } finally {
      setIsExportingPptx(false);
    }
  };

  const handleDownloadPdf = async () => {
    setIsExportingPdf(true);
    try {
      await reportsApi.downloadReportPdf(sessionId);
    } catch (err) {
      console.error("PDF export failed:", err);
      alert("Failed to export PDF report brief.");
    } finally {
      setIsExportingPdf(false);
    }
  };

  const handlePolish = () => {
    if (!currentSlide) return;
    polishMutation.mutate(currentSlide.slide_id);
  };

  const getSlideIcon = (type: string) => {
    switch (type) {
      case "title":
        return <Layers className="w-4 h-4 text-sky-400" />;
      case "hygiene":
        return <Activity className="w-4 h-4 text-emerald-400" />;
      case "correlations":
        return <GitBranch className="w-4 h-4 text-indigo-400" />;
      case "metrics":
        return <BarChart3 className="w-4 h-4 text-amber-400" />;
      case "summary":
        return <CheckCircle2 className="w-4 h-4 text-cyan-400" />;
      default:
        return <Presentation className="w-4 h-4 text-slate-400" />;
    }
  };

  // Preview styling based on theme
  const getThemeClass = () => {
    switch (selectedTheme) {
      case "light":
        return "bg-slate-50 text-slate-900 border-slate-200";
      case "navy":
        return "bg-[#0B192C] text-slate-100 border-[#1E3E62]";
      case "dark":
      default:
        return "bg-[#0F172A] text-slate-100 border-slate-800";
    }
  };

  const getCardBg = () => {
    switch (selectedTheme) {
      case "light":
        return "bg-white border-slate-200 shadow-sm";
      case "navy":
        return "bg-[#1E3E62]/70 border-[#2D5B8B]/40";
      case "dark":
      default:
        return "bg-[#1E293B] border-slate-700/60";
    }
  };

  if (isLoading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center p-12 text-slate-400">
        <Loader2 className="w-10 h-10 animate-spin text-sky-400 mb-4" />
        <span className="text-lg font-medium text-slate-200">
          Compiling Executive Presentation Deck...
        </span>
        <span className="text-xs text-slate-500 mt-1">
          Synthesizing diagnostics, statistical correlations, and native chart configurations
        </span>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-4rem)] bg-[#131314] overflow-hidden">
      {/* Top Action & Theme Header */}
      <div className="h-14 px-6 border-b border-outline-variant/15 flex items-center justify-between bg-surface-container-low shrink-0">
        <div className="flex items-center gap-3">
          <Presentation className="w-5 h-5 text-sky-400" />
          <div>
            <h1 className="text-sm font-semibold text-on-surface flex items-center gap-2">
              Reports & Presentation Studio
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20 font-mono">
                Track C
              </span>
            </h1>
          </div>
        </div>

        {/* Center: Theme Selector */}
        <div className="flex items-center gap-2 bg-surface-container-high/60 p-1 rounded-full border border-outline-variant/10 text-xs">
          <Palette className="w-3.5 h-3.5 text-slate-400 ml-2" />
          <button
            onClick={() => setSelectedTheme("dark")}
            className={`px-3 py-1 rounded-full font-medium transition-all ${
              selectedTheme === "dark"
                ? "bg-sky-500 text-slate-900 shadow-sm font-semibold"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Dark Slate
          </button>
          <button
            onClick={() => setSelectedTheme("navy")}
            className={`px-3 py-1 rounded-full font-medium transition-all ${
              selectedTheme === "navy"
                ? "bg-cyan-500 text-slate-900 shadow-sm font-semibold"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Gemini Navy
          </button>
          <button
            onClick={() => setSelectedTheme("light")}
            className={`px-3 py-1 rounded-full font-medium transition-all ${
              selectedTheme === "light"
                ? "bg-white text-slate-900 shadow-sm font-semibold"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Executive Light
          </button>
        </div>

        {/* Right: Export Downloads */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleDownloadPdf}
            disabled={isExportingPdf}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-surface-container-high hover:bg-surface-container-highest text-slate-200 text-xs font-medium border border-outline-variant/20 transition-all active:scale-95 disabled:opacity-50"
            title="Download Executive Brief (PDF)"
          >
            {isExportingPdf ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin text-rose-400" />
            ) : (
              <FileText className="w-3.5 h-3.5 text-rose-400" />
            )}
            <span>PDF Brief</span>
          </button>

          <button
            onClick={handleDownloadPptx}
            disabled={isExportingPptx}
            className="flex items-center gap-2 px-4 py-1.5 rounded-lg bg-gradient-to-r from-sky-500 to-indigo-500 hover:from-sky-400 hover:to-indigo-400 text-slate-950 text-xs font-semibold shadow-[0_0_16px_rgba(56,189,248,0.2)] transition-all active:scale-95 disabled:opacity-50"
            title="Download PowerPoint Presentation (.pptx)"
          >
            {isExportingPptx ? (
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
            ) : (
              <Download className="w-3.5 h-3.5" />
            )}
            <span>Export PowerPoint (.pptx)</span>
          </button>
        </div>
      </div>

      {/* Main Studio Viewport */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Rail: Slide Thumbnail Navigator */}
        <div className="w-64 border-r border-outline-variant/10 bg-surface-container-low/50 flex flex-col shrink-0">
          <div className="p-3 border-b border-outline-variant/10 flex items-center justify-between text-xs text-slate-400">
            <span className="font-semibold uppercase tracking-wider text-[11px] text-slate-500">
              Slides ({slides.length})
            </span>
            <span className="text-[10px] text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded-full">
              16:9 Widescreen
            </span>
          </div>

          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {slides.map((s, idx) => {
              const isActive = idx === activeSlideIndex;
              return (
                <div
                  key={s.slide_id}
                  onClick={() => setActiveSlideIndex(idx)}
                  className={`p-3 rounded-xl border text-left cursor-pointer transition-all ${
                    isActive
                      ? "bg-surface-container-highest border-sky-500/50 shadow-[0_0_12px_rgba(56,189,248,0.1)]"
                      : "bg-surface-container-low hover:bg-surface-container border-outline-variant/10 hover:border-outline-variant/30"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="flex items-center gap-1.5 text-xs font-medium text-slate-300">
                      {getSlideIcon(s.slide_type)}
                      <span className="truncate max-w-[130px]">{s.title}</span>
                    </span>
                    <span className="text-[10px] font-mono text-slate-500">#{idx + 1}</span>
                  </div>
                  <p className="text-[11px] text-slate-400 line-clamp-1">
                    {s.subtitle || s.bullet_points[0] || "Executive content"}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Center: Live 16:9 Slide Canvas Preview */}
        <div className="flex-1 bg-[#0c0c0d] p-8 flex flex-col items-center justify-center overflow-y-auto">
          {currentSlide && (
            <div className="w-full max-w-4xl aspect-[16/9] rounded-2xl border shadow-2xl p-8 flex flex-col justify-between transition-all relative overflow-hidden select-none animate-in fade-in zoom-in-95 duration-200">
              {/* Slide Background Container */}
              <div
                className={`absolute inset-0 border ${getThemeClass()} p-8 flex flex-col justify-between`}
              >
                {/* Decorative Top Accent Line */}
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-sky-400 via-indigo-400 to-emerald-400" />

                {/* Header */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-[11px] font-mono uppercase tracking-widest text-sky-400">
                        data_speaker • Slide {activeSlideIndex + 1} of {slides.length}
                      </span>
                    </div>

                    {/* AI Polish Button */}
                    <button
                      onClick={handlePolish}
                      disabled={polishMutation.isPending}
                      className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-500/10 hover:bg-sky-500/20 text-sky-400 border border-sky-500/30 text-xs font-medium transition-all active:scale-95"
                    >
                      {polishMutation.isPending ? (
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      ) : (
                        <Sparkles className="w-3.5 h-3.5 text-sky-400" />
                      )}
                      <span>
                        {polishedSlideId === currentSlide.slide_id ? "Polished" : "AI Polish"}
                      </span>
                    </button>
                  </div>

                  <h2 className="text-2xl font-bold tracking-tight mb-1">{currentSlide.title}</h2>
                  {currentSlide.subtitle && (
                    <p className="text-sm text-slate-400">{currentSlide.subtitle}</p>
                  )}
                </div>

                {/* Slide Body Content */}
                <div className="my-auto grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Left Column: Key Bullets */}
                  <div className={`p-4 rounded-xl border ${getCardBg()} flex flex-col justify-center`}>
                    <span className="text-xs font-semibold text-sky-400 mb-2 uppercase tracking-wider flex items-center gap-1.5">
                      <ChevronRight className="w-3.5 h-3.5" />
                      Strategic Observations
                    </span>
                    <ul className="space-y-2 text-xs">
                      {currentSlide.bullet_points.map((b, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="text-sky-400 mt-0.5">•</span>
                          <span className="leading-relaxed">{b}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Right Column: Visual / Metric Highlight */}
                  <div className={`p-4 rounded-xl border ${getCardBg()} flex flex-col justify-center items-center text-center`}>
                    {currentSlide.has_chart ? (
                      <div className="w-full flex flex-col items-center justify-center p-4">
                        <BarChart3 className="w-12 h-12 text-sky-400/80 mb-2" />
                        <span className="text-xs font-semibold text-slate-300">
                          Native Editable PowerPoint Chart
                        </span>
                        <span className="text-[11px] text-slate-400 mt-1">
                          Clustered Column Visualization generated directly in .pptx shape tree
                        </span>
                      </div>
                    ) : (
                      <div className="w-full flex flex-col items-center justify-center p-4">
                        <Activity className="w-12 h-12 text-emerald-400/80 mb-2" />
                        <span className="text-xs font-semibold text-slate-300">
                          Automated Diagnostic Heuristics
                        </span>
                        <span className="text-[11px] text-slate-400 mt-1">
                          Enterprise grade quality validation & anomaly attributions
                        </span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Footer Metadata */}
                <div className="border-t border-slate-700/30 pt-3 flex items-center justify-between text-[11px] text-slate-400">
                  <span>Confidential — Internal Executive Review</span>
                  <span>Session: {sessionId.slice(0, 18)}...</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
