const API_BASE_URL = "http://3.86.163.231:8000"; // Replace with your EC2 IP
 // Replace with actual EC2 IP

// 📝 Fetch all "I Will" tasks
async function fetchIWillTasks() {
  try {
    const response = await fetch(`${API_BASE_URL}/i_wills`);
    if (!response.ok) throw new Error("Failed to fetch tasks");
    return await response.json();
  } catch (error) {
    console.error("Error fetching tasks:", error);
    return [];
  }
}

// ➕ Create a new "I Will" task
async function addIWillTask(task) {
  try {
    const response = await fetch(`${API_BASE_URL}/i_wills`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(task),
    });
    return await response.json();
  } catch (error) {
    console.error("Error adding task:", error);
  }
}

// 🗑️ Delete an "I Will" task
async function deleteIWillTask(taskId) {
  try {
    await fetch(`${API_BASE_URL}/i_wills/${taskId}`, { method: "DELETE" });
  } catch (error) {
    console.error("Error deleting task:", error);
  }
}

// ✏️ Update an "I Will" task
async function updateIWillTask(taskId, updatedTask) {
  try {
    const response = await fetch(`${API_BASE_URL}/i_wills/${taskId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updatedTask),
    });
    return await response.json();
  } catch (error) {
    console.error("Error updating task:", error);
  }
}

// 📂 Fetch all projects
async function fetchProjects() {
  try {
    const response = await fetch(`${API_BASE_URL}/projects`);
    if (!response.ok) throw new Error("Failed to fetch projects");
    return await response.json();
  } catch (error) {
    console.error("Error fetching projects:", error);
    return [];
  }
}

// ➕ Create a new project
async function addProject(project) {
  try {
    const response = await fetch(`${API_BASE_URL}/projects`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(project),
    });
    return await response.json();
  } catch (error) {
    console.error("Error adding project:", error);
  }
}

// 🗑️ Delete a project
async function deleteProject(projectId) {
  try {
    await fetch(`${API_BASE_URL}/projects/${projectId}`, { method: "DELETE" });
  } catch (error) {
    console.error("Error deleting project:", error);
  }
}

// ✏️ Update a project
async function updateProject(projectId, updatedProject) {
  try {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updatedProject),
    });
    return await response.json();
  } catch (error) {
    console.error("Error updating project:", error);
  }
}

// 📋 Fetch tasks within a project
async function fetchProjectTasks(projectId) {
  try {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}/tasks`);
    if (!response.ok) throw new Error("Failed to fetch tasks");
    return await response.json();
  } catch (error) {
    console.error("Error fetching tasks:", error);
    return [];
  }
}

// ➕ Add a task to a project
async function addTaskToProject(projectId, task) {
  try {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(task),
    });
    return await response.json();
  } catch (error) {
    console.error("Error adding task:", error);
  }
}

// 🗑️ Delete a task within a project
async function deleteProjectTask(projectId, taskId) {
  try {
    await fetch(`${API_BASE_URL}/projects/${projectId}/tasks/${taskId}`, { method: "DELETE" });
  } catch (error) {
    console.error("Error deleting task:", error);
  }
}

// 🕒 Start a work session
async function startWorkSession(session) {
  try {
    const response = await fetch(`${API_BASE_URL}/work_sessions/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(session),
    });
    return await response.json();
  } catch (error) {
    console.error("Error starting work session:", error);
  }
}

// 🕒 Stop a work session
async function stopWorkSession(session) {
  try {
    const response = await fetch(`${API_BASE_URL}/work_sessions/stop`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(session),
    });
    return await response.json();
  } catch (error) {
    console.error("Error stopping work session:", error);
  }
}

// 📝 Manually log a work session
async function logManualWorkSession(session) {
  try {
    const response = await fetch(`${API_BASE_URL}/work_sessions/log`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(session),
    });
    return await response.json();
  } catch (error) {
    console.error("Error logging work session:", error);
  }
}

// 📅 Fetch weekly Google Calendar events
async function fetchWeeklyCalendarEvents(startDate, endDate) {
  try {
    const url = `${API_BASE_URL}/calendar/week?start_date=${startDate}&end_date=${endDate}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error("Failed to fetch calendar events");
    return await response.json();
  } catch (error) {
    console.error("Error fetching calendar events:", error);
    return { error: error.message };
  }
}

// 🧠 Generate a project idea using LLM
async function generateProjectIdea(description) {
  try {
    const response = await fetch(`${API_BASE_URL}/llm/project_idea`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description }),
    });
    return await response.json();
  } catch (error) {
    console.error("Error generating project idea:", error);
  }
}

export {
  fetchIWillTasks, addIWillTask, deleteIWillTask, updateIWillTask,
  fetchProjects, addProject, deleteProject, updateProject,
  fetchProjectTasks, addTaskToProject, deleteProjectTask,
  startWorkSession, stopWorkSession, logManualWorkSession,
  fetchWeeklyCalendarEvents, generateProjectIdea
};
