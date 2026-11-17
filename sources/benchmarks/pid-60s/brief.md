# Brief: pid-60s

Frozen once the first result is recorded. Give this text to the agent exactly as written.

---

Make a 60-second narrated explainer video, 16:9 at 1080p, in English, for beginners who are
building their first robot.

Topic: what a PID controller does, using one example throughout: a DC motor that must hold a
wheel at 120 RPM when a load is added.

It must:

1. Open with the problem in the first 3 seconds: the wheel slows down when the load arrives.
2. Show P alone, then P + I, then P + I + D, each as a step-response plot of speed against time.
   The plots must be computed from a simple motor model in the scene code, not drawn by hand.
3. Name the three effects in plain words: P reacts to the error now, I removes the error left over,
   D damps the overshoot.
4. End with one tuning tip: raise P until it oscillates, back off, then add I, then a little D.
5. Use readable text on a phone, keep music under the voice, and end on a frame that shows the
   whole idea.

Make the video with explainroo and follow the video-director skill for planning and checks.
