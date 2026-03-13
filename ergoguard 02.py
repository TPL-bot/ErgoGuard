"""
?��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��?
??             ErgoGuard International  ?? Competition Edition                ??
?? Privacy-First  ·  AI Posture Analytics  ·  ESG Reporting  ·  Multilingual  ??
?��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��??��?

Requirements:
    pip install opencv-python mediapipe numpy matplotlib screen-brightness-control

Usage:
    python "ergoguard 02.py"

Architecture:
    1. Tkinter Launcher  ??language / interval / privacy settings
    2. OpenCV Loop       ??real-time pose detection (MediaPipe)
    3. Privacy Stickman  ??black canvas + skeleton only (no raw feed)
    4. Reminder System   ??timed break with context-aware YouTube video
    5. Matplotlib Report ??donut chart, health grade, ESG footer
"""

# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  IMPORTS  (all graceful)
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
import time
import math
import sys
import os
import threading
import webbrowser
from datetime import datetime

try:
    import cv2
    CV2_OK = True
except ImportError:
    print("[ERROR] opencv-python not found. Run: pip install opencv-python")
    sys.exit(1)

try:
    import numpy as np
    NP_OK = True
except ImportError:
    print("[ERROR] numpy not found. Run: pip install numpy")
    sys.exit(1)

try:
    import mediapipe as mp
    MP_OK = True
except ImportError:
    MP_OK = False
    print("[WARN] mediapipe not found. Skeleton mode disabled. Run: pip install mediapipe")

try:
    import matplotlib
    matplotlib.use("Agg")          # non-interactive backend ??avoids Tk conflicts
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MPL_OK = True
except ImportError:
    MPL_OK = False

try:
    from plyer import notification as _plyer_notify # type: ignore
    PLYER_OK = True
except ImportError:  # graceful fallback ??toast becomes a print statement
    _plyer_notify = None
    PLYER_OK = False
    print("[WARN] matplotlib not found. Reports disabled.")

try:
    import tkinter as tk
    from tkinter import ttk, font as tkfont
    TK_OK = True
except ImportError:
    TK_OK = False
    print("[WARN] tkinter unavailable ??using CLI defaults.")

try:
    import screen_brightness_control as sbc
    SBC_OK = True
