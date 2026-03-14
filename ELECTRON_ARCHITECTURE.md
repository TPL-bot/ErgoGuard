# ErgoGuard Electron Architecture Diagram

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ERGOGUARD ELECTRON APP                             │
└─────────────────────────────────────────────────────────────────────────────┘

                          ┌─────────────────────┐
                          │   Main Process      │
                          │   (main.js)         │
                          └──────────┬──────────┘
                                     │
                  ┌──────────────────┼──────────────────┐
                  │                  │                  │
        ┌─────────▼────────┐ ┌──────▼──────┐ ┌────────▼─────────┐
        │  App Lifecycle   │ │ IPC Handler │ │ Native Features  │
        │  - create window │ │ - recv msgs │ │ - Notifications  │
        │  - quit/close    │ │ - tray cmds │ │ - Tray Icon      │
        │  - DevTools      │ │ - logging   │ │ - System Menus   │
        └──────────────────┘ └──────┬──────┘ └──────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  │       IPC Message Channel        │
                  │  (Secure contextBridge)          │
                  └─────────────────┬─────────────────┘
                                    │
        ┌──────────────────────────┐┌──────────────────────────┐
        │    Renderer Process      ││   Preload Script         │
        │    (index.html)          ││   (preload.js)           │
        │                          ││                          │
        │  • MediaPipe detection   ││  • contextBridge setup   │
        │  • Posture analysis      ││  • Expose safe APIs      │
        │  • Break timer logic     ││  • IPC send/receive      │
        │  • DOM modal UI          ││  • window.electronAPI    │
        │  • Chart.js reports      ││  • getAppVersion()       │
        │                          ││  • log()                 │
        │                          ││  • showNotification()    │
        │  CHANGE:                 ││  • onStartSession()      │
        │  Call window.electronAPI ││                          │
        │  instead of DOM modal    ││                          │
        │  when break fires        ││                          │
        └──────────────────────────┘└──────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      FILE & ASSET HIERARCHY                                │
│                                                                             │
│  c:\Code S4 Romania\ergoguard 02\                                          │
│  ├── main.js                    ◄─── Main Process (Electron lifecycle)     │
│  ├── preload.js                 ◄─── IPC Bridge (Security)                 │
│  ├── index.html                 ◄─── Renderer Process (Your web app)       │
│  ├── package.json               ◄─── Dependencies & build config           │
│  ├── assets/                    ◄─── Static Assets                         │
│  │   ├── icon.png              (256×256, app icon)                        │
│  │   ├── icon.ico              (Windows only, optional)                   │
│  │   └── neck-stretch.jpg      (Fallback local image, optional)           │
│  ├── node_modules/             ◄─── npm dependencies (not versioned)       │
│  ├── dist/                      ◄─── Build output (generated)              │
│  │   ├── ErgoGuard*.exe                                                    │
│  │   └── (other installers)                                               │
│  └── build/                     ◄─── Temp build folder (generated)         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Communication Flow: Break Notification Example

```
TIMELINE: Break Timer Fires (nextBreakAt reached)

┌─────────────────────────────────────────────────────────────────────────┐
│ Renderer Process (index.html)                                          │
│ ┌─────────────────────────────────────────────────────────────────┐    │
│ │ checkTimers(now)                                                │    │
│ │   if (now >= nextBreakAt && !isBreakModalOpen) {               │    │
│ │     isBreakModalOpen = true;                                    │    │
│ │     showBreakReminder();  ◄─── Timer fires!                    │    │
│ │   }                                                             │    │
│ │                                                                 │    │
│ │ function showBreakReminder() {                                 │    │
│ │   if (window.electronAPI) {  ◄─── Check if running in Electron │    │
│ │     window.electronAPI.showNotification({      [IPC SEND]      │    │
│ │       title: 'Break Time!',                                    │    │
│ │       body: 'Time to stretch...',                              │    │
│ │       icon: 'assets/icon.png'                                  │    │
│ │     });                                                         │    │
│ │   } else {                                                      │    │
│ │     // Fallback to DOM modal for web version                  │    │
│ │     showBreakReminderModal(content);                           │    │
│ │   }                                                             │    │
│ │ }                                                               │    │
│ └─────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────┬┘
                                                                        │
                    ┌───────────────── IPC ──────────────┐            │
                    │ ('show-break-notification', args) │            │
                    └───────────────────┬────────────────┘            │
                                        │                             │
                                        ▼                             │
┌─────────────────────────────────────────────────────────────────────┴──┐
│ Main Process (main.js)                                              │
│ ┌──────────────────────────────────────────────────────────────┐    │
│ │ ipcMain.on('show-break-notification', (event, args) => {    │    │
│ │                                                              │    │
│ │   const notification = new Notification({                    │    │
│ │     title: args.title,     ◄─── Extract from IPC args       │    │
│ │     body: args.body,                                         │    │
│ │     icon: args.icon,                                         │    │
│ │     silent: false,         ◄─── Play system sound            │    │
│ │     urgency: 'critical'    ◄─── Show prominently on Windows  │    │
│ │   });                                                         │    │
│ │                                                              │    │
│ │   notification.on('click', () => {  ◄─── User clicked!       │    │
│ │     mainWindow.show();                                       │    │
│ │     mainWindow.focus();    ◄─── Bring app to foreground      │    │
│ │   });                                                         │    │
│ │                                                              │    │
│ │   notification.show();     ◄─── Display native OS toast      │    │
│ │ })                                                            │    │
│ └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘

                        ▼

        ┌─────────────────────────────┐
        │  Windows/macOS/Linux        │
        │  Native Notification API    │
        │                             │
        │  ┌───────────────────────┐  │
        │  │ ⏰ Break Time!          │  │
        │  │ Time to stretch...      │  │
        │  │ [Action]                │  │
        │  └───────────────────────┘  │
        └─────────────────────────────┘

        User clicks → notification.on('click')
                   → mainWindow.show() & focus()
                   → App comes to foreground ✅
```

