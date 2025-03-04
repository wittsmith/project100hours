import React, { useEffect, useState } from 'react';

function App() {
  const [backendData, setBackendData] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then(response => response.json())
      .then(data => setBackendData(data.message))
      .catch(error => console.error('Error fetching backend:', error));
  }, []);

  return (
    <div>
      <h1>Project 100 Hours</h1>
      <p>Backend says: {backendData ? backendData : 'Loading...'}</p>
    </div>
  );
}

export default App;