except ImportError:
    SBC_OK = False   # optional; ESG calc still runs without it


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  TRANSLATIONS  (Top-10 global languages)  ?? keys are native-script display names
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
TRANSLATIONS = {
    "English": {
        "title":         "ErgoGuard International",
        "subtitle":      "AI Posture & Wellness Guardian",
        "language":      "Language",
        "interval":      "Reminder Interval (minutes)",
        "privacy":       "Privacy Mode  (Stickman Only ??No Camera Feed)",
        "start":         "Start ErgoGuard",
        "good":          "Good Posture  [OK]",
        "bad":           "Bad Posture   [!!]",
        "absent":        "No Person Detected",
        "partial":       "Partial Detection",
        "angle":         "Neck Angle",
        "neck_load":     "Neck Load",
        "break_msg":     "BREAK TIME!  Opening your stretch video...",
        "privacy_label": "PRIVACY MODE ON -- Stickman Only",
        "quit_tip":      "Press  Q  to quit & generate report",
        "report_title":  "ErgoGuard Session Report",
        "grade_label":   "Health Grade",
        "carbon_label":  "Max Continuous Slouch Time",
        "neck_avg":      "Avg Neck Load",
        "good_label":    "Good Posture",
        "bad_label":     "Bad Posture",
        "grade_A_msg":   "Excellent!  Keep it up.",
        "grade_B_msg":   "Average.  Try to sit straight more often to protect your spine.",
        "grade_F_msg":   "Danger!  Bad posture for most of your session.  Please stretch now!",
        "session_time":  "Session Time",
        "frames":        "Frames",
        "good_pct_label":"Good Posture %",
        "session_stats": "Session Statistics",
    },
    "\u7e41\u9ad4\u4e2d\u6587": {
        "title":         "ErgoGuard \u570b\u969b\u7248",
        "subtitle":      "AI \u59ff\u52e2\u8207\u5065\u5eb7\u5b88\u8b77\u8005",
        "language":      "\u8a9e\u8a00",
        "interval":      "\u63d0\u9192\u9593\u9694\uff08\u5206\u9418\uff09",
        "privacy":       "\u96b1\u79c1\u6a21\u5f0f\uff08\u50c5\u986f\u793a\u706b\u67f4\u4eba\u9aa8\u67b6\uff09",
        "start":         "\u555f\u52d5 ErgoGuard",
        "good":          "\u59ff\u52e2\u826f\u597d [OK]",
        "bad":           "\u59ff\u52e2\u4e0d\u826f [!!]",
        "absent":        "\u672a\u5075\u6e2c\u5230\u4eba\u54e1",
        "partial":       "\u90e8\u5206\u5075\u6e2c",
        "angle":         "\u9838\u90e8\u89d2\u5ea6",
        "neck_load":     "\u9838\u90e8\u8ca0\u8377",
        "break_msg":     "\u4f11\u606f\u6642\u9593\uff01\u6b63\u5728\u958b\u555f\u4f38\u5c55\u5f71\u7247...",
        "privacy_label": "\u96b1\u79c1\u6a21\u5f0f\u5df2\u958b\u555f -- \u50c5\u986f\u793a\u9aa8\u67b6",
        "quit_tip":      "\u6309  Q  \u9000\u51fa\u4e26\u751f\u6210\u5831\u544a",
        "report_title":  "ErgoGuard \u5de5\u4f5c\u968e\u6bb5\u5831\u544a",
        "grade_label":   "\u5065\u5eb7\u8a55\u7d1a",
        "carbon_label":  "\u6700\u9577\u9023\u7e8c\u99dd\u80cc\u6642\u9593",
        "neck_avg":      "\u5e73\u5747\u9838\u90e8\u8ca0\u8377",
        "good_label":    "\u826f\u597d\u59ff\u52e2",
        "bad_label":     "\u4e0d\u826f\u59ff\u52e2",
        "grade_A_msg":   "\u512a\u79c0\uff01\u7e7c\u7e8c\u4fdd\u6301\u3002",
        "grade_B_msg":   "\u4e00\u822c\u3002\u8acb\u66f4\u5e38\u4fdd\u6301\u631a\u76f4\u5750\u59ff\u4ee5\u4fdd\u8b77\u810a\u690e\u3002",
        "grade_F_msg":   "\u5371\u96aa\uff01\u60a8\u5927\u90e8\u5206\u6642\u9593\u59ff\u52e2\u4e0d\u826f\uff0c\u8acb\u7acb\u5373\u4f38\u5c55\uff01",
        "session_time":  "\u5de5\u4f5c\u968e\u6bb5\u6642\u9593",
        "frames":        "\u5e40\u6578",
        "good_pct_label":"\u826f\u597d\u59ff\u52e2 %",
        "session_stats": "\u5de5\u4f5c\u968e\u6bb5\u7d71\u8a08",
    },
    "Espa\u00f1ol": {
        "title":         "ErgoGuard Internacional",
        "subtitle":      "Guardian de Postura y Bienestar con IA",
        "language":      "Idioma",
        "interval":      "Intervalo de Recordatorio (minutos)",
        "privacy":       "Modo Privacidad  (Solo Contorno)",
        "start":         "Iniciar ErgoGuard",
        "good":          "Buena Postura [OK]",
        "bad":           "Mala Postura  [!!]",
        "absent":        "Persona No Detectada",
        "partial":       "Deteccion Parcial",
        "angle":         "Angulo de Cuello",
        "neck_load":     "Carga del Cuello",
        "break_msg":     "HORA DE DESCANSO!  Abriendo video de estiramiento...",
        "privacy_label": "MODO PRIVACIDAD -- Solo Contorno",
        "quit_tip":      "Presiona  Q  para salir y generar reporte",
        "report_title":  "Reporte de Sesion ErgoGuard",
        "grade_label":   "Calificacion de Salud",
        "carbon_label":  "Máximo Tiempo de Encorvamiento Continuo",
        "neck_avg":      "Carga Promedio del Cuello",
        "good_label":    "Buena Postura",
        "bad_label":     "Mala Postura",
        "grade_A_msg":   "\u00a1Excelente!  \u00a1Sigue as\u00ed!",
        "grade_B_msg":   "Regular.  Intenta sentarte m\u00e1s recto para proteger tu columna vertebral.",
        "grade_F_msg":   "\u00a1Peligro!  Mala postura la mayor parte del tiempo.  \u00a1Est\u00edrate ahora!",
        "session_time":  "Tiempo de Sesi\u00f3n",
        "frames":        "Fotogramas",
        "good_pct_label":"% Buena Postura",
        "session_stats": "Estad\u00edsticas de Sesi\u00f3n",
    },
    "\u65e5\u672c\u8a9e": {
        "title":         "ErgoGuard \u30a4\u30f3\u30bf\u30fc\u30ca\u30b7\u30e7\u30ca\u30eb",
        "subtitle":      "AI \u59ff\u52e2\u30fb\u5065\u5eb7\u30ac\u30fc\u30c7\u30a3\u30a2\u30f3",
        "language":      "\u8a00\u8a9e",
        "interval":      "\u30ea\u30de\u30a4\u30f3\u30c0\u30fc\u9593\u9694\uff08\u5206\uff09",
        "privacy":       "\u30d7\u30e9\u30a4\u30d0\u30b7\u30fc\u30e2\u30fc\u30c9\uff08\u30b9\u30b1\u30eb\u30c8\u30f3\u8868\u793a\u306e\u307f\uff09",
        "start":         "ErgoGuard \u3092\u958b\u59cb",
        "good":          "\u59ff\u52e2\u826f\u597d [OK]",
        "bad":           "\u59ff\u52e2\u4e0d\u826f [!!]",
        "absent":        "\u4eba\u7269\u672a\u691c\u51fa",
        "partial":       "\u90e8\u5206\u691c\u51fa",
        "angle":         "\u9996\u306e\u89d2\u5ea6",
        "neck_load":     "\u9996\u306e\u8ca0\u8377",
        "break_msg":     "\u4f11\u686c\u6642\u9593\uff01 \u30b9\u30c8\u30ec\u30c3\u30c1\u52d5\u753b\u3092\u958b\u3044\u3066\u3044\u307e\u3059...",
        "privacy_label": "\u30d7\u30e9\u30a4\u30d0\u30b7\u30fc\u30e2\u30fc\u30c9 ON -- \u30b9\u30b1\u30eb\u30c8\u30f3\u306e\u307f",
        "quit_tip":      "Q \u3092\u62bc\u3057\u3066\u7d42\u4e86\u30fb\u30ec\u30dd\u30fc\u30c8\u751f\u6210",
        "report_title":  "ErgoGuard \u30bb\u30c3\u30b7\u30e7\u30f3\u30ec\u30dd\u30fc\u30c8",
        "grade_label":   "\u5065\u5eb7\u8a55\u4fa1",
        "carbon_label":  "\u6700\u9577\u9023\u7d9a\u732b\u80cc\u30bf\u30a4\u30e0",
        "neck_avg":      "\u5e73\u5747\u9996\u8ca0\u8377",
        "good_label":    "\u826f\u3044\u59ff\u52e2",
        "bad_label":     "\u60aa\u3044\u59ff\u52e2",
        "grade_A_msg":   "\u7d20\u6674\u3089\u3057\u3044\uff01\u3053\u306e\u8abf\u5b50\u3067\u7d9a\u3051\u3066\u304f\u3060\u3055\u3044\u3002",
        "grade_B_msg":   "\u666e\u901a\u3002\u810a\u690e\u3092\u5b88\u308b\u305f\u3081\u3001\u3082\u3063\u3068\u771f\u3063\u76f4\u3050\u5ea7\u308b\u3088\u3046\u5fc3\u304c\u3051\u307e\u3057\u3087\u3046\u3002",
        "grade_F_msg":   "\u5371\u967a\uff01\u30bb\u30c3\u30b7\u30e7\u30f3\u306e\u307b\u3068\u3093\u3069\u3067\u59ff\u52e2\u304c\u60aa\u304b\u3063\u305f\u3067\u3059\u3002\u4eca\u3059\u3050\u30b9\u30c8\u30ec\u30c3\u30c1\u3057\u3066\u304f\u3060\u3055\u3044\uff01",
        "session_time":  "\u30bb\u30c3\u30b7\u30e7\u30f3\u6642\u9593",
        "frames":        "\u30d5\u30ec\u30fc\u30e0\u6570",
        "good_pct_label":"\u826f\u3044\u59ff\u52e2 %",
        "session_stats": "\u30bb\u30c3\u30b7\u30e7\u30f3\u7d71\u8a08",
    },
    "\ud55c\uad6d\uc5b4": {
        "title":         "ErgoGuard \uc778\ud130\ub0b4\uc154\ub110",
        "subtitle":      "AI \uc790\uc138 & \uac74\uac15 \uc218\ud638\uc790",
        "language":      "\uc5b8\uc5b4",
        "interval":      "\uc54c\ub9bc \uac04\uaca9 (\ubd84)",
        "privacy":       "\ud504\ub77c\uc774\ubc84\uc2dc \ubaa8\ub4dc  (\uc724\uacfd\uc120\ub9cc \ud45c\uc2dc)",
        "start":         "ErgoGuard \uc2dc\uc791",
        "good":          "\uc88b\uc740 \uc790\uc138 [OK]",
        "bad":           "\ub098\uc05c \uc790\uc138 [!!]",
        "absent":        "\uc0ac\ub78c \ubbf8\uac10\uc9c0",
        "partial":       "\ubd80\ubd84 \uac10\uc9c0",
        "angle":         "\ubaa9 \uac01\ub3c4",
        "neck_load":     "\ubaa9 \ubd80\ud558",
        "break_msg":     "\ud734\uc2dd \uc2dc\uac04!  \uc2a4\ud2b8\ub808\uce6d \uc601\uc0c1\uc744 \uc5f4\uace0 \uc788\uc2b5\ub2c8\ub2e4...",
        "privacy_label": "\ud504\ub77c\uc774\ubc84\uc2dc \ubaa8\ub4dc \ucf1c\uc9d0 -- \uc724\uacfd\uc120\ub9cc",
        "quit_tip":      "Q \ub97c \ub208\ub7ec \uc885\ub8cc \ubc0f \ubcf4\uace0\uc11c \uc0dd\uc131",
        "report_title":  "ErgoGuard \uc138\uc158 \ubcf4\uace0\uc11c",
        "grade_label":   "\uac74\uac15 \ub4f1\uae09",
        "carbon_label":  "\ucd5c\ub300 \uc5f0\uc18d \uad6c\ubd80\uc815\ud55c \uc790\uc138 \uc2dc\uac04",
        "neck_avg":      "\ud3c9\uade0 \ubaa9 \ubd80\ud558",
        "good_label":    "\uc88b\uc740 \uc790\uc138",
        "bad_label":     "\ub098\uc05c \uc790\uc138",
        "grade_A_msg":   "\ud6c4\ub96d\ud569\ub2c8\ub2e4!  \uacc4\uc18d \uc720\uc9c0\ud558\uc138\uc694.",
        "grade_B_msg":   "\ubcf4\ud1b5\uc785\ub2c8\ub2e4.  \ucb99\ucd94 \ubcf4\ud638\ub97c \uc704\ud574 \ub354 \uc790\uc8fc \ubc14\ub974\uac8c \uc549\uc73c\uc138\uc694.",
        "grade_F_msg":   "\uc704\ud5d8!  \ub300\ubd80\ubd84\uc758 \uc2dc\uac04 \ub3d9\uc548 \ub098\uc05c \uc790\uc138\uc600\uc2b5\ub2c8\ub2e4.  \uc9c0\uae08 \ubc14\ub85c \uc2a4\ud2b8\ub808\uce6d\ud558\uc138\uc694!",
        "session_time":  "\uc138\uc158 \uc2dc\uac04",
        "frames":        "\ud504\ub808\uc784 \uc218",
        "good_pct_label":"\uc880\uc740 \uc790\uc138 %",
        "session_stats": "\uc138\uc158 \ud1b5\uacc4",
    },
    "Fran\u00e7ais": {
        "title":         "ErgoGuard International",
        "subtitle":      "Gardien de Posture & Bien-etre par IA",
        "language":      "Langue",
        "interval":      "Intervalle de Rappel (minutes)",
        "privacy":       "Mode Confidentialite  (Squelette Seulement)",
        "start":         "Demarrer ErgoGuard",
        "good":          "Bonne Posture [OK]",
        "bad":           "Mauvaise Posture [!!]",
        "absent":        "Aucune Personne Detectee",
        "partial":       "Detection Partielle",
        "angle":         "Angle du Cou",
        "neck_load":     "Charge du Cou",
        "break_msg":     "PAUSE!  Ouverture de la video d'etirement...",
        "privacy_label": "MODE CONFIDENTIALITE -- Squelette Seulement",
        "quit_tip":      "Appuyez sur  Q  pour quitter et generer le rapport",
        "report_title":  "Rapport de Session ErgoGuard",
        "grade_label":   "Note de Sante",
        "carbon_label":  "Max Temps de Voûte Continue",
        "neck_avg":      "Charge Moyenne du Cou",
        "good_label":    "Bonne Posture",
        "bad_label":     "Mauvaise Posture",
        "grade_A_msg":   "Excellent !  Continuez ainsi.",
        "grade_B_msg":   "Moyen.  Essayez de vous asseoir plus droit pour prot\u00e9ger votre colonne vert\u00e9brale.",
        "grade_F_msg":   "Danger !  Mauvaise posture la plupart du temps.  \u00c9tirez-vous maintenant !",
        "session_time":  "Dur\u00e9e de Session",
        "frames":        "Images",
        "good_pct_label":"% Bonne Posture",
        "session_stats": "Statistiques de Session",
    },
    "Deutsch": {
        "title":         "ErgoGuard International",
        "subtitle":      "KI-Haltungs- & Gesundheitswaechter",
        "language":      "Sprache",
        "interval":      "Erinnerungsintervall (Minuten)",
        "privacy":       "Datenschutzmodus  (Nur Skelett)",
        "start":         "ErgoGuard Starten",
        "good":          "Gute Haltung [OK]",
        "bad":           "Schlechte Haltung [!!]",
        "absent":        "Keine Person Erkannt",
        "partial":       "Teilweise Erkennung",
        "angle":         "Nackenwinkel",
        "neck_load":     "Nackenlast",
        "break_msg":     "PAUSE!  Dehnvideo wird geoffnet...",
        "privacy_label": "DATENSCHUTZMODUS EIN -- Nur Skelett",
        "quit_tip":      "Druecke  Q  zum Beenden & Bericht erstellen",
        "report_title":  "ErgoGuard Sitzungsbericht",
        "grade_label":   "Gesundheitsnote",
        "carbon_label":  "Max. Kont. Rundrückendauer",
        "neck_avg":      "Durchschnittliche Nackenlast",
        "good_label":    "Gute Haltung",
        "bad_label":     "Schlechte Haltung",
        "grade_A_msg":   "Ausgezeichnet!  Weiter so.",
        "grade_B_msg":   "Durchschnittlich.  Versuche \u00f6fter gerade zu sitzen, um deine Wirbels\u00e4ule zu sch\u00fctzen.",
        "grade_F_msg":   "Gefahr!  Die meiste Zeit schlechte Haltung.  Bitte jetzt dehnen!",
        "session_time":  "Sitzungsdauer",
        "frames":        "Bilder",
        "good_pct_label":"Gute Haltung %",
        "session_stats": "Sitzungsstatistiken",
    },
    "\u0420\u0443\u0441\u0441\u043a\u0438\u0439": {
        "title":         "ErgoGuard International",
        "subtitle":      "II-strazh osanki i zdorov'ya",
        "language":      "\u042f\u0437\u044b\u043a",
        "interval":      "\u0418\u043d\u0442\u0435\u0440\u0432\u0430\u043b \u043d\u0430\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u044f (\u043c\u0438\u043d.)",
        "privacy":       "\u0420\u0435\u0436\u0438\u043c \u043a\u043e\u043d\u0444\u0438\u0434\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u0438  (\u0422\u043e\u043b\u044c\u043a\u043e \u0441\u043a\u0435\u043b\u0435\u0442)",
        "start":         "\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c ErgoGuard",
        "good":          "\u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u0430\u044f \u043e\u0441\u0430\u043d\u043a\u0430 [OK]",
        "bad":           "\u041d\u0435\u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u0430\u044f \u043e\u0441\u0430\u043d\u043a\u0430 [!!]",
        "absent":        "\u0427\u0435\u043b\u043e\u0432\u0435\u043a \u043d\u0435 \u043e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d",
        "partial":       "\u0427\u0430\u0441\u0442\u0438\u0447\u043d\u043e\u0435 \u043e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u0438\u0435",
        "angle":         "\u0423\u0433\u043e\u043b \u0448\u0435\u0438",
        "neck_load":     "\u041d\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u043d\u0430 \u0448\u0435\u044e",
        "break_msg":     "\u0412\u0420\u0415\u041c\u042f \u041f\u0415\u0420\u0415\u0420\u042b\u0412\u0410!  \u041e\u0442\u043a\u0440\u044b\u0432\u0430\u044e \u0432\u0438\u0434\u0435\u043e...",
        "privacy_label": "\u0420\u0415\u0416\u0418\u041c \u041a\u041e\u041d\u0424. \u0412\u041a\u041b -- \u0422\u043e\u043b\u044c\u043a\u043e \u0441\u043a\u0435\u043b\u0435\u0442",
        "quit_tip":      "\u041d\u0430\u0436\u043c\u0438\u0442\u0435  Q  \u0434\u043b\u044f \u0432\u044b\u0445\u043e\u0434\u0430 \u0438 \u043e\u0442\u0447\u0451\u0442\u0430",
        "report_title":  "\u041e\u0442\u0447\u0451\u0442 \u0441\u0435\u0441\u0441\u0438\u0438 ErgoGuard",
        "grade_label":   "\u041e\u0446\u0435\u043d\u043a\u0430 \u0437\u0434\u043e\u0440\u043e\u0432\u044c\u044f",
        "carbon_label":  "\u0421\u044d\u043a\u043e\u043d\u043e\u043c\u043b\u0435\u043d\u043e CO2 (ESG)",
        "neck_avg":      "\u0421\u0440\u0435\u0434\u043d\u044f\u044f \u043d\u0430\u0433\u0440\u0443\u0437\u043a\u0430 \u043d\u0430 \u0448\u0435\u044e",
        "good_label":    "\u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u0430\u044f \u043e\u0441\u0430\u043d\u043a\u0430",
        "bad_label":     "\u041d\u0435\u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u0430\u044f \u043e\u0441\u0430\u043d\u043a\u0430",
        "grade_A_msg":   "\u041e\u0442\u043b\u0438\u0447\u043d\u043e!  \u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0430\u0439\u0442\u0435 \u0432 \u0442\u043e\u043c \u0436\u0435 \u0434\u0443\u0445\u0435.",
        "grade_B_msg":   "\u0421\u0440\u0435\u0434\u043d\u0435.  \u0421\u0442\u0430\u0440\u0430\u0439\u0442\u0435\u0441\u044c \u0447\u0430\u0449\u0435 \u0441\u0438\u0434\u0435\u0442\u044c \u043f\u0440\u044f\u043c\u043e, \u0447\u0442\u043e\u0431\u044b \u0437\u0430\u0449\u0438\u0442\u0438\u0442\u044c \u043f\u043e\u0437\u0432\u043e\u043d\u043e\u0447\u043d\u0438\u043a.",
        "grade_F_msg":   "\u041e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u044c!  \u0411\u043e\u043b\u044c\u0448\u0443\u044e \u0447\u0430\u0441\u0442\u044c \u0441\u0435\u0441\u0441\u0438\u0438 \u043f\u043b\u043e\u0445\u0430\u044f \u043e\u0441\u0430\u043d\u043a\u0430.  \u0421\u0440\u043e\u0447\u043d\u043e \u0440\u0430\u0437\u043e\u043c\u043d\u0438\u0442\u0435\u0441\u044c!",
        "session_time":  "\u0412\u0440\u0435\u043c\u044f \u0441\u0435\u0441\u0441\u0438\u0438",
        "frames":        "\u041a\u0430\u0434\u0440\u043e\u0432",
        "good_pct_label":"\u0425\u043e\u0440\u043e\u0448\u0430\u044f \u043e\u0441\u0430\u043d\u043a\u0430 %",
        "session_stats": "\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430 \u0441\u0435\u0441\u0441\u0438\u0438",
    },
    "Portugu\u00eas": {
        "title":         "ErgoGuard Internacional",
        "subtitle":      "Guardiao de Postura e Bem-Estar com IA",
        "language":      "Idioma",
        "interval":      "Intervalo de Lembrete (minutos)",
        "privacy":       "Modo Privacidade  (Apenas Contorno)",
        "start":         "Iniciar ErgoGuard",
        "good":          "Boa Postura [OK]",
        "bad":           "Ma Postura  [!!]",
        "absent":        "Nenhuma Pessoa Detectada",
        "partial":       "Deteccao Parcial",
        "angle":         "Angulo do Pescoco",
        "neck_load":     "Carga do Pescoco",
        "break_msg":     "HORA DO INTERVALO!  Abrindo video de alongamento...",
        "privacy_label": "MODO PRIVACIDADE -- Apenas Contorno",
        "quit_tip":      "Pressione  Q  para sair e gerar relatorio",
        "report_title":  "Relatorio de Sessao ErgoGuard",
        "grade_label":   "Nota de Saude",
        "carbon_label":  "Tempo Máximo Contínuo de Má Postura",
        "neck_avg":      "Carga Média do Pescoço",
        "good_label":    "Boa Postura",
        "bad_label":     "Ma Postura",
        "grade_A_msg":   "Excelente!  Continue assim.",
        "grade_B_msg":   "M\u00e9dio.  Tente sentar mais ereto para proteger sua coluna vertebral.",
        "grade_F_msg":   "Perigo!  M\u00e1 postura na maior parte da sess\u00e3o.  Alongue-se agora!",
        "session_time":  "Tempo de Sess\u00e3o",
        "frames":        "Quadros",
        "good_pct_label":"% Boa Postura",
        "session_stats": "Estat\u00edsticas de Sess\u00e3o",
    },
    "\u0627\u0644\u0639\u0631\u0628\u064a\u0629": {
        "title":         "ErgoGuard International",
        "subtitle":      "AI Posture Guardian",
        "language":      "\u0627\u0644\u0644\u063a\u0629",
        "interval":      "\u0641\u062a\u0631\u0629 \u0627\u0644\u062a\u0630\u0643\u064a\u0631 (\u062f\u0642\u064a\u0642\u0629)",
        "privacy":       "\u0648\u0636\u0639 \u0627\u0644\u062e\u0635\u0648\u0635\u064a\u0629  (\u0647\u064a\u0643\u0644 \u0639\u0638\u0645\u064a \u0641\u0642\u0637)",
        "start":         "\u062a\u0634\u063a\u064a\u0644 ErgoGuard",
        "good":          "\u0648\u0636\u0639\u064a\u0629 \u062c\u064a\u062f\u0629 [OK]",
        "bad":           "\u0648\u0636\u0639\u064a\u0629 \u0633\u064a\u0626\u0629 [!!]",
        "absent":        "\u0644\u0645 \u064a\u062a\u0645 \u0627\u0643\u062a\u0634\u0627\u0641 \u0623\u064a \u0634\u062e\u0635",
        "partial":       "\u0627\u0643\u062a\u0634\u0627\u0641 \u062c\u0632\u0626\u064a",
        "angle":         "\u0632\u0627\u0648\u064a\u0629 \u0627\u0644\u0631\u0642\u0628\u0629",
        "neck_load":     "\u062d\u0645\u0644 \u0627\u0644\u0631\u0642\u0628\u0629",
        "break_msg":     "\u062d\u0627\u0646 \u0648\u0642\u062a \u0627\u0644\u0627\u0633\u062a\u0631\u0627\u062d\u0629!  \u062c\u0627\u0631\u064d \u0641\u062a\u062d \u0641\u064a\u062f\u064a\u0648 \u0627\u0644\u062a\u0645\u062f\u062f...",
        "privacy_label": "Privacy Mode ON -- Skeleton Only",
        "quit_tip":      "\u0627\u0636\u063a\u0637  Q  \u0644\u0644\u062e\u0631\u0648\u062c \u0648\u0625\u0646\u0634\u0627\u0621 \u0627\u0644\u062a\u0642\u0631\u064a\u0631",
        "report_title":  "\u062a\u0642\u0631\u064a\u0631 \u062c\u0644\u0633\u0629 ErgoGuard",
        "grade_label":   "\u062a\u0642\u064a\u064a\u0645 \u0627\u0644\u0635\u062d\u0629",
        "carbon_label":  "\u0627\u0644\u0643\u0631\u0628\u0648\u0646 \u0627\u0644\u0645\u0648\u0641\u064e\u0651\u0631 (ESG)",
        "neck_avg":      "\u0645\u062a\u0648\u0633\u0637 \u062d\u0645\u0644 \u0627\u0644\u0631\u0642\u0628\u0629",
        "good_label":    "\u0648\u0636\u0639\u064a\u0629 \u062c\u064a\u062f\u0629",
        "bad_label":     "\u0648\u0636\u0639\u064a\u0629 \u0633\u064a\u0626\u0629",
        "grade_A_msg":   "\u0645\u0645\u062a\u0627\u0632!  \u0627\u0633\u062a\u0645\u0631 \u0641\u064a \u0630\u0644\u0643.",
        "grade_B_msg":   "\u0645\u062a\u0648\u0633\u0637.  \u062d\u0627\u0648\u0644 \u0627\u0644\u062c\u0644\u0648\u0633 \u0628\u0627\u0633\u062a\u0642\u0627\u0645\u0629 \u0623\u0643\u062b\u0631 \u0644\u062d\u0645\u0627\u064a\u0629 \u0639\u0645\u0648\u062f\u0643 \u0627\u0644\u0641\u0642\u0631\u064a.",
        "grade_F_msg":   "\u062e\u0637\u0631!  \u0648\u0636\u0639\u064a\u062a\u0643 \u0633\u064a\u0626\u0629 \u0645\u0639\u0638\u0645 \u0627\u0644\u062c\u0644\u0633\u0629.  \u062a\u0645\u062f\u062f \u0627\u0644\u0622\u0646!",
        "session_time":  "\u0648\u0642\u062a \u0627\u0644\u062c\u0644\u0633\u0629",
        "frames":        "\u0627\u0644\u0625\u0637\u0627\u0631\u0627\u062a",
        "good_pct_label":"% \u0648\u0636\u0639\u064a\u0629 \u062c\u064a\u062f\u0629",
        "session_stats": "\u0625\u062d\u0635\u0627\u0626\u064a\u0627\u062a \u0627\u0644\u062c\u0644\u0633\u0629",
    },
}

