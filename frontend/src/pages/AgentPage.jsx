import React from "react";
import AgentChat from "../components/AgentChat";

export default function AgentPage(){
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">APEX Agent</h1>
      <AgentChat />
    </div>
  );
}
