import React, { useState } from "react";
import { CriticReview, DebateExchange } from "@/lib/types";
import {
  ShieldCheck,
  AlertTriangle,
  AlertOctagon,
  ChevronDown,
  ChevronUp,
  Activity,
  GitCompare,
  CheckCircle2,
  HelpCircle,
  Code2,
} from "lucide-react";

interface StatisticalPeerReviewCardProps {
  criticReview?: CriticReview;
  debateHistory?: DebateExchange[];
}

export const StatisticalPeerReviewCard: React.FC<StatisticalPeerReviewCardProps> = ({
  criticReview,
  debateHistory = [],
}) => {
  const [isDebateExpanded, setIsDebateExpanded] = useState<boolean>(false);
  const [isDetailsExpanded, setIsDetailsExpanded] = useState<boolean>(false);

  if (!criticReview && debateHistory.length === 0) return null;

  const verdict = criticReview?.verdict || "passed";
  const confidencePercent = Math.round((criticReview?.confidence_score ?? 0.85) * 100);

  const getVerdictBadge = () => {
    switch (verdict) {
      case "passed":
        return {
          label: "Methodologically Sound",
          color: "text-emerald-400 bg-emerald-500/15 border-emerald-500/30",
          icon: ShieldCheck,
        };
      case "flagged_with_caveats":
        return {
          label: "Accepted with Caveats",
          color: "text-amber-400 bg-amber-500/15 border-amber-500/30",
          icon: AlertTriangle,
        };
      case "requires_revision":
        return {
          label: "Revisions Requested",
          color: "text-rose-400 bg-rose-500/15 border-rose-500/30",
          icon: AlertOctagon,
        };
      default:
        return {
          label: "Peer Reviewed",
          color: "text-blue-400 bg-blue-500/15 border-blue-500/30",
          icon: CheckCircle2,
        };
    }
  };

  const badge = getVerdictBadge();
  const BadgeIcon = badge.icon;

  return (
    <div className="w-full bg-[#1e1f20]/95 border border-[#3c4043] rounded-2xl p-4 shadow-xl my-2 text-zinc-200">
      {/* Top Bar: Verdict + Score */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-[#3c4043]/60">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-purple-500/15 text-purple-400 flex items-center justify-center">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-sm text-white">
                Statistician Peer Review
              </span>
              <span
                className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium border ${badge.color}`}
              >
                <BadgeIcon className="w-3 h-3" />
                {badge.label}
              </span>
            </div>
            <p className="text-[11px] text-zinc-400">
              Rigorous AST screening and sample validity verification
            </p>
          </div>
        </div>

        {/* Statistical Confidence Score Metric */}
        <div className="flex items-center gap-3 bg-[#131314] px-3 py-1.5 rounded-xl border border-zinc-800">
          <div className="text-right">
            <div className="text-[10px] text-zinc-400 uppercase tracking-wider font-mono">
              Confidence
            </div>
            <div className="text-sm font-bold font-mono text-white">
              {confidencePercent}%
            </div>
          </div>
          <div className="w-16 h-2 bg-zinc-800 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-500 rounded-full ${
                confidencePercent >= 80
                  ? "bg-emerald-400"
                  : confidencePercent >= 60
                  ? "bg-amber-400"
                  : "bg-rose-400"
              }`}
              style={{ width: `${confidencePercent}%` }}
            />
          </div>
        </div>
      </div>

      {/* Critique summary */}
      {criticReview?.critique && (
        <div className="mt-3 text-xs leading-relaxed text-zinc-300">
          <span className="text-zinc-400 font-medium mr-1.5 font-mono">CRITIQUE:</span>
          {criticReview.critique}
        </div>
      )}

      {/* Detected Anti-Patterns / Flagged Items */}
      {criticReview?.detected_anti_patterns &&
        criticReview.detected_anti_patterns.length > 0 && (
          <div className="mt-3 p-2.5 rounded-xl bg-rose-950/20 border border-rose-500/30 flex flex-col gap-1.5">
            <span className="text-xs font-semibold text-rose-300 flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5" />
              Statistical Anti-Patterns Flagged:
            </span>
            <ul className="list-disc list-inside text-xs text-rose-200/90 space-y-0.5 pl-1">
              {criticReview.detected_anti_patterns.map((flag, idx) => (
                <li key={idx}>{flag}</li>
              ))}
            </ul>
          </div>
        )}

      {/* Caveats */}
      {criticReview?.caveats && criticReview.caveats.length > 0 && (
        <div className="mt-2.5 p-2.5 rounded-xl bg-amber-950/20 border border-amber-500/30 flex flex-col gap-1.5">
          <span className="text-xs font-semibold text-amber-300 flex items-center gap-1.5">
            <HelpCircle className="w-3.5 h-3.5" />
            Methodological Caveats:
          </span>
          <ul className="list-disc list-inside text-xs text-amber-200/90 space-y-0.5 pl-1">
            {criticReview.caveats.map((cav, idx) => (
              <li key={idx}>{cav}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Guidance */}
      {criticReview?.specific_guidance && (
        <div className="mt-2.5 text-xs text-indigo-300 bg-indigo-950/25 border border-indigo-500/25 p-2.5 rounded-xl">
          <span className="font-semibold text-indigo-200 mr-1.5">Peer Guidance:</span>
          {criticReview.specific_guidance}
        </div>
      )}

      {/* Debate Exchange History Accordion */}
      {debateHistory && debateHistory.length > 0 && (
        <div className="mt-3 pt-3 border-t border-[#3c4043]/50">
          <button
            type="button"
            onClick={() => setIsDebateExpanded(!isDebateExpanded)}
            className="w-full flex items-center justify-between text-xs font-medium text-purple-300 hover:text-purple-200 transition-colors py-1"
          >
            <div className="flex items-center gap-1.5">
              <GitCompare className="w-3.5 h-3.5" />
              <span>Multi-Agent Deliberation History ({debateHistory.length} exchanges)</span>
            </div>
            {isDebateExpanded ? (
              <ChevronUp className="w-4 h-4" />
            ) : (
              <ChevronDown className="w-4 h-4" />
            )}
          </button>

          {isDebateExpanded && (
            <div className="mt-2.5 space-y-2 animate-in fade-in duration-200">
              {debateHistory.map((step, idx) => (
                <div
                  key={idx}
                  className={`p-2.5 rounded-xl border text-xs leading-relaxed ${
                    step.role === "critic"
                      ? "bg-purple-950/25 border-purple-500/30 text-purple-200"
                      : "bg-blue-950/25 border-blue-500/30 text-blue-200"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1 text-[11px] font-mono">
                    <span className="font-bold flex items-center gap-1">
                      {step.role === "critic" ? "Statistician Critic" : "Analyst Agent"}
                      <span className="text-zinc-400 font-normal">
                        (Round {step.round})
                      </span>
                    </span>
                    {step.verdict && (
                      <span className="px-1.5 py-0.5 rounded bg-black/40 text-[10px]">
                        {step.verdict}
                      </span>
                    )}
                  </div>
                  <p className="whitespace-pre-wrap">{step.argument}</p>

                  {step.revised_code && (
                    <details className="mt-2 rounded-lg bg-black/40 border border-white/10 overflow-hidden">
                      <summary className="px-2 py-1 text-[11px] font-mono cursor-pointer text-zinc-400 hover:text-zinc-200">
                        View Self-Corrected Code
                      </summary>
                      <pre className="p-2 text-[11px] font-mono overflow-x-auto text-zinc-200">
                        <code>{step.revised_code}</code>
                      </pre>
                    </details>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
