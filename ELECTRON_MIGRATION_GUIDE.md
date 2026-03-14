# ErgoGuard Electron Desktop Migration Guide

## Step 1: Initialize the Electron Project

Run these commands in your workspace root:

```bash
# Initialize npm if you haven't already
npm init -y

# Install Electron and necessary dependencies
npm install --save-dev electron
npm install --save-dev electron-builder

# Optional: For auto-reload during development
npm install --save-dev electron-reloader
```

---

## Step 2: Project Structure

Create this folder layout in `c:\Code S4 Romania\ergoguard 02\`:

```
├── main.js                    # Main process (Electron lifecycle, tray, notifications)
├── preload.js                 # Preload script (IPC bridge)
├── package.json               # npm configuration (see below)
├── index.html                 # Your existing web app (Renderer process)
├── assets/                    # Folder for local images
│   └── neck-stretch.jpg       # (optional - for fallback local image)
├── src/
│   └── (if you want to organize JS separately - optional)
└── build/                     # Electron builder output (auto-generated)
```

**Key Point:** Keep `index.html` and `main.js` in the ROOT directory for simplicity.

---

## Step 3: Complete package.json

```json
{
  "name": "ergoguard-international",
  "version": "1.0.0",
  "description": "AI Posture & Wellness Guardian - Desktop Edition",
  "main": "main.js",
  "homepage": "./",
  "scripts": {
    "start": "electron .",
    "dev": "electron . --dev",
    "build": "electron-builder",
    "build-win": "electron-builder --win",
    "build-mac": "electron-builder --mac",
    "build-linux": "electron-builder --linux"
  },
  "devDependencies": {
    "electron": "^latest",
    "electron-builder": "^24.6.4",
    "electron-reloader": "^1.2.3"
  },
  "build": {
    "appId": "com.ergoguard.international",
    "productName": "ErgoGuard International",
    "files": [
      "main.js",
      "preload.js",
      "index.html",
      "assets/**/*",
      "node_modules/**/*"
    ],
    "win": {
      "target": [
        "nsis",
        "portable"
      ],
      "icon": "assets/icon.ico"
    },
    "nsis": {
      "oneClick": false,
      "allowToChangeInstallationDirectory": true
    }
  }
}
```

---

## Step 4: Run the App

```bash
npm start
```

This will launch your Electron app with the local `index.html` loaded.

---

## Step 5: Asset Management Best Practices

### ✅ DO:
- Place images in `./assets/` folder (sibling to `index.html`)
- Reference in HTML as: `<img src="assets/neck-stretch.jpg">`
- Use absolute paths in IPC messages from Electron: `path.join(__dirname, 'assets', 'image.jpg')`

### ❌ DON'T:
- Use relative paths like `../assets` (unreliable in Electron)
- Mix local and remote URLs in the same array
- Trust browser caching in Electron (always force-refresh: `require('electron').app.reloadIgnoringCache()`)

### 🔧 For Your Break Modal Image:
Since your Wikipedia URL works fine, **keep it as the primary**:
```javascript
// In your breakContent dictionary
imageUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Neck_stretch.jpg/640px-Neck_stretch.jpg"
// Electron will load it fine - it has full internet access
```

---

## Step 6: IPC Communication Flow

**Main Process** (`main.js`) → sends native notifications  
**Renderer Process** (`index.html`) → calls `window.electronAPI.showNotification()`  
**Preload** (`preload.js`) → securely bridges them via `contextBridge`

Example from your `index.html`:
```javascript
// When break timer fires:
if (window.electronAPI) {
  window.electronAPI.showNotification({
    title: 'Break Time!',
    body: 'Time to stand up and stretch...',
    icon: 'assets/icon.png'
  });
} else {
  // Fallback for web version
  showBreakReminder();
}
```

---

## Ready? Proceed to the code files below! →