LANGUAGE_LIST = list(TRANSLATIONS.keys())

# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  CONTEXT-AWARE EXERCISE VIDEOS  (one per language)
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
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


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  DAILY  REMINDERS  ?? global in-memory store  (persists for the full session)
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
# Each entry is a dict: {"name": str, "hour": int, "minute": int,
#                        "category": str, "done": bool}
DAILY_REMINDERS: list = []


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  BIOMECHANICAL  &  ESG  UTILITIES
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
def calc_neck_load(inclination_angle_deg: float) -> float:
    """
    Estimate effective neck load (kg) using the simplified Hansraj model.

    inclination_angle_deg:  angle between head-shoulder and shoulder-hip
                            vectors (180 deg = perfectly upright).

    Published reference loads (Hansraj, 2014):
        0 deg forward  ?? 4.5 kg
       15 deg forward  ?? 12  kg
       30 deg forward  ?? 18  kg
       45 deg forward  ?? 22  kg
       60 deg forward  ?? 27  kg
    """
    forward_deg = max(0.0, 180.0 - inclination_angle_deg)
    forward_rad = math.radians(min(forward_deg, 90.0))
    neck_load   = 4.5 + 27.5 * (math.sin(forward_rad) ** 1.2)
    return round(neck_load, 1)


def calc_max_slouch_duration(posture_log: list) -> str:
    """
    Find the longest continuous duration of bad posture.
    
    Returns MM:SS format string.
    
    Args:
        posture_log: List of (timestamp, angle, status) tuples
    
    Returns:
        String in "MM:SS" format
    """
    max_durations = []
    current_bad_start = None
    
    for i, entry in enumerate(posture_log):
        status = entry[2] if len(entry) > 2 else "Good"
        if status == "Bad":
            if current_bad_start is None:
                current_bad_start = i
        else:
            if current_bad_start is not None:
                max_durations.append(i - current_bad_start)
                current_bad_start = None
    
    # Include the last streak if session ended during slouch
    if current_bad_start is not None:
        max_durations.append(len(posture_log) - current_bad_start)
    
    max_frames = max(max_durations, default=0)
    # Assume ~30 FPS framerate
    frame_rate = 30
    seconds = round(max_frames / frame_rate)
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"


def health_grade(good_pct: float) -> str:
    """Lenient 3-level health grade  (A / B / F).

    A  ??good_pct >= 60%   Excellent posture
    B  ??good_pct >= 25%   Average / needs improvement
    F  ??good_pct  < 25%   Dangerous; mostly bad posture
    """
    if   good_pct >= 60: return "A"
    elif good_pct >= 25: return "B"
    else:                return "F"


