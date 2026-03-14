# ✅ ElectronJS Migration Checklist

## Phase 1: Setup (5 minutes)

- [ ] Open PowerShell/Terminal in `c:\Code S4 Romania\ergoguard 02\`
- [ ] Run: `npm init -y`
- [ ] Run: `npm install --save-dev electron electron-builder electron-reloader`
- [ ] Create `main.js` (copy from ELECTRON_MIGRATION_GUIDE.md)
- [ ] Create `preload.js` (copy from ELECTRON_MIGRATION_GUIDE.md)
- [ ] Update `package.json` (copy from ELECTRON_MIGRATION_GUIDE.md)

## Phase 2: Create Assets (5 minutes)

- [ ] Create `assets/` folder in app root
- [ ] Add app icon as `assets/icon.png` (256x256 minimum, PNG format)
  - Can be any image, but 256x256 PNG works best
  - For now, use any image: copy a screenshot or use an online converter
- [ ] (Optional on Windows) Generate `assets/icon.ico` from PNG

## Phase 3: Integrate IPC (10 minutes)

- [ ] Open `index.html` in VS Code
- [ ] Find `function showBreakReminder()` (around line 1470-1505)
- [ ] Replace with the code in `ELECTRON_INTEGRATION_GUIDE.md` Step 1
- [ ] Find `checkTimers(now)` function (around line 1267)
- [ ] Look for where it calls `showBreakReminder()` and ensure it's still there
- [ ] (Optional) Add tray listener code from Integration Guide Step 2

## Phase 4: Test (5 minutes)

```bash
# In PowerShell, from your app folder:
npm start
```

- [ ] App launches in window
- [ ] Form displays properly
- [ ] Click "Start ErgoGuard" → detection starts
- [ ] Window minimize → hides to tray
- [ ] Tray icon visible in system tray
- [ ] Right-click tray → context menu appears
- [ ] For testing break notification: temporarily set `nextBreakAt` to 3 seconds in checkTimers()

## Phase 5: Build (10 minutes)

```bash
# Build Windows installer:
npm run build-win

# Build portable .exe (no installer):
npm run build-win
# Look in ./dist for output
```

- [ ] Build completes without errors
- [ ] Check `./dist/` folder for `.exe` installer
- [ ] Test installer on another machine (optional)

---

## 📋 File Checklist

Make sure your app folder has:

```
✅ main.js                           (Electron main process)
✅ preload.js                        (IPC bridge)
✅ index.html                        (Your existing web app - modified)
✅ package.json                      (Updated with npm scripts)
✅ assets/icon.png                   (App icon)
✅ ELECTRON_MIGRATION_GUIDE.md       (This setup guide)
✅ ELECTRON_INTEGRATION_GUIDE.md     (Integration details)
✅ .gitignore                        (Don't commit node_modules etc)
```

---

## 🚀 Quick Test: One-Liner

```bash
npm install --save-dev electron && npm start
```

This will:
1. Install Electron
2. Launch your app immediately
3. Show any errors if something's wrong

---

## 💡 Pro Tips

1. **Fast icon creation**: Use your screenshot, resize to 256x256, save as `assets/icon.png`
2. **Test notifications**: Modify `checkTimers()` to set break time to 5 seconds temporarily
3. **DevTools**: Uncomment `mainWindow.webContents.openDevTools()` in main.js to debug
4. **Hot reload**: electron-reloader will auto-restart when you modify main.js or preload.js
5. **Build for prod**: Use `npm run build-win` to create proper installer with code signing (optional)

---

## 🔗 Next Steps

1. **Complete Phase 1-3 above**
2. **Run `npm start`** to test
3. **Test the break timer** by temporarily setting it to fire in 5 seconds
4. **Build the installer** with `npm run build-win`
5. **Distribute the .exe** to users!

---

## ❓ Questions?

If anything breaks:
- Check `main.js` console output (add `console.log()` statements)
- Verify `assets/icon.png` exists
- Ensure `preload.js` path is correct in `main.js`
- Look for errors in DevTools (Ctrl+I in app)

---

**You're ready! Let's migrate! 🚀**
