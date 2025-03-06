import React, { useEffect, useState } from "react";
import {
  fetchIWillTasks,
  addIWillTask,
  updateIWillTask,
  fetchWeeklyCalendarEvents,
} from "../api";

function HomeScreen() {
  const [iWillTasks, setIWillTasks] = useState([]);
  const [calendarEvents, setCalendarEvents] = useState([]);
  const [calendarError, setCalendarError] = useState(null);
  const [newIWill, setNewIWill] = useState({ action: "", date: "" });

  // 🔹 Fetch "I Will" tasks and calendar events
  useEffect(() => {
    async function loadData() {
      try {
        const iWillData = await fetchIWillTasks();
        console.log("✅ Fetched 'I Will' Tasks:", iWillData); // Debugging
  
        if (!Array.isArray(iWillData)) {
          console.error("❌ API Error: 'I Will' response is not an array!", iWillData);
          setIWillTasks([]);
        } else {
          setIWillTasks(iWillData);
        }
  
        // Get calendar events for the next 7 days
        const today = new Date();
        const startDate = today.toISOString().split("T")[0];
        const endDate = new Date(today.setDate(today.getDate() + 7))
          .toISOString()
          .split("T")[0];
  
        const calendarData = await fetchWeeklyCalendarEvents(startDate, endDate);
  
        if (calendarData.error) {
          setCalendarError(calendarData.error);
        } else {
          setCalendarEvents(calendarData);
        }
      } catch (error) {
        console.error("❌ Error loading data:", error);
      }
    }
  
    loadData();
  }, []);
  

  // ✅ Add a new "I Will" task
  const handleAddIWill = async () => {
    if (!newIWill.action.trim() || !newIWill.date) return;

    const iWillData = {
      action: newIWill.action,
      date: newIWill.date,
      completed: false,
    };

    try {
      const addedIWill = await addIWillTask(iWillData);
      setIWillTasks([...iWillTasks, addedIWill]); // Update UI
      setNewIWill({ action: "", date: "" }); // Clear input
    } catch (error) {
      console.error("❌ Error adding 'I Will' task:", error);
    }
  };

  // ✅ Mark "I Will" as complete
  const handleCompleteIWill = async (task) => {
    const updatedTask = { ...task, completed: true };

    try {
      await updateIWillTask(task.id, updatedTask);
      setIWillTasks(iWillTasks.map((t) => (t.id === task.id ? updatedTask : t))); // Update UI
    } catch (error) {
      console.error("❌ Error marking 'I Will' as complete:", error);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Welcome to Project 100 Hours</h2>
      <p>Manage your commitments and upcoming events.</p>

      {/* 🔹 Add New "I Will" Task */}
      <h3>Add an "I Will" Task</h3>
      <input
        type="text"
        placeholder="I will..."
        value={newIWill.action}
        onChange={(e) =>
          setNewIWill((prev) => ({ ...prev, action: e.target.value }))
        }
      />
      <input
        type="date"
        value={newIWill.date}
        onChange={(e) =>
          setNewIWill((prev) => ({ ...prev, date: e.target.value }))
        }
      />
      <button onClick={handleAddIWill}>Add</button>

      {/* 🔹 List All "I Will" Tasks */}
      <h3>"I Will" Tasks</h3>
      {iWillTasks.length === 0 ? (
        <p>No tasks available.</p>
      ) : (
        <ul>
          {iWillTasks.map((task) => (
            <li key={task.id}>
              {task.action} - {task.date}{" "}
              {!task.completed && (
                <button onClick={() => handleCompleteIWill(task)}>
                  ✅ Complete
                </button>
              )}
            </li>
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
              {event.title} - {event.start.dateTime || event.start.date}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default HomeScreen;
