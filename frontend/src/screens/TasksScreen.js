import React, { useEffect, useState } from "react";
import { fetchProjectTasks, addTaskToProject, deleteProjectTask } from "../api";

function TasksScreen() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");
  const projectId = 1; // Replace with dynamic project selection later

  useEffect(() => {
    async function loadTasks() {
      const data = await fetchProjectTasks(projectId);
      setTasks(data);
    }
    loadTasks();
  }, []);

  const handleAddTask = async () => {
    if (!newTask.trim()) return;
    const task = { title: newTask, due_date: new Date().toISOString().split("T")[0] };
    const addedTask = await addTaskToProject(projectId, task);
    setTasks([...tasks, addedTask]);
    setNewTask("");
  };

  const handleDeleteTask = async (taskId) => {
    await deleteProjectTask(projectId, taskId);
    setTasks(tasks.filter((task) => task.id !== taskId));
  };

  return (
    <div>
      <h2>Tasks</h2>
      <ul>
      {tasks && tasks.length > 0 ? (
        tasks.map(task => (
          <div key={task.id}>{task.title}</div>
        ))
      ) : (
        <p>No tasks available.</p>
      )}

      </ul>
      <input 
        type="text" 
        value={newTask} 
        onChange={(e) => setNewTask(e.target.value)} 
        placeholder="Add a new task" 
      />
      <button onClick={handleAddTask}>Add</button>
    </div>
  );
}

export default TasksScreen;