GRADE_COLOR = {
    "A": "#2ECC71",   # green
    "B": "#F39C12",   # amber
    "F": "#E74C3C",   # red
}


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  MEDIAPIPE  INITIALISATION  (robust for all install variants)
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
def init_mediapipe():
    """Return (mp_drawing, mp_pose) or (None, None) when unavailable."""
    if not MP_OK:
        return None, None
    import importlib
    for candidate in ("mediapipe.solutions", "mediapipe.python.solutions"):
        try:
            sol = importlib.import_module(candidate)
            return sol.drawing_utils, sol.pose
        except Exception:
            pass
    if hasattr(mp, "drawing_utils") and hasattr(mp, "pose"):
        return mp.drawing_utils, mp.pose
    return None, None


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  CAMERA  INITIALISATION  (CAP_DSHOW for Windows stability)
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
def init_camera(index: int = 0):
    print("[INFO] Opening camera...")
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,  720)
    if not cap.isOpened():
        print("[ERROR] Could not open camera.")
        sys.exit(1)
    return cap




# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  TKINTER  LAUNCHER  ?? Wellness & Eco-Friendly Theme
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�

# ?�?� Palette ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
_BG        = "#F4F9F4"   # soft mint off-white  (window background)
_BG_HEADER = "#FFFFFF"   # pure white header panel
_ACCENT    = "#2C5E3B"   # deep forest green  (titles, labels)
_ACCENT2   = "#4A8C5C"   # medium green  (secondary text)
_BTN       = "#4CAF50"   # vibrant green button
_BTN_HOV   = "#45A049"   # darker on hover
_MUTED     = "#7F8C8D"   # muted grey  (disclaimers, info)
_TROUGH    = "#C8E6C9"   # light green slider trough
_SEP       = "#D5E8D4"   # separator / divider line
_VAL_FG    = "#2C5E3B"   # slider value label


class LauncherApp:
    """
    Wellness-themed startup launcher for ErgoGuard International.
    Native-script language names are shown in the combobox.
    All visible strings update instantly when the language is changed.
    """

    def __init__(self, root: "tk.Tk"):
        self.root     = root
        self.settings = {}

        self.lang_var     = tk.StringVar(value="English")
        self.interval_var = tk.IntVar(value=60)
        self.privacy_var  = tk.BooleanVar(value=False)

        self.root.title("ErgoGuard International")
        self.root.resizable(False, False)
        self.root.configure(bg=_BG)
        self._center_window(560, 530)

        # ?�?� Apply ttk styles BEFORE building widgets ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground="#FFFFFF",
                        background="#FFFFFF",
                        foreground=_ACCENT,
                        selectbackground=_BTN,
                        selectforeground="white",
                        bordercolor=_SEP,
                        lightcolor=_SEP,
                        darkcolor=_SEP)
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#FFFFFF")],
                  foreground=[("readonly", _ACCENT)])
        style.configure("Green.Horizontal.TScale",
                        background=_BG,
                        troughcolor=_TROUGH,
                        sliderlength=20,
                        sliderrelief="flat",
                        bordercolor=_SEP)
        style.configure("TSeparator", background=_SEP)
        # Prevent OS-theme grey bleeding behind native text widgets
        style.configure("TLabel",
                        background=_BG,
                        foreground="#333333")
        style.configure("TCheckbutton",
                        background=_BG,
                        foreground="#333333",
                        focuscolor=_BG)
        style.map("TCheckbutton",
                  background=[("active", _BG)],
                  foreground=[("active", _ACCENT)])

        # ?�?� Fonts ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        try:
            f_brand  = tkfont.Font(family="Segoe UI", size=20, weight="bold")
            f_sub    = tkfont.Font(family="Segoe UI", size=10)
            f_label  = tkfont.Font(family="Segoe UI", size=12)
            f_small  = tkfont.Font(family="Segoe UI", size=9)
            f_val    = tkfont.Font(family="Segoe UI", size=11, weight="bold")
            f_button = tkfont.Font(family="Segoe UI", size=13, weight="bold")
            f_chk    = tkfont.Font(family="Segoe UI", size=11)
        except Exception:
            f_brand  = ("Helvetica", 20, "bold")
            f_sub    = ("Helvetica", 10)
            f_label  = ("Helvetica", 12)
            f_small  = ("Helvetica",  9)
            f_val    = ("Helvetica", 11, "bold")
            f_button = ("Helvetica", 13, "bold")
            f_chk    = ("Helvetica", 11)

        # ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        #  HEADER  (white card with green left accent bar)
        # ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        header_outer = tk.Frame(self.root, bg=_BG, pady=0)
        header_outer.pack(fill="x", padx=0, pady=0)

        # Thin green top accent strip
        tk.Frame(header_outer, bg=_BTN, height=4).pack(fill="x")

        header_card = tk.Frame(header_outer, bg=_BG_HEADER,
                               padx=32, pady=20)
        header_card.pack(fill="x")

        # Logo leaf icon (Unicode) + title on the same row
        title_row = tk.Frame(header_card, bg=_BG_HEADER)
        title_row.pack(anchor="w")

        tk.Label(title_row, text="\U0001F33F",       # ?��
                 bg=_BG_HEADER, fg=_BTN,
                 font=("Segoe UI Emoji", 20)).pack(side="left", padx=(0, 8))

        self.lbl_title = tk.Label(
            title_row, text="ErgoGuard International",
            bg=_BG_HEADER, fg=_ACCENT, font=f_brand)
        self.lbl_title.pack(side="left")

        self.lbl_sub = tk.Label(
            header_card,
            text="AI Posture & Wellness Guardian",
            bg=_BG_HEADER, fg="#555555", font=f_sub)
        self.lbl_sub.pack(anchor="w", pady=(4, 0))

        # Thin separator under header
        tk.Frame(self.root, bg=_SEP, height=1).pack(fill="x")

        # ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        #  FORM  BODY
        # ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        body = tk.Frame(self.root, bg=_BG, padx=36)
        body.pack(fill="both", expand=True, pady=(30, 22))
        body.columnconfigure(1, weight=1)

        # ?�?� Row 0  :  Language ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        self.lbl_lang = tk.Label(
            body, text="Language",
            bg=_BG, fg="#333333", font=f_label, anchor="w")
        self.lbl_lang.grid(row=0, column=0, sticky="w", pady=(0, 18))

        self.lang_combo = ttk.Combobox(
            body, textvariable=self.lang_var,
            values=LANGUAGE_LIST, state="readonly",
            width=26, font=f_label)
        self.lang_combo.grid(row=0, column=1, sticky="w",
                             pady=(0, 18), padx=(16, 0))
        self.lang_combo.bind("<<ComboboxSelected>>", self._on_lang_change)

        # ?�?� Divider ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        tk.Frame(body, bg=_SEP, height=1).grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(2, 18))

        # ?�?� Row 2  :  Interval slider ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        self.lbl_interval = tk.Label(
            body, text="Reminder Interval (minutes)",
            bg=_BG, fg="#333333", font=f_label, anchor="w")
        self.lbl_interval.grid(row=2, column=0, sticky="w", pady=(0, 16))

        slider_wrap = tk.Frame(body, bg=_BG)
        slider_wrap.grid(row=2, column=1, sticky="w",
                         pady=(0, 16), padx=(16, 0))

        self.slider = ttk.Scale(
            slider_wrap, from_=15, to=120,
            orient="horizontal", length=190,
            variable=self.interval_var,
            command=self._on_slider,
            style="Green.Horizontal.TScale")
        self.slider.pack(side="left")

        self.lbl_slider_val = tk.Label(
            slider_wrap, text="60 min",
            bg=_BG, fg=_VAL_FG, font=f_val, width=7)
        self.lbl_slider_val.pack(side="left", padx=(10, 0))

        # ?�?� Divider ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        tk.Frame(body, bg=_SEP, height=1).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(2, 18))

        # ?�?� Row 4  :  Privacy checkbox ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        self.chk_privacy = tk.Checkbutton(
            body,
            text="Privacy Mode  ?? Stickman skeleton only, no raw camera feed",
            variable=self.privacy_var,
            bg=_BG, fg="#333333",
            selectcolor="#FFFFFF",
            activebackground=_BG,
            activeforeground=_ACCENT,
            font=f_chk, anchor="w",
            cursor="hand2")
        self.chk_privacy.grid(row=4, column=0, columnspan=2,
                               sticky="w", pady=(0, 12))

        # ?�?� Row 5  :  Disclaimer note ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        note = ("Edge Computing: all AI runs locally ??zero data leaves your device.\n"
                "Privacy Mode visualises joint geometry only, never your appearance.")
        self.lbl_info = tk.Label(
            body, text=note,
            bg=_BG, fg="#555555", font=f_small,
            justify="left", anchor="w")
        self.lbl_info.grid(row=5, column=0, columnspan=2,
                            sticky="w", pady=(0, 6))

        # ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        #  FOOTER  ?? Start button
        # ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        tk.Frame(self.root, bg=_SEP, height=1).pack(fill="x")

        footer = tk.Frame(self.root, bg=_BG_HEADER, padx=36, pady=20)
        footer.pack(fill="x")

        # Centred button row ??both buttons in a self-centering sub-frame
        btn_row = tk.Frame(footer, bg=_BG_HEADER)
        btn_row.pack(anchor="center")

        self.btn_start = tk.Button(
            btn_row,
            text="  \U0001F7E2  Start ErgoGuard  ",   # ?��
            command=self._on_start,
            bg=_BTN, fg="white",
            activebackground=_BTN_HOV, activeforeground="white",
            font=f_button,
            relief="flat",
            padx=24, pady=11,
            cursor="hand2",
            bd=0)
        self.btn_start.pack(side="left", ipadx=6, ipady=2)

        # Reminders button ??evenly spaced to the right of Start
        self.btn_reminder = tk.Button(
            btn_row,
            text="  \U0001F514  Reminders  ",
            command=self._on_reminders,
            bg=_BG, fg=_ACCENT,
            activebackground=_SEP, activeforeground=_ACCENT,
            font=f_button,
            relief="flat",
            padx=16, pady=11,
            cursor="hand2",
            bd=1,
            highlightthickness=1,
            highlightbackground=_ACCENT2,
            highlightcolor=_ACCENT)
        self.btn_reminder.pack(side="left", padx=(14, 0), ipadx=6, ipady=2)

        # Version tag centred below the buttons
        tk.Label(footer,
                 text="v2.0  \u00b7  MediaPipe + OpenCV",
                 bg=_BG_HEADER, fg="#555555",
                 font=f_small).pack(pady=(10, 0))

    # ?�?� Internal helpers ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    def _center_window(self, w: int, h: int) -> None:
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _on_slider(self, _=None) -> None:
        self.lbl_slider_val.config(text=f"{int(self.interval_var.get())} min")

    def _on_lang_change(self, _=None) -> None:
        t = TRANSLATIONS.get(self.lang_var.get(), TRANSLATIONS["English"])
        self.lbl_title.config(text=t["title"])
        self.lbl_sub.config(text=t["subtitle"])
        self.lbl_lang.config(text=t["language"])
        self.lbl_interval.config(text=t["interval"])
        self.chk_privacy.config(text=t["privacy"])
        self.btn_start.config(text=f"  \U0001F7E2  {t['start']}  ")
        r = _REMINDER_I18N.get(self.lang_var.get(), _REMINDER_I18N["English"])
        self.btn_reminder.config(text=f"  {r['reminder_btn']}  ")

    def _on_reminders(self) -> None:
        """Open the ReminderManagerUI Toplevel."""
        ReminderManagerUI(self.root, language=self.lang_var.get())

    def _on_start(self) -> None:
        self.settings = {
            "language": self.lang_var.get(),
            "interval": int(self.interval_var.get()),
            "privacy":  self.privacy_var.get(),
        }
        self.root.destroy()

    def run(self) -> dict:
        self.root.mainloop()
        return self.settings


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  DAILY  REMINDER  MANAGER  ?? Toplevel UI
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�

