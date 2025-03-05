import React, { useEffect, useState } from "react";
import { fetchProjects, fetchIWillTasks, fetchWeeklyCalendarEvents } from "../api";

function HomeScreen() {
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [calendarEvents, setCalendarEvents] = useState([]);
  const [calendarError, setCalendarError] = useState(null);

  // 🔹 Fetch projects, tasks, and calendar events automatically
  useEffect(() => {
    async function loadData() {
      try {
        const projectsData = await fetchProjects();
        const tasksData = await fetchIWillTasks();

        // Get calendar events for the next 7 days
        const today = new Date();
        const startDate = today.toISOString().split("T")[0];
        const endDate = new Date(today.setDate(today.getDate() + 7)).toISOString().split("T")[0];
        
        const calendarData = await fetchWeeklyCalendarEvents(startDate, endDate);

        if (calendarData.error) {
          setCalendarError(calendarData.error); // Display error message
        } else {
          setCalendarEvents(calendarData);
        }

        setProjects(projectsData);
        setTasks(tasksData);
      } catch (error) {
        console.error("❌ Error loading data:", error);
      }
    }

    loadData();
  }, []);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Welcome to Project 100 Hours</h2>
      <p>Manage your projects, tasks, and upcoming events.</p>

      {/* 🔹 List All Projects */}
      <h3>Projects</h3>
      {projects.length === 0 ? (
        <p>No projects available.</p>
      ) : (
        <ul>
          {projects.map((project) => (
            <li key={project.id}>{project.name}</li>
          ))}
        </ul>
      )}

      {/* 🔹 List All Tasks */}
      <h3>Tasks</h3>
      {tasks.length === 0 ? (
        <p>No tasks available.</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <li key={task.id}>{task.action} (Due: {task.date})</li>
          ))}
        </ul>
      )}

      {/* 🔹 Google Calendar Events */}
      <h3>Upcoming Events</h3>
      {calendarError ? (
        <p style={{ color: "red" }}>❌ Error: {calendarError}</p>
      ) : calendarEvents.length === 0 ? (
        <p>No upcoming events.</p>
      ) : (
        <ul>
          {calendarEvents.map((event, index) => (
            <li key={index}>
              {event.summary} - {event.start.dateTime || event.start.date}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default HomeScreen;
