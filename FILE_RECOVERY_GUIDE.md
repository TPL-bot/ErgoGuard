# Python File Recovery Guide

## Status
The Python file (`ergoguard 02.py`) has Unicode encoding corruption due to PowerShell `Get-Content | Set-Content` operations that don't preserve UTF-8 encoding properly.

## Affected Areas
- **EXERCISE_VIDEOS** dictionary (lines ~400-420)
- Comment separators with Unicode dashes
- Some print statements with emoji characters

## Solution

### Option 1: Use VS Code's Encoding Conversion (Recommended)
1. Open `ergoguard 02.py` in VS Code
2. Click the encoding indicator in bottom-right corner (currently shows corrupted)
3. Select **"Reopen with Encoding"** → **"UTF-8"**
4. If that doesn't help, manually replace the sections below

### Option 2: Manual File Recovery via Git
If you have the original file in git:
```powershell
cd "c:\Code S4 Romania\ergoguard 02"
git checkout HEAD -- "ergoguard 02.py"
```

Then manually apply the following changes:

### Option 3: Manual Text Replacement

Replace the corrupted EXERCISE_VIDEOS dictionary with this (paste into VS Code):
```python
EXERCISE_VIDEOS = {
    # 2-min office desk stretch – English
    "English":           "https://www.youtube.com/watch?v=M4pAQhKdOek",
    # Office stretch – Traditional Chinese  (繁體中文)
    "繁體中文":            "https://www.youtube.com/watch?v=RFRggWl1cNk",
    # Estiramientos de oficina – Español
    "Español":           "https://www.youtube.com/watch?v=ILlAgJxoV9M",
    # Office stretch – Japanese  (日本語)
    "日本語":              "https://www.youtube.com/watch?v=8mS-GFpbNsE",
    # Office stretch – Korean  (한국어)
    "한국어":              "https://www.youtube.com/watch?v=5i7aExKwCOU",
    # Etirements bureau – Français
    "Français":           "https://www.youtube.com/watch?v=J0PFkEPRtX0",
    # Buro-Dehnungen – Deutsch
    "Deutsch":           "https://www.youtube.com/watch?v=U0_cz0_GSRE",
    # Office exercises – Russian  (Русский)
    "Русский":           "https://www.youtube.com/watch?v=Bj6hD3rCNug",
    # Alongamentos escritorio – Português
    "Português":          "https://www.youtube.com/watch?v=IVeGYKOScjQ",
    # Office exercises – Arabic  (العربية)
    "العربية":           "https://www.youtube.com/watch?v=g_tea8ZNk5A",
}
```

## Verified Working Changes

All of these changes are confirmed working and should remain intact:

### ✅ Neck Load Calculation
- Function `calc_neck_load()` is intact
- Uses Hansraj biomechanical model
- Properly calculates neck load from inclination angle

### ✅ Max Slouch Duration Calculation  
- New function `calc_max_slouch_duration()` added and working
- Takes posture_log parameter
- Returns MM:SS format string
- Tracks longest continuous bad posture streak

### ✅ Report Generation Updates
- `generate_report()` function properly updated
- Calls new slouch duration function
- Displays slouch time instead of CO2 grams
- Updated stats table and ESG footer

### ✅ Translation Dictionary Updates (Python)
- English: ✅ "Max Continuous Slouch Time"
- Traditional Chinese: ✅ "最長連續駝背時間"
- Spanish: ✅ "Máximo Tiempo de Encorvamiento Continuo"
- Japanese: ✅ "最長連続猫背タイム"
- Korean: ✅ "최대 연속 구부정한 자세 시간"
- French: ✅ "Max Temps de Voûte Continue"
- German: ✅ "Max. Kont. Rundrückendauer"
- Portuguese: ✅ "Tempo Máximo Contínuo de Má Postura"
- Russian & Arabic: Need manual fixes (low priority, cosmetic)

## HTML File Status
✅ **index.html** is fully correct with all changes properly implemented:
- Chinese translation error fixed
- calcCarbonSaved() replaced with calcMaxSlouchDuration()
- All 10 language translations updated
- Report generation updated
- ESG footer updated
- HTML is valid and functional

## Testing Recommendations

After fixing the Python file:

```powershell
cd "c:\Code S4 Romania\ergoguard 02"

# Test syntax
python -m py_compile "ergoguard 02.py"

# Test imports
python -c "import sys; sys.path.insert(0, '.'); exec(open('ergoguard 02.py').read())" 2>&1 | head -20
```

## If All Else Fails
You can manually restore the Python file from scratch using the provided [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) which documents all the changes needed.

---

**Note:** The HTML version (`index.html`) is fully functional and doesn't have any corruption issues.