# Category accent colours  (used in both the UI and the OpenCV overlay)
_CAT_COLORS: dict[str, str] = {
    "Work":   "#4A90D9",   # professional blue
    "Health": "#4CAF50",   # wellness green
    "Break":  "#F5A623",   # warm amber
    "Urgent": "#E74C3C",   # alert red
}

# BGR equivalents for OpenCV HUD drawing
_CAT_BGR: dict[str, tuple] = {
    "Work":   (217, 144,  74),
    "Health": ( 80, 175,  76),
    "Break":  ( 35, 166, 245),
    "Urgent": ( 60,  76, 231),
}

# Lightweight i18n for the reminder window (separate from TRANSLATIONS)
_REMINDER_I18N: dict = {
    "English":   {"win_title": "Daily Reminders",       "name_ph": "Task name\u2026",             "time_lbl": "Time  (HH : MM)",    "cat_lbl": "Category",        "add_btn": "+  Add Reminder",     "del_btn": "Delete",        "done_btn": "\u2713  Mark Done",     "no_items": "No reminders yet \u2013 add one above",  "col_work": "Work",    "col_health": "Health",  "col_break": "Break",    "col_urgent": "Urgent",  "reminder_btn": "\U0001F514  Reminders"},
    "\u7e41\u9ad4\u4e2d\u6587": {"win_title": "\u6bcf\u65e5\u63d0\u9192",             "name_ph": "\u4efb\u52d9\u540d\u7a31\u2026",           "time_lbl": "\u6642\u9593  (HH : MM)",     "cat_lbl": "\u985e\u5225",        "add_btn": "+  \u65b0\u589e\u63d0\u9192",       "del_btn": "\u522a\u9664",       "done_btn": "\u2713  \u6a19\u8a18\u5b8c\u6210",  "no_items": "\u5c1a\u7121\u63d0\u9192\uff0c\u8acb\u5728\u4e0a\u65b9\u65b0\u589e",    "col_work": "\u5de5\u4f5c", "col_health": "\u5065\u5eb7", "col_break": "\u4f11\u606f", "col_urgent": "\u7dca\u6025", "reminder_btn": "\U0001F514  \u63d0\u9192\u4e8b\u9805"},
    "Espa\u00f1ol":  {"win_title": "Recordatorios Diarios",    "name_ph": "Nombre de la tarea\u2026",      "time_lbl": "Hora  (HH : MM)",     "cat_lbl": "Categor\u00eda",    "add_btn": "+  Agregar",           "del_btn": "Eliminar",     "done_btn": "\u2713  Hecho",          "no_items": "Sin recordatorios \u2013 agrega uno arriba",       "col_work": "Trabajo","col_health": "Salud",   "col_break": "Descanso","col_urgent": "Urgente","reminder_btn": "\U0001F514  Recordatorios"},
    "\u65e5\u672c\u8a9e":   {"win_title": "\u30c7\u30a4\u30ea\u30fc\u30ea\u30de\u30a4\u30f3\u30c0\u30fc","name_ph": "\u30bf\u30b9\u30af\u540d\u2026",              "time_lbl": "\u6642\u523b  (HH : MM)",     "cat_lbl": "\u30ab\u30c6\u30b4\u30ea",   "add_btn": "+  \u8ffd\u52a0",             "del_btn": "\u524a\u9664",       "done_btn": "\u2713  \u5b8c\u4e86",          "no_items": "\u30ea\u30de\u30a4\u30f3\u30c0\u30fc\u306a\u3057 \u2013 \u4e0a\u3067\u8ffd\u52a0",              "col_work": "\u4ed5\u4e8b","col_health": "\u5065\u5eb7","col_break": "\u4f11\u61a9","col_urgent": "\u7dca\u6025","reminder_btn": "\U0001F514  \u30ea\u30de\u30a4\u30f3\u30c0\u30fc"},
    "\ud55c\uad6d\uc5b4":   {"win_title": "\uc77c\uc77c \uc54c\ub9bc",             "name_ph": "\uc791\uc5c5 \uc774\ub984\u2026",            "time_lbl": "\uc2dc\uac04  (HH : MM)",     "cat_lbl": "\uce74\ud14c\uace0\ub9ac",  "add_btn": "+  \ucd94\uac00",             "del_btn": "\uc0ad\uc81c",       "done_btn": "\u2713  \uc644\ub8cc",          "no_items": "\uc54c\ub9bc \uc5c6\uc74c \u2013 \uc704\uc5d0\uc11c \ucd94\uac00",              "col_work": "\uc5c5\ubb34","col_health": "\uac74\uac15","col_break": "\ud734\uc2dd","col_urgent": "\uae34\uae09","reminder_btn": "\U0001F514  \uc54c\ub9bc"},
    "Fran\u00e7ais":  {"win_title": "Rappels Quotidiens",       "name_ph": "Nom de la t\u00e2che\u2026",          "time_lbl": "Heure  (HH : MM)",    "cat_lbl": "Cat\u00e9gorie",   "add_btn": "+  Ajouter",           "del_btn": "Supprimer",    "done_btn": "\u2713  Termin\u00e9",        "no_items": "Aucun rappel \u2013 ajoutez-en un ci-dessus",       "col_work": "Travail","col_health": "Sant\u00e9",  "col_break": "Pause",   "col_urgent": "Urgent",  "reminder_btn": "\U0001F514  Rappels"},
    "Deutsch":   {"win_title": "T\u00e4gliche Erinnerungen",   "name_ph": "Aufgabenname\u2026",              "time_lbl": "Zeit  (HH : MM)",     "cat_lbl": "Kategorie",   "add_btn": "+  Hinzuf\u00fcgen",       "del_btn": "L\u00f6schen",    "done_btn": "\u2713  Erledigt",         "no_items": "Keine Erinnerungen \u2013 f\u00fcge eine oben hinzu",     "col_work": "Arbeit", "col_health": "Gesundheit","col_break": "Pause",   "col_urgent": "Dringend","reminder_btn": "\U0001F514  Erinnerungen"},
    "\u0420\u0443\u0441\u0441\u043a\u0438\u0439":  {"win_title": "\u0415\u0436\u0435\u0434\u043d\u0435\u0432\u043d\u044b\u0435 \u043d\u0430\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u044f","name_ph": "\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0437\u0430\u0434\u0430\u0447\u0438\u2026",      "time_lbl": "\u0412\u0440\u0435\u043c\u044f  (HH : MM)",  "cat_lbl": "\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f","add_btn": "+  \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c",        "del_btn": "\u0423\u0434\u0430\u043b\u0438\u0442\u044c",  "done_btn": "\u2713  \u0412\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u043e",    "no_items": "\u041d\u0435\u0442 \u043d\u0430\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u0439 \u2013 \u0434\u043e\u0431\u0430\u0432\u044c\u0442\u0435 \u0432\u044b\u0448\u0435",       "col_work": "\u0420\u0430\u0431\u043e\u0442\u0430","col_health": "\u0417\u0434\u043e\u0440\u043e\u0432\u044c\u0435","col_break": "\u041f\u0435\u0440\u0435\u0440\u044b\u0432","col_urgent": "\u0421\u0440\u043e\u0447\u043d\u043e","reminder_btn": "\U0001F514  \u041d\u0430\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u044f"},
    "Portugu\u00eas": {"win_title": "Lembretes Di\u00e1rios",      "name_ph": "Nome da tarefa\u2026",            "time_lbl": "Hora  (HH : MM)",     "cat_lbl": "Categoria",   "add_btn": "+  Adicionar",          "del_btn": "Excluir",      "done_btn": "\u2713  Conclu\u00eddo",       "no_items": "Sem lembretes \u2013 adicione um acima",            "col_work": "Trabalho","col_health": "Sa\u00fade",  "col_break": "Pausa",   "col_urgent": "Urgente","reminder_btn": "\U0001F514  Lembretes"},
    "\u0627\u0644\u0639\u0631\u0628\u064a\u0629":   {"win_title": "\u0627\u0644\u062a\u0630\u0643\u064a\u0631\u0627\u062a \u0627\u0644\u064a\u0648\u0645\u064a\u0629",  "name_ph": "\u0627\u0633\u0645 \u0627\u0644\u0645\u0647\u0645\u0629\u2026",            "time_lbl": "\u0627\u0644\u0648\u0642\u062a  (HH : MM)",  "cat_lbl": "\u0627\u0644\u0641\u0626\u0629",     "add_btn": "+  \u0625\u0636\u0627\u0641\u0629",           "del_btn": "\u062d\u0630\u0641",       "done_btn": "\u2713  \u062a\u0645",              "no_items": "\u0644\u0627 \u062a\u0648\u062c\u062f \u062a\u0630\u0643\u064a\u0631\u0627\u062a \u2013 \u0623\u0636\u0641 \u0648\u0627\u062d\u062f\u0629 \u0623\u0639\u0644\u0627\u0647",      "col_work": "\u0639\u0645\u0644","col_health": "\u0635\u062d\u0629",  "col_break": "\u0627\u0633\u062a\u0631\u0627\u062d\u0629","col_urgent": "\u0639\u0627\u062c\u0644","reminder_btn": "\U0001F514  \u0627\u0644\u062a\u0630\u0643\u064a\u0631\u0627\u062a"},
}


