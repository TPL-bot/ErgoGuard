# 🎯 ElectronJS Migration - Quick Reference Card

## 🚀 One-Liner to Get Started

```bash
cd "c:\Code S4 Romania\ergoguard 02" && npm install --save-dev electron electron-builder && npm start
```

---

## 📋 Files You Need (Copy-Paste Ready)

### ✅ main.js
**What:** Electron main process (app lifecycle, notifications, tray)  
**Where:** Root of your project  
**Status:** ✅ Already created for you (copy from guide)  

### ✅ preload.js
**What:** IPC security bridge  
**Where:** Root of your project  
**Status:** ✅ Already created for you (copy from guide)  

### ✅ package.json
**What:** Dependencies & build config  
**Where:** Root of your project  
**Status:** ✅ Already created for you (copy from guide)  

### ✅ index.html (MODIFY)
**What:** Your existing web app  
**Where:** Root of your project  
**Change:** Update `showBreakReminder()` function only  
**Lines to change:** Around 1470-1505  

### ✅ assets/icon.png
**What:** App icon for taskbar & installer  
**Where:** `assets/` folder  
**Size:** 256×256 pixels minimum  
**Format:** PNG  
**Create:** Take any image, resize to 256×256  

---

## 🔨 Command Cheatsheet

| Command | Purpose | Time |
|---------|---------|------|
| `npm install --save-dev electron` | Install Electron | 2 min |
| `npm start` | Run app in dev mode | instant |
| `npm run build-win` | Create .exe installer | 3 min |
| `npm run build-mac` | Create .dmg for macOS | 3 min |
| `npm run build-linux` | Create AppImage for Linux | 3 min |

---

## 🎨 Folder Structure Checklist

```
Your Project Root
├── ✅ main.js                    Copy from guide
├── ✅ preload.js                 Copy from guide
├── ✅ index.html                 MODIFY showBreakReminder()
├── ✅ package.json               Copy from guide
├── ✅ .gitignore                 Copy from guide
├── ✅ assets/icon.png            Create (256×256 PNG)
├── (auto) node_modules/          npm install creates this
├── (auto) dist/                  npm run build creates this
└── README_ELECTRON.md            Reading material
```

---

## 🔧 The ONE Change to index.html

**Find this (line ~1470):**
```javascript
function showBreakReminder() {
  const content = breakContent[lang] || breakContent["English"];
  const imageContainer = document.getElementById("break-media-container");
  imageContainer.innerHTML = `<img src="${content.imageUrl}" ... />`;
  // more DOM stuff...
}
```

**Replace with this:**
```javascript
function showBreakReminder() {
  const content = breakContent[lang] || breakContent["English"];
  
  if (window.electronAPI) {
    // ELECTRON: Use native notification
    window.electronAPI.showNotification({
      title: 'Break Time!',
      body: 'Time to stand up and stretch',
      icon: 'assets/icon.png'
    });
    showBreakReminderModal(content);
  } else {
    // WEB: Use DOM modal (fallback)
    showBreakReminderModal(content);
  }
}

// New helper function
function showBreakReminderModal(content) {
  document.getElementById("break-media-container").innerHTML = `
    <img src="${content.imageUrl}" class="w-full max-h-64 object-contain rounded mb-4" alt="Stretch Guide" />
  `;
  
  const actionsList = content.actions
    .map(a => `<li class="text-sm mb-2">• ${a}</li>`)
    .join("");
  
  document.getElementById("break-stretch-content").innerHTML = `
    <h3 class="text-base font-bold mb-3">${content.title}</h3>
    <ul class="list-none p-0 m-0">${actionsList}</ul>
  `;
  
  document.getElementById("modal-break-reminder").classList.remove("hidden");
  isBreakModalOpen = true;
  playBeep(440, 0.3);
}
```

---

## ⚡ Workflow

### Development
```bash
npm start             # Always restart if you change main.js or preload.js
Ctrl+I               # Open DevTools to debug
Ctrl+R               # Refresh app
Ctrl+C               # Stop app
```

### Testing Break Notification
In `onStart()`, add:
```javascript
intervalSecs = 5;  // Fire in 5 seconds for testing
```
Wait 5 seconds → notification appears ✅

### Building for Users
```bash
npm run build-win    # Creates dist/ErgoGuard-1.0.0.exe
                     # Share this file with users!
```

---

## ❌ Common Mistakes to Avoid

| ❌ DON'T | ✅ DO |
|----------|-------|
| `<img src="./assets/icon.png">` | `<img src="assets/icon.png">` |
| `<img src="C:\Users\...">` | Use relative paths only |
| Forget to create `assets/icon.png` | Create it first, **256×256 PNG** |
| Move `main.js` out of root | Keep it in **project root** |
| Edit `preload.js` path wrong | Copy exact path: `path.join(__dirname, 'preload.js')` |
| Forget `npm install` | Run it first! It's required |
| Use local `1.jpg` for notifications | Use Wikipedia URL (tested & works) |

---

## 🧪 Verification: Does It Work?

Run this test:
```bash
npm start
# Wait for app to open
# Minimize → should hide to tray ✅
# Click tray icon → should reappear ✅
# Right-click tray → menu appears ✅
# Watch console (Ctrl+I) for errors ❌
```

If all ✅ → you're ready to build!

---

## 📦 Build & Share

```bash
npm run build-win
# Output: dist/ErgoGuard-1.0.0.exe

# Share dist/ErgoGuard-1.0.0.exe with users
# They run it or install it
# Works on Windows 7+ with no dependencies!
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution | Time |
|---------|----------|------|
| "Cannot find electron" | `npm install --save-dev electron` | 2 min |
| App won't start | Check `preload.js` path in `main.js` | 1 min |
| No tray icon | Create `assets/icon.png` (256×256) | 5 min |
| Notification doesn't show | Check: `window.electronAPI.log('test')` in console | 2 min |
| Build fails | Remove code signing: delete `sign` from package.json | 1 min |

---

## 🎯 Success Checklist

- [ ] `npm install` ✅
- [ ] `npm start` launches app ✅
- [ ] Minimize → hides to tray ✅
- [ ] Tray icon visible ✅
- [ ] No console errors ✅
- [ ] Modify `showBreakReminder()` in index.html ✅
- [ ] Set `intervalSecs = 5` to test ✅
- [ ] Wait 5 seconds → notification pops ✅
- [ ] Reset `intervalSecs = 3600` for real use ✅
- [ ] `npm run build-win` creates .exe ✅
- [ ] Share with users! 🎉 ✅

---

## 📚 Where to Find Full Docs

| Question | See |
|----------|-----|
| How does the app work? | `README_ELECTRON.md` |
| What files do I need? | `ELECTRON_MIGRATION_GUIDE.md` |
| How do I code the changes? | `ELECTRON_INTEGRATION_GUIDE.md` |
| Show me diagrams | `ELECTRON_ARCHITECTURE.md` |
| Step-by-step checklist | `ELECTRON_QUICKSTART.md` |

---

## 💡 Pro Tips

1. **Keep it simple:** Don't touch more than `showBreakReminder()` in index.html
2. **Test in 5 seconds:** Temporarily set `intervalSecs = 5` during development
3. **Use the wiki image:** It's reliable and works offline-ish (cached by browser)
4. **Icon can be anything:** Your screenshot, logo, whatever – just 256×256 PNG
5. **Tray is optional:** App works fine without it, but users love minimizing to tray

---

## 🎉 That's It!

You now have everything to:
✅ Create a professional desktop app  
✅ Send native notifications  
✅ Use system tray  
✅ Build installers  
✅ Share with users  

**Go build! 🚀**
