import React from "react";
import { SwarmPhaseEvent } from "@/lib/types";
import {
  Code2,
  ShieldAlert,
  GitCompare,
  Terminal,
  Activity,
  Sparkles,
  CheckCircle2,
  Clock,
  Layers,
} from "lucide-react";

interface SwarmWorkflowStepperProps {
  currentPhase?: SwarmPhaseEvent | null;
  isStreaming: boolean;
}

interface StepConfig {
  key: string;
  label: string;
  agent: string;
  icon: React.ElementType;
  description: string;
}

const STEPS: StepConfig[] = [
  {
    key: "analyst_draft",
    label: "Analyst Code Draft",
    agent: "Analyst Agent",
    icon: Code2,
    description: "Generates vectorized pandas/numpy computational pipeline",
  },
  {
    key: "pre_critic_audit",
    label: "AST Peer Audit",
    agent: "Statistician Critic",
    icon: ShieldAlert,
    description: "AST checks: unlogged dropna, arbitrary head slicing, mean-of-means",
  },
  {
    key: "analyst_debate",
    label: "Critic Debate Loop",
    agent: "Debate Swarm",
    icon: GitCompare,
    description: "Autonomous 2-round deliberation when revisions required",
  },
  {
    key: "sandbox_execution",
    label: "Isolated Sandbox",
    agent: "Execution Kernel",
    icon: Terminal,
    description: "Safely runs validated code in stateful sandbox",
  },
  {
    key: "post_critic_verification",
    label: "Statistical Validity",
    agent: "Statistician Critic",
    icon: Activity,
    description: "Sample size (N >= 30), skewness vs median, causality check",
  },
  {
    key: "executive_synthesis",
    label: "Executive Synthesis",
    agent: "Executive Agent",
    icon: Sparkles,
    description: "Formulates grounded decision-ready takeaways",
  },
];

export const SwarmWorkflowStepper: React.FC<SwarmWorkflowStepperProps> = ({
  currentPhase,
  isStreaming,
}) => {
  if (!isStreaming && !currentPhase) return null;

  const currentStepKey = currentPhase?.phase || "analyst_draft";
  const currentIndex = STEPS.findIndex((s) => s.key === currentStepKey);

  return (
    <div className="w-full bg-[#1e1f20]/90 backdrop-blur-md border border-[#3c4043] rounded-2xl p-3.5 my-2 shadow-xl animate-in fade-in slide-in-from-top-2 duration-300">
      {/* Header bar */}
      <div className="flex items-center justify-between pb-2.5 mb-2.5 border-b border-[#3c4043]/60 text-xs">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold">
            <Layers className="w-3.5 h-3.5 animate-pulse" />
          </div>
          <div>
            <span className="font-semibold text-white tracking-wide">
              Multi-Agent Debate Swarm
            </span>
            <span className="text-zinc-400 ml-2 font-mono text-[11px]">
              Analyst + Statistician Pair
            </span>
          </div>
        </div>

        {currentPhase && (
          <div className="flex items-center gap-2 bg-[#2d2f31] px-2.5 py-1 rounded-full border border-indigo-500/30">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
            </span>
            <span className="text-[11px] font-medium text-indigo-200">
              {currentPhase.agent}: {currentPhase.description}
            </span>
            {currentPhase.round !== undefined && currentPhase.round > 0 && (
              <span className="px-1.5 py-0.2 rounded bg-amber-500/20 text-amber-300 font-mono text-[10px]">
                R{currentPhase.round}
              </span>
            )}
          </div>
        )}
      </div>

      {/* Stepper Progress Pipeline */}
      <div className="grid grid-cols-2 md:grid-cols-6 gap-2 pt-1">
        {STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isDone = currentIndex > idx;
          const isCurrent = currentIndex === idx;
          const isPending = currentIndex < idx;

          return (
            <div
              key={step.key}
              className={`flex flex-col p-2 rounded-xl transition-all border ${
                isCurrent
                  ? "bg-indigo-950/40 border-indigo-500/60 shadow-lg shadow-indigo-950/50 scale-[1.02]"
                  : isDone
                  ? "bg-[#18191a] border-emerald-500/30 opacity-90"
                  : "bg-[#131314]/60 border-zinc-800 opacity-50"
              }`}
            >
              <div className="flex items-center justify-between mb-1.5">
                <div
                  className={`w-6 h-6 rounded-lg flex items-center justify-center text-xs ${
                    isCurrent
                      ? "bg-indigo-500 text-white animate-bounce"
                      : isDone
                      ? "bg-emerald-500/20 text-emerald-400"
                      : "bg-zinc-800 text-zinc-500"
                  }`}
                >
                  {isDone ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <Icon className="w-3.5 h-3.5" />
                  )}
                </div>
                <span className="text-[10px] font-mono text-zinc-400">0{idx + 1}</span>
              </div>

              <div className="text-[11px] font-medium text-white truncate">
                {step.label}
              </div>
              <div className="text-[10px] text-zinc-400 truncate">
                {step.agent}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
