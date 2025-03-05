import React, { useEffect, useState } from "react";
import { fetchTasks, addTask } from "../api";

const Home = () => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  useEffect(() => {
    async function loadTasks() {
      const data = await fetchTasks();
      setTasks(data);
    }
    loadTasks();
  }, []);

  const handleAddTask = async () => {
    if (!newTask.trim()) return;
    const task = { action: newTask, date: new Date().toISOString().split("T")[0] };
    await addTask(task);
    setTasks([...tasks, task]);  // Update UI optimistically
    setNewTask("");
  };

  return (
    <div>
      <h1>Project 100 Hours</h1>
      <h2>I Will - To-Do List</h2>
      <ul>
        {tasks.map((task, index) => (
          <li key={index}>{task.action} ({task.date})</li>
        ))}
      </ul>
      <input 
        type="text" 
        value={newTask} 
        onChange={(e) => setNewTask(e.target.value)} 
        placeholder="Add a task"
      />
      <button onClick={handleAddTask}>Add</button>
    </div>
  );
};

export default Home;
