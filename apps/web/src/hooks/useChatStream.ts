"use client";

import { useState, useCallback } from "react";
import { ChatMessage, ReflexionStep } from "@/lib/types";

export function useChatStream() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [activeFigures, setActiveFigures] = useState<any[]>([]);
  const [activeCode, setActiveCode] = useState<string>("");
  const [activeStdout, setActiveStdout] = useState<string>("");

  const sendMessage = useCallback(
    async (sessionId: string, prompt: string) => {
      if (!prompt.trim() || isStreaming) return;

      const userMsgId = `usr_${Date.now()}`;
      const assistantMsgId = `ast_${Date.now() + 1}`;

      const userMsg: ChatMessage = {
        id: userMsgId,
        role: "user",
        content: prompt,
      };

      const initialAssistantMsg: ChatMessage = {
        id: assistantMsgId,
        role: "assistant",
        content: "",
        status: "generating_code",
        figures: [],
        reflexionSteps: [],
      };

      setMessages((prev) => [...prev, userMsg, initialAssistantMsg]);
      setIsStreaming(true);

      try {
        const response = await fetch(`/api/v1/sessions/${sessionId}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt, stream: true }),
        });

        if (!response.ok || !response.body) {
          throw new Error(`Chat request failed: ${response.statusText}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let buffer = "";

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const frames = buffer.split("\n\n");
          // Keep the last partial frame in the buffer
          buffer = frames.pop() || "";

          for (const frame of frames) {
            const lines = frame.split("\n");
            let eventType = "";
            let dataStr = "";

            for (const line of lines) {
              if (line.startsWith("event: ")) {
                eventType = line.replace("event: ", "").trim();
              } else if (line.startsWith("data: ")) {
                dataStr = line.replace("data: ", "").trim();
              }
            }

            if (!eventType || !dataStr) continue;

            let payload: any = {};
            try {
              payload = JSON.parse(dataStr);
            } catch {
              continue;
            }

            setMessages((prev) =>
              prev.map((msg) => {
                if (msg.id !== assistantMsgId) return msg;

                switch (eventType) {
                  case "execution_status":
                    return { ...msg, status: payload.status };

                  case "code_generated":
                    setActiveCode(payload.code || "");
                    return {
                      ...msg,
                      code: payload.code,
                      thought: payload.thought,
                      status: "running_sandbox",
                    };

                  case "execution_stdout":
                    setActiveStdout(payload.stdout || "");
                    return { ...msg, stdout: payload.stdout };

                  case "chart_generated":
                    if (payload.spec) {
                      setActiveFigures((figs) => [...figs, payload.spec]);
                      const currentFigs = msg.figures || [];
                      return { ...msg, figures: [...currentFigs, payload.spec] };
                    }
                    return msg;

                  case "reflexion_step":
                    const step: ReflexionStep = {
                      attempt: payload.attempt,
                      error: payload.error,
                      status: payload.status,
                    };
                    const currentSteps = msg.reflexionSteps || [];
                    return {
                      ...msg,
                      status: "generating_code",
                      reflexionSteps: [...currentSteps, step],
                    };

                  case "token":
                    return {
                      ...msg,
                      content: (msg.content || "") + (payload.token || ""),
                      status: "synthesizing_insights",
                    };

                  case "turn_complete":
                    return {
                      ...msg,
                      status: "complete",
                      durationMs: payload.duration_ms,
                      activeVersion: payload.active_version,
                    };

                  case "error":
                    return {
                      ...msg,
                      status: "error",
                      content: (msg.content ? msg.content + "\n\n" : "") + `⚠️ Error: ${payload.error || payload.detail}`,
                    };

                  default:
                    return msg;
                }
              })
            );
          }
        }
      } catch (err: any) {
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMsgId
              ? {
                  ...msg,
                  status: "error",
                  content: `Connection error: ${err.message || "Failed to communicate with API"}`,
                }
              : msg
          )
        );
      } finally {
        setIsStreaming(false);
      }
    },
    [isStreaming]
  );

  return {
    messages,
    isStreaming,
    activeFigures,
    activeCode,
    activeStdout,
    sendMessage,
    setMessages,
  };
}
