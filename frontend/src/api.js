const API_BASE_URL = "http://3.86.163.231:8000"; // Replace with actual EC2 IP

async function fetchTasks() {
  try {
    const response = await fetch(`${API_BASE_URL}/i_wills`);
    if (!response.ok) throw new Error("Failed to fetch tasks");
    return await response.json();
  } catch (error) {
    console.error("Error fetching tasks:", error);
    return [];
  }
}

async function addTask(task) {
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

export { fetchTasks, addTask };
