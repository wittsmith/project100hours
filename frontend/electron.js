const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false
    }
  });

  win.loadURL('http://localhost:3000');
}

// Log messages when receiving from React
ipcMain.on("message", (event, arg) => {
  console.log("Received from React:", arg);
  event.reply("reply", "Hello from Electron!");  // Send a reply back
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
