const { app, BrowserWindow } = require("electron");
const path = require("path");

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: false,  // Allow JavaScript execution
    }
  });

  win.loadURL("http://localhost:3000").catch((err) => {
    console.error("Failed to load React:", err);
  });

  win.webContents.openDevTools(); // Open DevTools automatically
}

app.whenReady().then(createWindow);
