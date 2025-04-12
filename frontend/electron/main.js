const { app, BrowserWindow, session } = require("electron");
const path = require("path");

function createWindow() {
    const win = new BrowserWindow({
        width: 1000,
        height: 800, 
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            nodeIntegration: true,
            contextIsolation: false,
            webSecurity: false, // TODO: change when outside dev
        },
    });

    // Allow CORS
    session.defaultSession.webRequest.onBeforeSendHeaders((details, callback) => {
        callback({
            requestHeaders: {
                ...details.requestHeaders,
                'Access-Control-Allow-Origin': '*'
            }
        });
    });

    // Load the index.html file
    win.loadFile(path.join(__dirname, "index.html"));
}

app.whenReady().then(createWindow);