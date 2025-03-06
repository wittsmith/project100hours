require("dotenv").config({ path: "./frontend/.env" }); // ✅ Explicitly load from frontend
const { app, BrowserWindow, ipcMain } = require("electron");
const { google } = require("googleapis");
const path = require("path");

const CLIENT_ID = process.env.GOOGLE_CLIENT_ID;
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;
const REDIRECT_URI = process.env.GOOGLE_REDIRECT_URI;

console.log("✅ Loaded Google Client ID:", CLIENT_ID);

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  win.loadURL("http://localhost:3000");
}

app.whenReady().then(createWindow);
