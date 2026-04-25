import React, { useState, useRef, useEffect } from "react";
import api from "../api/apiClient";

export default function AgentChat() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const boxRef = useRef(null);

  useEffect(() => {
    if (boxRef.current) {
      boxRef.current.scrollTop = boxRef.current.scrollHeight;
    }
  }, [messages]);

  const normalizeResult = (data) => {
    if (data === undefined || data === null) return null;
    return data;
  };

  const renderResult = (data) => {
    if (!data) return "No data returned.";

    // ---------- Vendors ----------
    if (Array.isArray(data)) {
      if (data.length === 0) return "No records found.";

      if (data[0]?.code && data[0]?.name) {
        return (
          <>
            <div className="font-medium mb-2">
              {data.length} vendor(s) found:
            </div>
            <ul className="list-disc pl-5 space-y-1">
              {data.map((v, i) => (
                <li key={i}>
                  <strong>{v.name}</strong> ({v.code})
                  {v.contact_email && (
                    <span className="text-gray-500">
                      {" "}
                      – {v.contact_email}
                    </span>
                  )}
                </li>
              ))}
            </ul>
          </>
        );
      }

      return <pre>{JSON.stringify(data, null, 2)}</pre>;
    }

    // ---------- Objects ----------
    if (typeof data === "object") {
      return <pre>{JSON.stringify(data, null, 2)}</pre>;
    }

    return String(data);
  };

  // send promot to agent
  const send = async () => {
    if (!prompt.trim()) return;

    setMessages((m) => [...m, { role: "user", text: prompt }]);
    setPrompt("");
    setLoading(true);

    try {
      const res = await api.askAgent(prompt);
      const payload = res.data;

      // FUNCTION RESULT
      if (payload?.type === "function_result") {
        const normalized = normalizeResult(payload.data);

        setMessages((m) => [
          ...m,
          {
            role: "assistant",
            text: (
              <>
                {payload.summary && (
                  <div className="mb-2 font-medium text-gray-700">
                    {payload.summary}
                  </div>
                )}
                {renderResult(normalized)}
              </>
            ),
          },
        ]);
        return;
      }

      // NORMAL MESSAGE
      if (payload?.type === "message") {
        setMessages((m) => [
          ...m,
          {
            role: "assistant",
            text: payload.content || "No response returned.",
          },
        ]);
        return;
      }

      // ERROR
      if (payload?.error) {
        setMessages((m) => [
          ...m,
          { role: "assistant", text: `Error: ${payload.error}` },
        ]);
        return;
      }

      // FALLBACK
      setMessages((m) => [
        ...m,
        { role: "assistant", text: renderResult(payload) },
      ]);
    } catch {
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          text: "Error: Unable to reach agent service.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div
        ref={boxRef}
        className="max-h-96 overflow-y-auto mb-4 space-y-4"
      >
        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex ${
              m.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`rounded-lg p-3 max-w-[80%] ${
                m.role === "user"
                  ? "bg-primary text-white"
                  : "bg-gray-50 text-gray-800"
              }`}
            >
              {typeof m.text === "string" ? (
                <div className="whitespace-pre-wrap">{m.text}</div>
              ) : (
                m.text
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-3">
        <textarea
          rows="2"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="flex-1 rounded-lg border border-gray-200 px-3 py-2"
          placeholder="Ask the agent about vendors or purchase orders..."
        />
        <button
          onClick={send}
          disabled={loading}
          className="rounded-lg bg-primary text-white px-4 py-2"
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>
    </div>
  );
}
