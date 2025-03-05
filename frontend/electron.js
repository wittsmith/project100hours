const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
    }
  });

  win.loadURL("http://localhost:3000").catch((err) => {
    console.error("Failed to load React:", err);
  });

  win.webContents.openDevTools(); // Open DevTools for debugging
}

// Handle messages from React
ipcMain.on("message", (event, data) => {
  console.log("📩 Received from React:", data); // Debugging line
  event.reply("reply", "Hello from Electron! ✅"); // Send response to React
});

app.whenReady().then(createWindow);
