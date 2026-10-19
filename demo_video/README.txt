========================================================================
PUSHKAR SMART MOVE AI - DEMO VIDEO PRODUCTION README
========================================================================
Project: Pushkar Smart Move AI (Godavari Pushkaralu 2027, Problem Statement PS-05)
Tagline: Smarter Mobility. Safer Pilgrimages.
Video File: demo_video/final_demo.mp4

This script records the real, running application without mocking or UI faking.
It launches two coordinated browser viewports (Pilgrim View and Admin View),
drives user journeys, and renders a synchronized side-by-side demonstration.

------------------------------------------------------------------------
PREREQUISITES
------------------------------------------------------------------------
1. Python 3.10+
2. FFmpeg installed (available in PATH or via WinGet)
3. Node.js & npm
4. Python packages:
   pip install playwright requests
   python -m playwright install chromium

------------------------------------------------------------------------
HOW TO RE-RUN THE DEMO VIDEO GENERATION
------------------------------------------------------------------------
Step 1: Start Backend (Terminal 1)
   cd backend
   venv\Scripts\activate
   python -m uvicorn main:app --reload

Step 2: Start Frontend (Terminal 2)
   cd web
   npm run dev

Step 3: Run Video Recorder (Terminal 3)
   cd "c:\Users\Anushka\OneDrive\Desktop\pushkar -smart -move -ai"
   python record_demo.py

------------------------------------------------------------------------
GENERATED OUTPUT ARTIFACTS
------------------------------------------------------------------------
- demo_video/final_demo.mp4:
  1280x720 H.264 (yuv420p, 24 fps), under 10 MB, duration ~2:20 (140s).
- demo_video/cards/:
  High-definition 1280x720 title cards and scenario transitions.
- demo_video/verification_frames/:
  Extracted inspection frames across all scenes for quality audit.
- record_demo.py:
  Complete end-to-end automated driving and video production script.

------------------------------------------------------------------------
APP OBSERVATIONS & PROTOCOL COMPLIANCE
------------------------------------------------------------------------
1. "SIMULATED DATA": Displayed clearly with amber badges and caption notices.
2. Zero-Panic Crowd Diversion: Diversions remain hidden from pilgrims until
   staff physically verify on-site and click "Approve diversion".
3. SOS Prototype: Prominently warns "Prototype only. In a real emergency, call 112."
4. Multi-Lingual: Full support for English, Telugu (తెలుగు), and Hindi (हिन्दी).
   Captioned: "Telugu and Hindi texts are drafts pending native-speaker review."
5. Admin PIN / Reset: In the current codebase, Admin View opens directly without
   a PIN prompt, and backend data is restored cleanly via API at test conclusion.
========================================================================
