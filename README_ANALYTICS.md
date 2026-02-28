# ErgoGuard - Passive Posture Analytics Tool

## Overview
Your ErgoGuard project has been successfully transformed from an active posture corrector to a **Passive Posture Analytics Tool**. The tool now focuses on data logging and visualization instead of hardware control.

## What Changed?

### ✅ REMOVED
- **Brightness Control**: Completely removed `screen_brightness_control` library and all screen dimming functionality
- **Hardware Feedback**: No more automatic screen brightness changes
- **Active Correction**: Removed the "dimmed" state and correction prompts

### ✅ ADDED
1. **Data Logging System**
   - Records timestamp, inclination angle, and posture status for every frame
   - Tracks three states: "Good", "Bad", or "Absent"

2. **End-of-Session Report (Matplotlib)**
   - Generates a beautiful visual report when you press 'q' to quit
   - Line graph showing inclination angle over time
   - Color-coded background zones:
     - 🟢 **Green**: Good Posture periods
     - 🔴 **Red**: Bad Posture periods
     - ⚫ **Grey**: User Away/Not Detected

3. **Statistics & Gamification**
   - Calculates Total Focus Time (in hours)
   - Calculates Good Posture Percentage
   - **Achievement System**: Unlock "Spine Guardian (脊椎守護者)" title if Good Posture > 80%
   - Auto-saves chart as `Report_YYYY-MM-DD_HHMM.png`

### ✅ KEPT
- Real-time video feed with skeleton overlay
- Visual text feedback (colored text showing posture status)
- All three detection modes: MediaPipe Tasks, MediaPipe Solutions, OpenCV Fallback

## Installation

Update your dependencies:

```bash
pip install opencv-python mediapipe numpy matplotlib
```

Note: `screen-brightness-control` is no longer needed and has been removed.

## Usage

1. Run the program:
   ```bash
   python "ergoguard 02.py"
   ```

2. Sit in front of your camera and work normally
   - Green text = Good Posture ✅
   - Red text = Bad Posture ⚠️
   - Inclination angle displayed in real-time

3. Press 'q' to quit
   - A matplotlib window will open showing your session report
   - Report is automatically saved as PNG with timestamp

## Example Output

The report will show:
- **Title**: "Posture Analytics Report"
- **Stats**: "Focus Time: 2.34 hrs | Good Posture: 85.3%"
- **Achievement** (if applicable): "🏆 Title Unlocked: Spine Guardian (脊椎守護者)"
- **Graph**: Your inclination angle over time with color-coded posture zones

## Privacy

- All frames are processed in-memory only
- Posture data is logged temporarily for the session report
- No video recording or external data transmission
- Report files are saved locally only

## Next Steps

Try it out and monitor your posture passively! The analytics will help you understand your sitting patterns without intrusive feedback.
