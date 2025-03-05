import React, { useEffect, useState } from "react";
import { fetchProjects, addProject, deleteProject } from "../api";

function ProjectsScreen() {
  const [projects, setProjects] = useState([]);
  const [newProject, setNewProject] = useState("");

  useEffect(() => {
    async function loadProjects() {
      const data = await fetchProjects();
      setProjects(data);
    }
    loadProjects();
  }, []);

  const handleAddProject = async () => {
    if (!newProject.trim()) return;
    const project = { name: newProject };
    const addedProject = await addProject(project);
    setProjects([...projects, addedProject]);
    setNewProject("");
  };

  const handleDeleteProject = async (projectId) => {
    await deleteProject(projectId);
    setProjects(projects.filter((p) => p.id !== projectId));
  };

  return (
    <div>
      <h2>Projects</h2>
      <ul>
        {projects.map((project) => (
          <li key={project.id}>
            {project.title}
            <button onClick={() => handleDeleteProject(project.id)}>Delete</button>
          </li>
        ))}
      </ul>
      <input 
        type="text" 
        value={newProject} 
        onChange={(e) => setNewProject(e.target.value)} 
        placeholder="Add a new project" 
      />
      <button onClick={handleAddProject}>Add</button>
    </div>
  );
}

export default ProjectsScreen;
