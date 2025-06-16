const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let pyProc = null;

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false
    }
  });
  win.loadURL('http://127.0.0.1:5000');
}

function startPython() {
  pyProc = spawn('python', ['app.py'], { cwd: __dirname, shell: true });
  pyProc.stdout.on('data', data => console.log(`py: ${data}`));
  pyProc.stderr.on('data', data => console.error(`pyerr: ${data}`));
}

app.whenReady().then(() => {
  startPython();
  createWindow();
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('quit', () => {
  if (pyProc) pyProc.kill();
});