class ReminderManagerUI:
    """Modal Toplevel for managing daily reminders with colour-coded categories."""

    def __init__(self, parent: tk.Tk, language: str = "English") -> None:
        self._lang = language
        self._r    = _REMINDER_I18N.get(language, _REMINDER_I18N["English"])
        self._cat_var = tk.StringVar(value="Health")
        self._name_placeholder = self._r["name_ph"]

        win = tk.Toplevel(parent)
        win.title(self._r["win_title"])
        win.configure(bg=_BG)
        win.resizable(False, False)
        win.grab_set()          # modal ??block launcher while open
        self._win = win

        # ?�?� Center on screen ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        win.update_idletasks()
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        win.geometry(f"540x640+{(sw-540)//2}+{(sh-640)//2}")

        # ?�?� Font stack ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        _ff     = "Segoe UI"   # Tkinter falls back gracefully if unavailable
        f_title = (_ff, 13, "bold")
        f_lbl   = (_ff,  9, "bold")
        f_body  = (_ff,  9)
        f_small = (_ff,  8)
        f_btn   = (_ff,  9, "bold")

        # ?�?� Green accent header bar ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        tk.Frame(win, bg=_ACCENT, height=4).pack(fill="x")
        hdr = tk.Frame(win, bg=_BG_HEADER, padx=22, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr,
                 text=f"\U0001F514  {self._r['win_title']}",
                 bg=_BG_HEADER, fg=_ACCENT, font=f_title).pack(anchor="w")

        # ?�?� INPUT PANEL ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        tk.Frame(win, bg=_SEP, height=1).pack(fill="x")
        inp = tk.Frame(win, bg=_BG, padx=22, pady=16)
        inp.pack(fill="x")
        inp.columnconfigure(1, weight=1)

        # Row 0 ??Task name entry
        tk.Label(inp, text=self._r["name_ph"].rstrip("\u2026"),
                 bg=_BG, fg=_ACCENT, font=f_lbl
                 ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        self._name_var = tk.StringVar()
        self._name_entry = tk.Entry(
            inp, textvariable=self._name_var,
            font=f_body, relief="flat",
            bg=_BG_HEADER, fg=_MUTED,
            insertbackground=_ACCENT,
            highlightthickness=1,
            highlightcolor=_BTN,
            highlightbackground=_SEP)
        self._name_entry.grid(row=0, column=1, columnspan=3,
                              sticky="ew", ipady=6, pady=(0, 4))
        self._name_entry.insert(0, self._name_placeholder)
        self._name_entry.bind("<FocusIn>",
                              lambda e: self._ph_focus_in(self._name_entry))
        self._name_entry.bind("<FocusOut>",
                              lambda e: self._ph_focus_out(self._name_entry))

        # Row 1 ??Time picker (HH spinbox  :  MM spinbox)
        tk.Label(inp, text=self._r["time_lbl"],
                 bg=_BG, fg=_ACCENT, font=f_lbl
                 ).grid(row=1, column=0, sticky="w", pady=(10, 4))
        time_frm = tk.Frame(inp, bg=_BG)
        time_frm.grid(row=1, column=1, columnspan=3, sticky="w", pady=(10, 4))

        self._hour_var = tk.StringVar(value="09")
        self._min_var  = tk.StringVar(value="00")
        _sp = dict(font=f_body, bg=_BG_HEADER, fg=_ACCENT,
                   relief="flat", width=3,
                   highlightthickness=1, highlightcolor=_BTN,
                   highlightbackground=_SEP, buttonbackground=_BG)
        tk.Spinbox(time_frm, from_=0, to=23, format="%02.0f",
                   textvariable=self._hour_var, **_sp).pack(side="left")
        tk.Label(time_frm, text=" : ", bg=_BG, fg=_ACCENT,
                 font=f_title).pack(side="left")
        tk.Spinbox(time_frm, from_=0, to=59, format="%02.0f",
                   textvariable=self._min_var, **_sp).pack(side="left")

        # Row 2 ??Category colour radio row
        tk.Label(inp, text=self._r["cat_lbl"],
                 bg=_BG, fg=_ACCENT, font=f_lbl
                 ).grid(row=2, column=0, sticky="nw", pady=(10, 4))
        cat_frm = tk.Frame(inp, bg=_BG)
        cat_frm.grid(row=2, column=1, columnspan=3, sticky="w", pady=(10, 4))

        _cat_map = [
            ("Work",   "col_work"),
            ("Health", "col_health"),
            ("Break",  "col_break"),
            ("Urgent", "col_urgent"),
        ]
        for key, dk in _cat_map:
            col = _CAT_COLORS[key]
            cell = tk.Frame(cat_frm, bg=_BG, padx=2)
            cell.pack(side="left", padx=(0, 10))
            # Colour swatch (4 px wide coloured bar on the left)
            tk.Frame(cell, bg=col, width=5, height=18).pack(
                side="left", padx=(0, 4))
            tk.Radiobutton(
                cell,
                text=self._r[dk],
                variable=self._cat_var,
                value=key,
                bg=_BG, fg=col,
                selectcolor=_BG,
                activebackground=_BG,
                activeforeground=col,
                font=(_ff, 9, "bold"),
                cursor="hand2",
            ).pack(side="left")

        # Row 3 ??Add button
        tk.Button(
            inp,
            text=self._r["add_btn"],
            command=self._on_add,
            bg=_BTN, fg="white",
            activebackground=_BTN_HOV, activeforeground="white",
            font=f_btn, relief="flat",
            padx=18, pady=8, cursor="hand2", bd=0,
        ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(14, 2))

        # ?�?� REMINDER LIST ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        tk.Frame(win, bg=_SEP, height=1).pack(fill="x")
        list_outer = tk.Frame(win, bg=_BG, padx=22, pady=12)
        list_outer.pack(fill="both", expand=True)

        # ttk.Treeview ??columns: time | name | category
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Rem.Treeview",
                         background=_BG_HEADER, foreground=_ACCENT,
                         fieldbackground=_BG_HEADER, rowheight=30,
                         font=(_ff, 9))
        style.configure("Rem.Treeview.Heading",
                         background=_SEP, foreground=_ACCENT,
                         font=(_ff, 9, "bold"), relief="flat")
        style.map("Rem.Treeview",
                  background=[("selected", _TROUGH)],
                  foreground=[("selected", _ACCENT)])

        cols = ("time", "name", "category")
        self._tree = ttk.Treeview(
            list_outer, columns=cols, show="headings",
            style="Rem.Treeview", selectmode="browse", height=8)
        self._tree.heading("time",     text="\u23f0  HH:MM")
        self._tree.heading("name",     text="\U0001F4DD  Task")
        self._tree.heading("category", text="\U0001F3F7  Category")
        self._tree.column("time",      width=80,  anchor="center")
        self._tree.column("name",      width=245, anchor="w")
        self._tree.column("category",  width=100, anchor="center")

        for cat, col in _CAT_COLORS.items():
            self._tree.tag_configure(cat,
                                     foreground=col,
                                     font=(_ff, 9, "bold"))
        self._tree.tag_configure("done",
                                 foreground=_MUTED,
                                 font=(_ff, 9, "overstrike"))

        vsb = ttk.Scrollbar(list_outer, orient="vertical",
                            command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self._lbl_empty = tk.Label(
            list_outer, text=self._r["no_items"],
            bg=_BG, fg=_MUTED, font=f_small)

        # ?�?� ACTION BAR (Done / Delete) ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
        tk.Frame(win, bg=_SEP, height=1).pack(fill="x")
        act = tk.Frame(win, bg=_BG_HEADER, padx=22, pady=10)
        act.pack(fill="x")

        _ab = dict(relief="flat", font=f_btn,
                   padx=16, pady=6, cursor="hand2", bd=0)
        tk.Button(act, text=self._r["done_btn"],
                  command=self._on_done,
                  bg=_BTN, fg="white",
                  activebackground=_BTN_HOV, activeforeground="white",
                  **_ab).pack(side="left", padx=(0, 8))
        tk.Button(act, text=self._r["del_btn"],
                  command=self._on_delete,
                  bg="#E74C3C", fg="white",
                  activebackground="#C0392B", activeforeground="white",
                  **_ab).pack(side="left")

        self._refresh_list()

    # ?�?� Placeholder helpers ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    def _ph_focus_in(self, entry: tk.Entry) -> None:
        if entry.get() == self._name_placeholder:
            entry.delete(0, "end")
            entry.config(fg=_ACCENT)

    def _ph_focus_out(self, entry: tk.Entry) -> None:
        if not entry.get():
            entry.insert(0, self._name_placeholder)
            entry.config(fg=_MUTED)

    # ?�?� CRUD helpers ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    def _on_add(self) -> None:
        name = self._name_var.get().strip()
        if not name or name == self._name_placeholder:
            return
        try:
            hh = max(0, min(23, int(self._hour_var.get())))
            mm = max(0, min(59, int(self._min_var.get())))
        except ValueError:
            return
        DAILY_REMINDERS.append({
            "name":     name,
            "hour":     hh,
            "minute":   mm,
            "category": self._cat_var.get(),
            "done":     False,
        })
        # Reset the name field to placeholder
        self._name_var.set("")
        self._ph_focus_out(self._name_entry)
        self._refresh_list()

    def _selected_index(self) -> "int | None":
        sel = self._tree.selection()
        return self._tree.index(sel[0]) if sel else None

    def _on_done(self) -> None:
        idx = self._selected_index()
        if idx is not None:
            DAILY_REMINDERS[idx]["done"] = not DAILY_REMINDERS[idx]["done"]
            self._refresh_list()

    def _on_delete(self) -> None:
        idx = self._selected_index()
        if idx is not None:
            del DAILY_REMINDERS[idx]
            self._refresh_list()

    def _refresh_list(self) -> None:
        """Repopulate the Treeview from DAILY_REMINDERS."""
        for iid in self._tree.get_children():
            self._tree.delete(iid)
        for rem in DAILY_REMINDERS:
            tag  = "done" if rem["done"] else rem["category"]
            hhmm = f"{rem['hour']:02d}:{rem['minute']:02d}"
            name = ("\u2713  " if rem["done"] else "") + rem["name"]
            self._tree.insert("", "end",
                              values=(hhmm, name, rem["category"]),
                              tags=(tag,))
        if DAILY_REMINDERS:
            self._lbl_empty.place_forget()
        else:
            self._lbl_empty.place(relx=0.5, rely=0.5, anchor="center")


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  MATPLOTLIB  REPORT  ?? Donut chart  +  Health Grade  +  ESG footer
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
def generate_report(posture_log: list, session_start: float,
                    language: str = "English") -> None:
    """Save ErgoGuard_Report.png then open it with the system viewer.

    Fixes & enhancements vs. original:
    - CJK font stack prevents ??boxes for Chinese / Japanese / Korean text.
    - All chart text is fully localised via the TRANSLATIONS dict.
    - Lenient A / B / F grading with contextual feedback message.
    - plt.savefig wrapped in try/finally so plt.close() always runs.
    """
    if not MPL_OK:
        print("[WARN] matplotlib unavailable ??skipping report.")
        return
    if not posture_log:
        print("[WARN] No posture data ??skipping report.")
        return

    # ?�?� CJK / Unicode font stack ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    # Tries system fonts in order; matplotlib falls back gracefully if absent.
    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei", "SimHei", "Noto Sans CJK SC",
        "Arial Unicode MS", "DejaVu Sans", "sans-serif",
    ]
    plt.rcParams["axes.unicode_minus"] = False   # fixes minus-sign rendering

    t = TRANSLATIONS.get(language, TRANSLATIONS["English"])

    # ?�?� Compute stats ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    statuses  = [e[2] for e in posture_log]
    angles    = [e[1] for e in posture_log]
    good_n    = sum(1 for s in statuses if s == "Good")
    bad_n     = sum(1 for s in statuses if s == "Bad")
    present_n = good_n + bad_n

    good_pct  = (good_n / present_n * 100) if present_n > 0 else 0.0
    grade     = health_grade(good_pct)
    grade_col = GRADE_COLOR[grade]

    # ?�?� Localised feedback sentence for the grade ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    _fb_defaults = {
        "A": "Excellent!  Keep it up.",
        "B": "Average.  Try to sit straight more often to protect your spine.",
        "F": "Danger!  Bad posture for most of your session.  Please stretch now!",
    }
    _fb_key  = {"A": "grade_A_msg", "B": "grade_B_msg", "F": "grade_F_msg"}
    feedback = t.get(_fb_key[grade], _fb_defaults[grade])

    session_secs = (posture_log[-1][0] - session_start) if posture_log else 0
    session_mins = session_secs / 60.0

    neck_loads = [calc_neck_load(a) for a in angles if a < 179.9]
    avg_neck   = (sum(neck_loads) / len(neck_loads)) if neck_loads else 4.5

    bad_frac  = bad_n / present_n if present_n > 0 else 0.5
    max_slouch_time = calc_max_slouch_duration(posture_log)

    # ?�?� Figure ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    fig = plt.figure(figsize=(14, 8), facecolor="#1A1A2E")
    gs  = fig.add_gridspec(2, 3,
                           height_ratios=[5, 1],
                           hspace=0.05, wspace=0.3,
                           left=0.06, right=0.97,
                           top=0.88, bottom=0.08)

    ax_donut = fig.add_subplot(gs[0, 0:2])
    ax_stats  = fig.add_subplot(gs[0, 2])
    ax_footer = fig.add_subplot(gs[1, :])

    for ax in (ax_donut, ax_stats, ax_footer):
        ax.set_facecolor("#16213E")
        ax.tick_params(colors="white")
        for sp in ax.spines.values():
            sp.set_edgecolor("#2C3E50")

    # ?�?� (a) Donut chart ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    sizes  = [good_pct, 100.0 - good_pct] if present_n > 0 else [50, 50]
    colors = ["#2ECC71", "#E74C3C"]

    ax_donut.pie(sizes,
                 colors=colors,
                 explode=(0.04, 0.0),
                 startangle=90,
                 wedgeprops=dict(width=0.52,
                                 edgecolor="#1A1A2E",
                                 linewidth=2),
                 shadow=True)

    # ?�?� (b) Content in the donut hole ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    ax_donut.text(0,  0.22, grade,
                  ha="center", va="center",
                  fontsize=72, fontweight="bold",
                  color=grade_col)
    ax_donut.text(0, -0.18, t["grade_label"],
                  ha="center", va="center",
                  fontsize=12, color="#A8DADC")
    ax_donut.text(0, -0.38, f"{good_pct:.1f}%  {t['good_label']}",
                  ha="center", va="center",
                  fontsize=10, color="#7F8C8D")
    # Contextual feedback sentence (localised, grade-appropriate colour)
    ax_donut.text(0, -0.62, feedback,
                  ha="center", va="center",
                  fontsize=8.5, color=grade_col,
                  fontstyle="italic",
                  wrap=True)

    legend_patches = [
        mpatches.Patch(color=colors[i],
                       label=f"{[t['good_label'], t['bad_label']][i]}  {sizes[i]:.1f}%")
        for i in range(2)
    ]
    ax_donut.legend(handles=legend_patches,
                    loc="lower center",
                    bbox_to_anchor=(0.5, -0.12),
                    ncol=2, frameon=False,
                    labelcolor="white", fontsize=11)
    ax_donut.set_title(t["report_title"],
                       color="white", fontsize=15,
                       fontweight="bold", pad=14)

    # ?�?� Stats table (fully localised) ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    ax_stats.axis("off")
    rows = [
        (t.get("session_time",   "Session Time"),   f"{session_mins:.1f} min"),
        (t.get("frames",         "Frames"),          f"{len(posture_log):,}"),
        (t["good_label"],                            f"{good_n:,}"),
        (t["bad_label"],                             f"{bad_n:,}"),
        (t.get("good_pct_label", "Good Posture %"),  f"{good_pct:.1f} %"),
        (t["grade_label"],                           grade),
        (t["neck_avg"],                              f"{avg_neck:.1f} kg"),
        (t["carbon_label"],                          max_slouch_time),
    ]
    for i, (label, value) in enumerate(rows):
        y  = 0.95 - i * 0.115
        vc = grade_col if label == t["grade_label"] else "white"
        ax_stats.text(0.04, y, label,
                      transform=ax_stats.transAxes,
                      color="#A8DADC", fontsize=9.5, va="top")
        ax_stats.text(0.98, y, value,
                      transform=ax_stats.transAxes,
                      color=vc, fontsize=9.5, va="top",
                      ha="right", fontweight="bold")
    ax_stats.set_title(t.get("session_stats", "Session Statistics"),
                       color="white", fontsize=12,
                       fontweight="bold", pad=10)

    # ?�?� (c) ESG footer (localised) ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    ax_footer.axis("off")
    ax_footer.axhline(y=0.95, color="#2C3E50", linewidth=1,
                      xmin=0.02, xmax=0.98)
    footer_txt = (
        f"  [Metrics]  {t['carbon_label']}: {max_slouch_time}"
        f"   |   [Health]  {t['neck_avg']}: {avg_neck:.1f} kg"
        f"   |   {t.get('session_time', 'Session')}: {session_mins:.1f} min"
        f"   |   ErgoGuard International ??MediaPipe + OpenCV"
    )
    ax_footer.text(0.5, 0.50, footer_txt,
                   ha="center", va="center",
                   transform=ax_footer.transAxes,
                   color="#7F8C8D", fontsize=9)

    fig.suptitle(
        f"ErgoGuard International  ·  {t.get('session_stats', 'Session Analytics')}",
        color="#E94560", fontsize=17, fontweight="bold", y=0.97)

    # ?�?� Save & open ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "ErgoGuard_Report.png")
    try:
        plt.savefig(out_path, dpi=150, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        print(f"[INFO] Report saved  ?? {out_path}")
    except Exception as exc:
        print(f"[ERROR] Could not save report: {exc}")
        return
    finally:
        plt.close(fig)

    try:
        if sys.platform == "win32":
            os.startfile(out_path)
        else:
            import subprocess
            subprocess.Popen(["xdg-open", out_path])
    except Exception as exc:
        print(f"[WARN] Could not auto-open report: {exc}")


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  HUD  OVERLAY
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
def draw_hud(frame: "np.ndarray",
             status_text: str,
             angle: float,
             neck_load: float,
             remaining_secs: float,
             lang: str,
             privacy: bool) -> None:
    """Render real-time HUD information onto the display frame."""
    t    = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
    h, w = frame.shape[:2]
    bad  = "[!!]" in status_text

    # Semi-transparent top bar
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 58), (22, 22, 46), -1)
    cv2.addWeighted(overlay, 0.72, frame, 0.28, 0, frame)

    # Status
    color = (55, 55, 220) if bad else (55, 200, 55)
    cv2.putText(frame, status_text, (14, 38),
                cv2.FONT_HERSHEY_DUPLEX, 1.0, color, 2, cv2.LINE_AA)

    # Angle & Neck Load (bottom-left)
    cv2.putText(frame, f"{t['angle']}: {angle:.1f}",
                (14, h - 56),
                cv2.FONT_HERSHEY_SIMPLEX, 0.68, (180, 220, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f"{t['neck_load']}: {neck_load:.1f} kg",
                (14, h - 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.68, (255, 200, 100), 1, cv2.LINE_AA)

    # Countdown timer (bottom-right)
    mins  = int(remaining_secs) // 60
    secs  = int(remaining_secs) % 60
    timer = f"Break in: {mins:02d}:{secs:02d}"
    (tw, _), _ = cv2.getTextSize(timer, cv2.FONT_HERSHEY_SIMPLEX, 0.65, 1)
    cv2.putText(frame, timer,
                (w - tw - 14, h - 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (160, 160, 255), 1, cv2.LINE_AA)

    # Privacy badge
    if privacy:
        badge = t["privacy_label"]
        (bw, _), _ = cv2.getTextSize(badge, cv2.FONT_HERSHEY_SIMPLEX, 0.52, 1)
        cv2.putText(frame, badge,
                    (w - bw - 14, 38),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (100, 220, 255), 1, cv2.LINE_AA)

    # Quit tip (bottom centre)
    tip = t["quit_tip"]
    (tw2, _), _ = cv2.getTextSize(tip, cv2.FONT_HERSHEY_SIMPLEX, 0.46, 1)
    cv2.putText(frame, tip,
                ((w - tw2) // 2, h - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.46, (90, 90, 90), 1, cv2.LINE_AA)


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  POSTURE  ANALYSER
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
# ?�?� Posture thresholds (tuned for natural sitting tolerance) ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
# Raised to reduce false positives from minor, natural body shifts.
_SHOULDER_Y_DIFF = 0.12   # was 0.08 ??allows ~30% more shoulder height asymmetry
_EAR_FWD_RATIO   = 0.50   # was 0.40 ??more tolerant of slight head-forward lean
_EAR_LOW_REL_SHD = 0.12   # was 0.09 ??ignores small downward ear drift
_INCLINE_THRESH  = 140.0  # was 145° ??needs more pronounced forward lean to flag
# Only flag bad posture after this many consecutive bad frames (~0.3 s @ 30 fps)
_BAD_STREAK_REQUIRED = 10


def _vec_angle_deg(ax: float, ay: float, bx: float, by: float) -> float:
    """Angle between 2-D vectors in degrees."""
    dot  = ax * bx + ay * by
    lena = math.hypot(ax, ay)
    lenb = math.hypot(bx, by)
    if lena < 1e-6 or lenb < 1e-6:
        return 180.0
    return math.degrees(math.acos(max(-1.0, min(1.0, dot / (lena * lenb)))))


def analyse_landmarks(lm_list, w: int, h: int):
    """
    Evaluate a MediaPipe landmark list.
    Returns (posture_bad: bool, inclination: float, coords: dict).
    coords maps landmark index -> (px, py) pixel position.
    """
    posture_bad = False
    inclination = 180.0
    coords: dict = {}

    if lm_list is None:
        return posture_bad, inclination, coords

    def get(idx):
        try:
            lm  = lm_list[idx]
            vis = getattr(lm, "visibility", 1.0)
            return lm.x, lm.y, vis > 0.25
        except (IndexError, AttributeError):
            return None

    for i in range(min(33, len(lm_list))):
        r = get(i)
        if r:
            coords[i] = (int(r[0] * w), int(r[1] * h))

    ls = get(11); rs = get(12)
    if not ls or not rs or not ls[2] or not rs[2]:
        return posture_bad, inclination, coords

    # Condition A ??uneven shoulders
    if abs(ls[1] - rs[1]) > _SHOULDER_Y_DIFF:
        posture_bad = True

    sh_w = abs(ls[0] - rs[0])

    # Condition B ??ear forward/low relative to shoulder
    for (ear_i, sh_x, sh_y) in ((7, ls[0], ls[1]), (8, rs[0], rs[1])):
        ear = get(ear_i)
        if ear and ear[2]:
            if sh_w > 1e-6 and abs(ear[0] - sh_x) / sh_w > _EAR_FWD_RATIO:
                posture_bad = True
            if ear[1] - sh_y > _EAR_LOW_REL_SHD:
                posture_bad = True

    # Condition C ??inclination angle (both sides, take worst)
    angles_calc = []
    for (ei, si, hi) in ((7, 11, 23), (8, 12, 24)):
        ear = get(ei); sh = get(si); hip = get(hi)
        if ear and sh and hip and ear[2] and sh[2] and hip[2]:
            ang = _vec_angle_deg(ear[0]-sh[0], ear[1]-sh[1],
                                 hip[0]-sh[0], hip[1]-sh[1])
            angles_calc.append(ang)
            if ang < _INCLINE_THRESH:
                posture_bad = True

    if angles_calc:
        inclination = min(angles_calc)

    return posture_bad, inclination, coords


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  PRIVACY  STICKMAN  DRAWING
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
_SKELETON = [
    (0,1),(1,2),(2,3),(3,7),(0,4),(4,5),(5,6),(6,8),(9,10),
    (11,12),(11,23),(12,24),(23,24),
    (11,13),(13,15),(12,14),(14,16),
    (23,25),(25,27),(24,26),(26,28),
]


def draw_stickman(canvas: "np.ndarray", coords: dict, bad: bool) -> None:
    """Draw a minimal skeleton on a canvas (privacy stickman mode)."""
    jc = (80,  80, 230) if bad else (160, 240, 160)
    bc = (60,  60, 200) if bad else (100, 220, 255)

    for (a, b) in _SKELETON:
        if a in coords and b in coords:
            cv2.line(canvas, coords[a], coords[b], bc, 2, cv2.LINE_AA)

    for idx, pt in coords.items():
        r = 5 if idx in (0, 11, 12, 23, 24) else 3
        cv2.circle(canvas, pt, r, jc, -1, cv2.LINE_AA)


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  SCREEN  BRIGHTNESS  (ESG feedback)
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
_orig_brightness: int  = 100
_brightness_set:  bool = False


def apply_brightness_feedback(bad: bool) -> None:
    """Dim screen 20 % on bad posture; restore when good. Silent on failure."""
    global _orig_brightness, _brightness_set
    if not SBC_OK:
        return
    try:
        if bad and not _brightness_set:
            _orig_brightness = sbc.get_brightness(display=0)[0]
            sbc.set_brightness(max(20, _orig_brightness - 20), display=0)
            _brightness_set = True
        elif not bad and _brightness_set:
            sbc.set_brightness(_orig_brightness, display=0)
            _brightness_set = False
    except Exception:
        pass


def restore_brightness() -> None:
    global _brightness_set
    if SBC_OK and _brightness_set:
        try:
            sbc.set_brightness(_orig_brightness, display=0)
        except Exception:
            pass
    _brightness_set = False


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  MAIN  DETECTION  LOOP
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
def run_detection(settings: dict) -> None:
    language      = settings.get("language",  "English")
    interval_mins = settings.get("interval",  60)
    privacy_mode  = settings.get("privacy",   False)
    t             = TRANSLATIONS.get(language, TRANSLATIONS["English"])

    mp_drawing, mp_pose = init_mediapipe()
    use_mp = (mp_drawing is not None and mp_pose is not None)

    cap   = init_camera()
    w_cap = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  or 1280
    h_cap = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 720

    posture_log    : list  = []
    session_start  : float = time.time()
    reminder_at    : float = session_start + interval_mins * 60.0
    break_msg_until: float = 0.0
    daily_alert_until: float = 0.0    # end timestamp for daily-reminder overlay
    daily_alert_text:  str   = ""     # reminder name to show in the overlay
    _fired_reminders: set  = set()    # id(rem) fired this session (avoids repeats)
    _bad_streak:  int  = 0            # consecutive frames with bad posture

    win_title = t["title"]
    cv2.namedWindow(win_title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win_title, min(w_cap, 1280), min(h_cap, 720))

    print(f"\n[INFO] Detection running  |  Language: {language}  "
          f"|  Interval: {interval_mins} min  |  Privacy: {privacy_mode}")
    print(f"[INFO] Press  Q  or ESC  in the video window to quit.\n")

    # ?�?� Inner loop (called with or without pose context) ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    def loop(pose_ctx=None):
        nonlocal break_msg_until, reminder_at, daily_alert_until, daily_alert_text, _bad_streak

        while True:
            ret, raw = cap.read()
            if not ret or raw is None:
                time.sleep(0.04)
                continue

            h_f, w_f = raw.shape[:2]
            now       = time.time()

            # ?�?� Smart Video Reminder ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
            if now >= reminder_at:
                url = EXERCISE_VIDEOS.get(language, EXERCISE_VIDEOS["English"])
                print(f"[BREAK] {t['break_msg']}")
                print(f"[BREAK] URL: {url}")
                webbrowser.open(url)
                break_msg_until = now + 9.0
                reminder_at     = now + interval_mins * 60.0  # schedule next

            # ?�?� Pose processing ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
            inclination = 180.0
            posture_bad = False
            coords      = {}
            status_text = t["absent"]
            result      = None
            lm_list     = None

            if use_mp and pose_ctx is not None:
                img_rgb = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
                img_rgb.flags.writeable = False
                result  = pose_ctx.process(img_rgb)
                img_rgb.flags.writeable = True

                if result.pose_landmarks:
                    lm_list = result.pose_landmarks.landmark
                    _raw_bad, inclination, coords = \
                        analyse_landmarks(lm_list, w_f, h_f)
                    # ?�?� Temporal smoothing: only flag after N consecutive frames ?�?�
                    if _raw_bad:
                        _bad_streak += 1
                    else:
                        _bad_streak = 0
                    posture_bad = _bad_streak >= _BAD_STREAK_REQUIRED
                    status_text = t["bad"] if posture_bad else t["good"]

            # ?�?� Build display frame ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
            if privacy_mode:
                # ?�?�?� PRIVACY MODE: black canvas + stickman ONLY ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
                display = np.zeros((h_f, w_f, 3), dtype=np.uint8)
                if coords:
                    draw_stickman(display, coords, posture_bad)
            else:
                # ?�?�?� NORMAL MODE: raw feed + skeleton overlay ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
                display = raw.copy()
                if use_mp and result is not None and result.pose_landmarks:
                    try:
                        mp_drawing.draw_landmarks(
                            display,
                            result.pose_landmarks,
                            mp_pose.POSE_CONNECTIONS,
                            mp_drawing.DrawingSpec(
                                color=(60, 210, 60), thickness=2, circle_radius=3),
                            mp_drawing.DrawingSpec(
                                color=(255, 195, 50), thickness=2),
                        )
                    except Exception:
                        draw_stickman(display, coords, posture_bad)

            # ?�?� ESG: screen brightness feedback ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
            apply_brightness_feedback(posture_bad)

            # ?�?� HUD ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
            neck_load = calc_neck_load(inclination)
            remaining = max(0.0, reminder_at - now)
            draw_hud(display, status_text, inclination,
                     neck_load, remaining, language, privacy_mode)

            # ?�?� Break overlay (8 s after reminder fires) ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
            if now < break_msg_until:
                msg = t["break_msg"]
                (mw, mh), _ = cv2.getTextSize(
                    msg, cv2.FONT_HERSHEY_DUPLEX, 0.80, 2)
                mx = (w_f - mw) // 2
                my = h_f // 2
                cv2.rectangle(display,
                              (mx - 18, my - mh - 16),
                              (mx + mw + 18, my + 16),
                              (0, 0, 0), -1)
                cv2.putText(display, msg, (mx, my),
                            cv2.FONT_HERSHEY_DUPLEX, 0.80,
                            (80, 240, 80), 2, cv2.LINE_AA)

            # ?�?� Daily Reminder check ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
            # Compare wall-clock HH:MM against every undone reminder once.
            _lt = time.localtime(now)
            for _rem in DAILY_REMINDERS:
                if _rem.get("done"):
                    continue
                _rid = id(_rem)
                if (_lt.tm_hour == _rem["hour"] and
                        _lt.tm_min == _rem["minute"] and
                        _rid not in _fired_reminders):
                    _fired_reminders.add(_rid)
                    daily_alert_text  = _rem["name"]
                    daily_alert_until = max(daily_alert_until, now + 9.0)
                    print(f"[REMINDER] {_rem['hour']:02d}:{_rem['minute']:02d}  "
                          f"{_rem['name']}  [{_rem['category']}]")
                    # ?�?� Native OS Toast Notification (non-blocking) ?�?�?�?�?�?�?�?�?�?�?�
                    _rem_snap = dict(_rem)   # capture values for the thread
                    def _toast(_r=_rem_snap):
                        if PLYER_OK and _plyer_notify is not None:
                            try:
                                _plyer_notify.notify(
                                    title=f"ErgoGuard  \U0001F514  {_r['category']}",
                                    message=_r["name"],
                                    app_name="ErgoGuard International",
                                    timeout=8,   # seconds before auto-dismiss
                                )
                            except Exception as _e:
                                print(f"[REMINDER-TOAST] plyer error: {_e}")
                        else:
                            print(f"[REMINDER-TOAST] (plyer not installed) "
                                  f"{_r['hour']:02d}:{_r['minute']:02d}  {_r['name']}")
                    threading.Thread(target=_toast, daemon=True).start()

            # ?�?� Daily Reminder overlay ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
            if now < daily_alert_until and daily_alert_text:
                _cat  = "Health"  # default colour for reminder overlay
                for _r2 in DAILY_REMINDERS:
                    if _r2["name"] == daily_alert_text:
                        _cat = _r2.get("category", "Health")
                        break
                _bgr  = _CAT_BGR.get(_cat, (80, 175, 76))
                _msg  = f"\U0001F514  {daily_alert_text}"
                (_mw, _mh), _ = cv2.getTextSize(
                    _msg, cv2.FONT_HERSHEY_DUPLEX, 0.80, 2)
                _mx = (w_f - _mw) // 2
                _my = h_f // 2 + 50   # offset below break overlay
                cv2.rectangle(display,
                              (_mx - 20, _my - _mh - 18),
                              (_mx + _mw + 20, _my + 18),
                              (20, 20, 20), -1)
                cv2.rectangle(display,
                              (_mx - 20, _my - _mh - 18),
                              (_mx - 14, _my + 18),
                              _bgr, -1)   # left category colour bar
                cv2.putText(display, _msg, (_mx, _my),
                            cv2.FONT_HERSHEY_DUPLEX, 0.80,
                            _bgr, 2, cv2.LINE_AA)

            # ?�?� Log ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
            ps = ("Absent" if status_text in (t["absent"], t["partial"])
                  else ("Bad" if posture_bad else "Good"))
            posture_log.append((now, inclination, ps))

            cv2.imshow(win_title, display)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q"), 27):
                break

    # ?�?� Run ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
    try:
        if use_mp:
            with mp_pose.Pose(min_detection_confidence=0.35,
                              min_tracking_confidence=0.35,
                              model_complexity=1) as pose_ctx:
                loop(pose_ctx)
        else:
            print("[WARN] MediaPipe unavailable ??running in camera-only mode.")
            loop(pose_ctx=None)
    finally:
        restore_brightness()
        cap.release()
        cv2.destroyAllWindows()

    print("\n[INFO] Session ended - generating report...")
    generate_report(posture_log, session_start, language)


# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
#  ENTRY  POINT
# ?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�?�
def main():
    settings = {}

    if TK_OK:
        root     = tk.Tk()
        app      = LauncherApp(root)
        settings = app.run()          # blocks until user clicks Start
    else:
        print("[INFO] Tkinter unavailable ??using default settings.")
        settings = {"language": "English", "interval": 60, "privacy": False}

    if not settings:
        print("[INFO] Launcher closed without starting. Goodbye.")
        return

    run_detection(settings)


if __name__ == "__main__":
    main()
oninput="?�this.value+' '+(t.min_unit||'min')"
