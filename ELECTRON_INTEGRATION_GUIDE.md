## 🔗 How to Integrate Electron IPC into Your index.html

Your `index.html` is already a fully functional Renderer process. You just need to:

1. **Replace the DOM modal with native notifications** when the break timer fires
2. **Listen for tray menu triggers** (optional)
3. **Handle graceful fallback** for web version

---

## Step 1: Modify `showBreakReminder()` in your `index.html`

**Find this function in your script section:**

```javascript
function showBreakReminder() {
  // OLD CODE - DOM-based modal
  const content = breakContent[lang] || breakContent["English"];
  const imageContainer = document.getElementById("break-media-container");
  imageContainer.innerHTML = `
    <img src="${content.imageUrl}" 
         class="w-full max-h-64 object-contain rounded mb-4" 
         alt="Stretch Guide" />
  `;
  // ... rest of DOM manipulation
}
```

**Replace with ELECTRON-AWARE code:**

```javascript
function showBreakReminder() {
  const content = breakContent[lang] || breakContent["English"];
  
  // ✅ ELECTRON: Use native OS notification if available
  if (window.electronAPI) {
    window.electronAPI.showNotification({
      title: t.break_msg || 'Break Time! 🏃',
      body: content.title || 'Time to stand up and stretch...',
      icon: 'assets/icon.png'  // Optional: path to icon within your assets folder
    });
    
    // OPTIONAL: Still show DOM modal on top for detailed instructions
    showBreakReminderModal(content);
    
  } else {
    // 🌐 WEB: Fall back to DOM modal for browser version
    showBreakReminderModal(content);
  }
}

// Extract the actual modal UI into a separate function
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
    <ul class="list-none p-0 m-0">
      ${actionsList}
    </ul>
    <p class="text-xs text-[var(--muted)] mt-3 italic">Take 2-3 minutes to perform this stretch.</p>
  `;
  
  document.getElementById("modal-break-reminder").classList.remove("hidden");
  isBreakModalOpen = true;
  playBeep(440, 0.3);
}
```

---

## Step 2: Optional – Listen for Tray Menu Triggers

If user clicks "Start Session" from the tray menu, listen for it:

```javascript
// Add this in your DOMContentLoaded or app initialization:
if (window.electronAPI) {
  window.electronAPI.onStartSession(() => {
    // Auto-start a session when user clicks tray menu
    onStart();
  });
  
  console.log('✅ Electron API bridged successfully');
  console.log('Platform:', window.electronAPI.getPlatform());
}
```

---

## Step 3: Image & Asset Management in Electron

### ✅ Your folder structure should be:

```
c:\Code S4 Romania\ergoguard 02\
├── main.js
├── preload.js
├── index.html
├── package.json
├── assets/
│   ├── icon.png          (512x512, app icon)
│   ├── icon.ico          (Windows only)
│   ├── icon.icns         (macOS only)
│   └── neck-stretch.jpg  (optional local image)
```

### ✅ Image URLs in your breakContent:

```javascript
// PRIMARY: Stick with Wikipedia (works everywhere in Electron with internet)
imageUrl: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Neck_stretch.jpg/640px-Neck_stretch.jpg",

// FALLBACK (optional): If you want a local image for offline mode:
imageUrl: new URL('assets/neck-stretch.jpg', window.location).href,
// OR simply:
imageUrl: "assets/neck-stretch.jpg",
```

### 🔧 Key differences from web version:

| Aspect | Web (HTTP Server) | Electron (file://) |
|--------|------|---------|
| Image path | `./assets/img.jpg` | `assets/img.jpg` (no leading dot) |
| Loading | Relative to server root | Relative to app root |
| Cache bust | Query params work | Not needed (isolated app) |
| External URLs | Need CORS | Work freely |

---

## Step 4: Cross-Platform Icon Setup

### For Windows (.ico):
```bash
# Using imagemagick (if installed) or online converter:
# Convert assets/icon.png → assets/icon.ico
# Recommended size: 256x256 source PNG
```

### For macOS (.icns):
```bash
# Use online converter or:
# npm install --save-dev icojs
# Or drag PNG into macOS "Image Capture" app
```

### For Linux (.png):
```bash
# Use assets/icon.png directly (256x256 minimum)
```

---

## Step 5: Test the Integration

### Run in development mode:
```bash
npm start
```

### Test checklist:
- [ ] App launches and loads `index.html`
- [ ] Click minimize → app hides to tray ✅
- [ ] Click tray icon → app reappears ✅
- [ ] Right-click tray → context menu appears ✅
- [ ] Break timer fires → native OS notification ✅
- [ ] Click notification → app comes to foreground ✅
- [ ] Click "Quit" → app exits cleanly ✅

---

## Step 6: Build the Installer

```bash
# Windows .exe installer
npm run build-win

# macOS .dmg
npm run build-mac

# Linux AppImage
npm run build-linux
```

Output will be in `./dist/` folder.

---

## Common Issues & Fixes

### ❌ "Cannot find module 'electron-reloader'"
```bash
npm install --save-dev electron-reloader
```

### ❌ Assets folder not included in build
Check `package.json` → `build.files` includes `"assets/**/*"` ✅

### ❌ Notification not showing on Windows
- Ensure `icon` path is valid
- Test with `urgency: 'critical'` in main.js (already set) ✅
- Check Windows Settings → Notifications & actions

### ❌ Tray icon not visible
- Create a 256x256 PNG icon
- Ensure `assets/icon.png` exists
- Restart app

---

## Ready? 

Run this in your terminal:

```bash
npm install
npm start
```

Your Electron app will launch! 🚀
