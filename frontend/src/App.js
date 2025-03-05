import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import HomeScreen from "./screens/HomeScreen";
import ProjectsScreen from "./screens/ProjectsScreen";
import TasksScreen from "./screens/TasksScreen";
import WorkSessionsScreen from "./screens/WorkSessionsScreen";

function App() {
  return (
    <Router>
      <div style={{ textAlign: "center", padding: "20px" }}>
        <h1>Project 100 Hours</h1>

        {/* Navigation Links */}
        <nav>
          <Link to="/" style={{ margin: "10px" }}>Home</Link>
          <Link to="/projects" style={{ margin: "10px" }}>Projects</Link>
          <Link to="/tasks" style={{ margin: "10px" }}>Tasks</Link>
          <Link to="/work-sessions" style={{ margin: "10px" }}>Work Sessions</Link>
        </nav>

        <Routes>
          <Route path="/" element={<HomeScreen />} />
          <Route path="/projects" element={<ProjectsScreen />} />
          <Route path="/tasks" element={<TasksScreen />} />
          <Route path="/work-sessions" element={<WorkSessionsScreen />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
