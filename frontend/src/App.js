import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState("Waiting for Electron...");

  useEffect(() => {
    if (window.electronAPI) {
      window.electronAPI.receiveFromMain("reply", (data) => {
        setMessage(data);
      });

      window.electronAPI.sendToMain("message", "Hello from React!");
    }
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Project 100 Hours</h1>
      <p>Electron says: {message}</p>
    </div>
  );
}

export default App;
