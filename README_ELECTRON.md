# 🚀 ErgoGuard Electron Desktop Migration - Complete Guide

## Overview

You're migrating **ErgoGuard International** from a web-based app (HTTP server + browser) to a **native Electron desktop application** with:

✅ Native OS notifications (Windows/macOS/Linux)  
✅ System tray background execution  
✅ Secure IPC communication via contextBridge  
✅ Local asset management  
✅ Professional installer (.exe, .dmg, .AppImage)  

---

## 📋 What You're Getting

### Files Created for You

| File | Purpose |
|------|---------|
| `main.js` | Electron main process (window lifecycle, tray, notifications) |
| `preload.js` | Security layer (contextBridge for safe IPC) |
| `package.json` | Dependencies, scripts, build config |
| `.gitignore` | Ignore node_modules, dist/, etc. |
| **GUIDES** for reference: |
| `ELECTRON_MIGRATION_GUIDE.md` | Project setup & folder structure |
| `ELECTRON_INTEGRATION_GUIDE.md` | How to modify index.html |
| `ELECTRON_ARCHITECTURE.md` | Diagrams & detailed flows |
| `ELECTRON_QUICKSTART.md` | Step-by-step checklist |

### What Stays the Same

✅ Your `index.html` (with minor modifications to showBreakReminder)  
✅ Your JavaScript logic (MediaPipe, posture analysis, charts)  
✅ Your Tailwind CSS styling  
✅ Your multilingual translations  

---

## ⚡ Quick Start (10 minutes)

### Step 1: Prepare your folder

```bash
cd "c:\Code S4 Romania\ergoguard 02"
```

Ensure you have:
- `index.html` ✅
- `main.js` (paste full content from guide)
- `preload.js` (paste full content from guide)
- `package.json` (paste full content from guide)
- `.gitignore` (paste content)
- `assets/` folder with an icon image

### Step 2: Install dependencies

```bash
npm install --save-dev electron electron-builder electron-reloader
```

**What this does:**
- Downloads Electron (127 MB)
- Installs build tools for creating installers
- Installs hot-reload for development

### Step 3: Run the app

```bash
npm start
```

**Expected result:**
- New window opens with your app
- Your `index.html` loads
- MediaPipe detection ready to start

### Step 4: Test tray & minimize

- Click the minimize button → app hides to system tray ✅
- Click tray icon → app reappears ✅
- Right-click tray → context menu appears ✅

### Step 5: Modify index.html (10 minutes)

Find this function (around line 1470):

```javascript
function showBreakReminder() {
  // Get content for current language, fallback to English
  const content = breakContent[lang] || breakContent["English"];
  
  // Populate image container
  const imageContainer = document.getElementById("break-media-container");
  imageContainer.innerHTML = `
    <img src="${content.imageUrl}" 
         class="w-full max-h-64 object-contain rounded mb-4" 
         alt="Stretch Guide" />
  `;
  // ... rest of code
}
```

**Replace with:**

```javascript
function showBreakReminder() {
  const content = breakContent[lang] || breakContent["English"];
  
  // ✅ NEW: Use native OS notification if running in Electron
  if (window.electronAPI) {
    window.electronAPI.showNotification({
      title: t.break_msg || 'Break Time! 🏃',
      body: content.title || 'Time to stand up and stretch...',
      icon: 'assets/icon.png'
    });
    
    // Still show modal for detailed stretches
    showBreakReminderModal(content);
    
  } else {
    // WEB: Fall back to DOM modal
    showBreakReminderModal(content);
  }
}

// NEW: Extract modal display to separate function
function showBreakReminderModal(content) {
  const imageContainer = document.getElementById("break-media-container");
  imageContainer.innerHTML = `
    <img src="${content.imageUrl}" 
         class="w-full max-h-64 object-contain rounded mb-4" 
         alt="Stretch Guide" />
  `;
  
  const contentContainer = document.getElementById("break-stretch-content");
  const actionsList = content.actions
    .map(action => `<li class="text-sm text-[var(--muted)] leading-relaxed mb-2">• ${action}</li>`)
    .join("");
  
  contentContainer.innerHTML = `
    <h3 class="text-base font-bold text-[var(--accent)] mb-3">${content.title}</h3>
    <ul class="list-none p-0 m-0">${actionsList}</ul>
  `;
  
  document.getElementById("modal-break-reminder").classList.remove("hidden");
  isBreakModalOpen = true;
  playBeep(440, 0.3);
}
```

### Step 6: Test the notification

Add this to your `onStart()` function temporarily for testing:

```javascript
function onStart() {
  // ... existing code ...
  
  // TEST: Set break interval to 5 seconds instead of 60 minutes
  if (window.electronAPI) {
    intervalSecs = 5; // 5 seconds for quick testing
  }
  
  // ... rest of code ...
}
```

Run and wait 5 seconds → you should see a native notification! 🎉

### Step 7: Build the installer

```bash
npm run build-win
```

**Output:** 
- `dist/ErgoGuard-1.0.0.exe` (NSIS installer)
- `dist/ErgoGuard-1.0.0-portable.exe` (standalone)

Distribute the .exe to users!

---

## 📁 Folder Structure (Final)

```
c:\Code S4 Romania\ergoguard 02\
├── main.js                              ✅ Created
├── preload.js                           ✅ Created
├── index.html                           ✅ Modified (showBreakReminder)
├── package.json                         ✅ Created
├── .gitignore                           ✅ Created
├── assets/
│   ├── icon.png                        ✅ Create this (256×256)
│   └── (optional) neck-stretch.jpg
├── node_modules/                        (auto-generated by npm)
├── dist/                                (auto-generated by build)
└── Guides (for reference):
    ├── ELECTRON_MIGRATION_GUIDE.md
    ├── ELECTRON_INTEGRATION_GUIDE.md
    ├── ELECTRON_ARCHITECTURE.md
    └── ELECTRON_QUICKSTART.md
```

