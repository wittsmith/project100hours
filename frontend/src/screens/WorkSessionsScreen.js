import React from "react";
import { startWorkSession, stopWorkSession } from "../api";

function WorkSessionsScreen() {
  const projectId = 1; // Replace with dynamic project selection later

  return (
    <div>
      <h2>Work Sessions</h2>
      <button onClick={() => startWorkSession(projectId)}>Start Work Session</button>
      <button onClick={() => stopWorkSession(1)}>Stop Work Session</button>
    </div>
  );
}

export default WorkSessionsScreen;
