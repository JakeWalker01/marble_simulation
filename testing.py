# ===============================
# Marble Music – Onset Test Scene
# ===============================

import librosa
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# CONFIG
# -------------------------------

AUDIO_PATH = "cartoon.wav"   # must exist in the same folder
BLENDER_FPS = 24             # only used if running inside Blender
SHOW_PLOT = True             # set False if you don't want matplotlib

# -------------------------------
# LOAD AUDIO
# -------------------------------

waveform, sample_rate = librosa.load(AUDIO_PATH, sr=None)

# -------------------------------
# ONSET DETECTION
# -------------------------------

onset_frames = librosa.onset.onset_detect(
    y=waveform,
    sr=sample_rate
)

onset_times = librosa.frames_to_time(
    onset_frames,
    sr=sample_rate
)

print(f"Detected {len(onset_times)} onsets")
print("First 10 onset times (seconds):")
print(onset_times[:10])

# -------------------------------
# WAVEFORM VISUALIZATION
# -------------------------------

if SHOW_PLOT:
    time_axis = np.arange(len(waveform)) / sample_rate

    plt.figure(figsize=(14, 4))
    plt.plot(time_axis, waveform, alpha=0.6)

    for t in onset_times:
        plt.axvline(t, color="red", alpha=0.25)

    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Waveform with Detected Onsets")
    plt.tight_layout()
    plt.show()

# -------------------------------
# BLENDER TIMELINE MARKERS
# -------------------------------

try:
    import bpy

    scene = bpy.context.scene
    fps = scene.render.fps

    print(f"Running inside Blender (FPS = {fps})")

    # Optional: clear existing markers
    scene.timeline_markers.clear()

    for t in onset_times:
        frame = int(t * fps)
        scene.timeline_markers.new(
            name="Onset",
            frame=frame
        )

    print(f"Added {len(onset_times)} timeline markers")

except ImportError:
    print("Not running inside Blender — skipping timeline markers")