---

## 🎨 Create Your App Icon

### Option A: Use an existing image (fastest)

```bash
# Any 256×256 PNG works:
# 1. Take a screenshot of your app
# 2. Resize to 256×256 in Paint/Photoshop
# 3. Save as assets/icon.png
```

### Option B: Online icon converter

1. Find a `.png` image you like (256×256+)
2. Visit: https://icoconvert.com/
3. Upload PNG → Download `.ico`
4. Save both to `assets/`

### Option C: Generate from text (quick and dirty)

```python
from PIL import Image, ImageDraw, ImageFont

# Create a 256×256 image
img = Image.new('RGB', (256, 256), color='green')
draw = ImageDraw.Draw(img)

# Add text
draw.text((50, 110), "ErgoGuard", fill='white')

img.save('assets/icon.png')
```

**Minimum requirement:** `assets/icon.png` at 256×256 pixels

---

## 🔄 Development Workflow

### During development:

```bash
# Terminal 1: Your app
npm start

# Once something breaks, Ctrl+C and restart
npm start

# DevTools: Ctrl+I in the app window
```

### For production/release:

```bash
# Build Windows installer
npm run build-win

# Build macOS (on macOS)
npm run build-mac

# Build Linux
npm run build-linux

# Output in ./dist/ folder
```

---

## 🐛 Common Issues & Fixes

### ❌ "Cannot find module 'electron-reloader'"
```bash
npm install --save-dev electron-reloader
```

### ❌ App launches but loads blank page
- Check console: `Ctrl+I` in app
- Verify `index.html` exists in app root
- Verify `preload.js` path in `main.js` is correct

### ❌ Notification doesn't appear
- Make sure `window.electronAPI` is available (check DevTools console)
- Verify preload.js is being loaded
- Test: `window.electronAPI.log('test')` in console
- On Windows: Check Settings → Notifications & actions (enable app notifications)

### ❌ Tray icon doesn't show
- Create `assets/icon.png` (256×256)
- Verify path in `main.js`: `path.join(__dirname, 'assets', 'icon.png')`
- Restart app

### ❌ Images showing 404 in network tab
- Your wiki URL (`https://upload.wikimedia.org/...`) should work fine ✅
- If using local images, use `assets/filename.jpg` (not `./assets/`)
- Never use hardcoded paths like `C:\...` (Electron won't find them)

### ❌ Build fails: "No code signing certificate"
- On Windows: This is optional for development
- For distribution, you can sign later or skip for now
- To skip: Remove the `sign` property from `package.json` → `build.win`

---

## 🚀 Advanced Topics

### Custom data storage
```javascript
// main.js: Save app data in user home directory
const { app } = require('electron');
const dataPath = path.join(app.getPath('userData'), 'data.json');
// Read/write JSON for settings, session history, etc.
```

### Auto-updates
```bash
npm install electron-updater
# See electron-updater docs for GitHub releases integration
```

### Code signing (macOS/Windows)
```bash
# For professional distribution, sign your installer
# This requires certificates from Apple/Microsoft
# Beyond scope of this guide - see electron-builder docs
```

---

## 📞 Key Resources

| Topic | Resource |
|-------|----------|
| Electron Basics | https://www.electronjs.org/docs |
| IPC Communication | https://www.electronjs.org/docs/latest/api/ipc-main |
| contextBridge | https://www.electronjs.org/docs/latest/tutorial/context-isolation |
| Electron Builder | https://www.electron.build/ |
| Native Notifications | https://www.electronjs.org/docs/latest/api/notification |

---

## ✅ Verification Checklist

Before building:

- [ ] `npm install` completed without errors
- [ ] `npm start` launches your app
- [ ] App window displays `index.html` (check title)
- [ ] MediaPipe loads (camera permissions requested)
- [ ] Minimize button hides to tray
- [ ] Tray icon visible in system tray
- [ ] Right-click tray → menu appears
- [ ] Temporarily set break interval to 5 sec
- [ ] Wait 5 seconds → native notification appears
- [ ] Click notification → app comes to foreground
- [ ] No console errors (Ctrl+I in app)
- [ ] `assets/icon.png` exists (256×256)

---

## 🎯 Summary of Changes

| Component | Change | Why |
|-----------|--------|-----|
| **index.html** | Modify `showBreakReminder()` | Use native notifications in Electron, DOM modal in web |
| **Add main.js** | Electron entry point | Handles app lifecycle, tray, window creation |
| **Add preload.js** | IPC bridge | Securely expose APIs to Renderer |
| **Add package.json** | Dependencies | Install Electron and build tools |
| **Create assets/** | Icon storage | App icon for taskbar and installer |
| **Add .gitignore** | VCS config | Don't commit `node_modules/` |

**No other changes needed!** Your posture detection, timers, translations all stay the same.

---

## 🎉 You're Ready!

1. **Copy files into your folder** (main.js, preload.js, package.json, .gitignore)
2. **Run `npm install`**
3. **Run `npm start`** to test
4. **Modify `index.html`** (showBreakReminder function)
5. **Build with `npm run build-win`**
6. **Share the .exe!** 🚀

---

## 💭 Questions?

Refer to:
- `ELECTRON_QUICKSTART.md` — Step-by-step checklist
- `ELECTRON_INTEGRATION_GUIDE.md` — Code examples
- `ELECTRON_ARCHITECTURE.md` — Diagrams & flows
- `ELECTRON_MIGRATION_GUIDE.md` — Setup details

**You've got this!** Let's make ErgoGuard a professional desktop app! 🎉