---

## 🔐 Security Model (contextBridge)

```
┌──────────────────────────────────────┐
│  Renderer Process (Sandboxed)        │
│  • NO direct access to Node.js       │
│  • NO require()                      │
│  • Can only access preload.js APIs   │
│                                      │
│  Code:                               │
│    window.electronAPI.log('msg')     │
│    window.electronAPI.showNotif(...) │
└──────────────────────┬─────────────────┘
                       │
         contextBridge (isolated bridge)
         ✅ Type-safe
         ✅ Limited API surface
         ✅ No privilege escalation
                       │
┌──────────────────────▼─────────────────┐
│  Preload Script (preload.js)           │
│  • Has Node.js + Electron access       │
│  • Carefully exposes only safe methods │
│                                        │
│  Code:                                 │
│    contextBridge.exposeInMainWorld(    │
│      'electronAPI', {                  │
│        showNotification: (args) => {   │
│          ipcRenderer.send(...)         │
│        }                               │
│      }                                 │
│    )                                   │
└──────────────────────┬──────────────────┘
                       │
              ipcRenderer (one-way IPC)
              Sends message to Main
                       │
┌──────────────────────▼──────────────────┐
│  Main Process (main.js)                 │
│  • Full Node.js + OS access             │
│  • Creates native notifications         │
│  • Manages system tray                  │
│  • Handles app lifecycle                │
│                                        │
│  Code:                                 │
│    ipcMain.on('show-break-notif', ...)│
│    new Notification({...})             │
│    new Tray(iconPath)                  │
└─────────────────────────────────────────┘

✅ Renderer cannot directly call OS APIs
✅ Renderer cannot access file system
✅ Renderer cannot run arbitrary Node.js
✅ Only explicitly exposed methods available
✅ Maximum security with full power
```

---

## 🔄 Data Flow: Asset Loading

```
FILE REQUEST: Image Display

index.html:
┌─────────────────────────┐
│ <img src="assets/..." > │
└──────────────┬──────────┘
               │
               ▼
    Browser File System
    (file:///__dirname/)
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
 Local Asset        External URL
 (file://)          (https://)
    │                     │
    ├─ assets/*.png       ├─ Wikipedia
    ├─ assets/*.jpg       ├─ CDN
    ├─ assets/icon.ico    ├─ Any HTTPS
    │                     │
    ✅ Works offline       ✅ Requires internet
    ✅ No 404 errors       ✅ Fallback needed
    (if files exist)       (if no internet)

YOUR STRATEGY:
✅ Primary: Wikipedia URL (works everywhere with internet)
✅ Fallback: Local assets/ folder (for offline)
✅ Never: Hardcode "1.jpg" local path (causes 404)
```

---

## 📦 Build & Distribution

```
npm run build-win
        │
        ▼
electron-builder
        │
    ┌───┴────────┐
    │           │
    ▼           ▼
  NSIS      Portable
 (setup)     (.exe)
    │           │
    ▼           ▼
dist/            dist/
├─ ErgoGuard         └─ ErgoGuard-Portable.exe
│  Setup 1.0.0.exe       (no installation needed)
│ (requires install)
│
└─ Installers folder
   ├─ en-US.nsh
   └─ (localization files)

User Experience:
  [Download ErgoGuard-1.0.0.exe]
        │
        ├─ Run NSIS installer
        │  ├─ Choose install location
        │  ├─ Create Start Menu shortcut
        │  ├─ Create Desktop shortcut
        │  └─ Run app
        │
        └─ Or run Portable.exe directly
           └─ No system modifications
```

---

## ✅ Checklist: Each Component

- [x] **main.js**
  - [x] App lifecycle (ready, quit, activate)
  - [x] Window creation & preload setup
  - [x] System tray with context menu
  - [x] IPC receiver for notifications
  - [x] Security: no nodeIntegration

- [x] **preload.js**
  - [x] contextBridge.exposeInMainWorld
  - [x] Expose showNotification()
  - [x] Expose onStartSession()
  - [x] Expose getPlatform(), getAppVersion()
  - [x] No direct window access

- [x] **index.html** (Your current file, just modify showBreakReminder)
  - [x] Check for window.electronAPI
  - [x] Call showNotification() if available
  - [x] Fallback to DOM modal
  - [ ] Update image paths (remove leading ./)

- [x] **package.json**
  - [x] electron-builder config
  - [x] Platform-specific icons
  - [x] npm scripts (start, build-win, etc)
  - [x] files array includes assets/

- [x] **assets/** folder
  - [ ] icon.png (256×256)
  - [ ] icon.ico (Windows, optional)
  - [ ] icon.icns (macOS, optional)

---

## 🚀 Next Action

1. Run Phase 1 setup in ELECTRON_QUICKSTART.md
2. Copy main.js, preload.js, package.json into your project
3. Run `npm install`
4. Run `npm start`
5. Test the app
6. Modify index.html's showBreakReminder()
7. Test notifications
8. Build: `npm run build-win`
9. Distribute the .exe!

---

**Questions?** Refer to `ELECTRON_INTEGRATION_GUIDE.md` for detailed code examples.
