import bpy
import numpy as np
import csv
from pathlib import Path

# ============================================================
# POSER - Blender Camera Path -> Subsurface Dive Log Exporter
# ============================================================
#
# Exports the active camera animation as a CSV dive profile
# compatible with Subsurface.
#
# HOW TO USE:
# 1. Select the animated camera
# 2. Open Blender Text Editor
# 3. Paste and run this script
# 4. Import generated CSV into Subsurface
#
# ============================================================

# -----------------------------
# USER SETTINGS
# -----------------------------

OUTPUT_FILE = str(Path.home() / "POSER_to_SUBSURFACE_export.csv")

DIVE_NUMBER = 5000
DIVE_DATE = "2024-01-15"
DIVE_TIME = "00:00:00"

START_DEPTH_M = 15.0

# Diver horizontal movement speed (m/s)
SWIM_SPEED_M_S = 0.25

# Descent / ascent rates
DESCENT_RATE_M_MIN = 18.0
ASCENT_RATE_M_MIN = 9.0

# Safety stop
SAFETY_STOP_DEPTH_M = 6.0
SAFETY_STOP_DURATION_SEC = 180

# ------------------------------------------------------------
# VALIDATION
# ------------------------------------------------------------

camera = bpy.context.active_object

if camera is None:
    raise Exception("No active object selected.")

if camera.type != 'CAMERA':
    raise Exception("Active object must be a camera.")

scene = bpy.context.scene

print("====================================")
print("POSER Exporter")
print("Camera:", camera.name)
print("Frames:", scene.frame_start, "->", scene.frame_end)
print("Output:", OUTPUT_FILE)
print("====================================")

# ------------------------------------------------------------
# INITIALIZE
# ------------------------------------------------------------

scene.frame_set(scene.frame_start)

mw = camera.matrix_world
x0, y0, z0 = mw.to_translation()

initial_position = np.array([x0, y0, z0])

current_time_sec = 0.0

# ------------------------------------------------------------
# CSV OUTPUT
# ------------------------------------------------------------

with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:

    writer = csv.writer(f)

    # Subsurface CSV header
    writer.writerow([
        "dive number",
        "date",
        "time",
        "sample time (min)",
        "sample depth (m)",
        "sample temperature (C)",
        "sample pressure (bar)",
        "sample heartrate"
    ])

    # --------------------------------------------------------
    # DESCENT TO START DEPTH
    # --------------------------------------------------------

    descent_time_sec = START_DEPTH_M / DESCENT_RATE_M_MIN * 60.0

    current_time_sec += descent_time_sec

    writer.writerow([
        DIVE_NUMBER,
        DIVE_DATE,
        DIVE_TIME,
        f"{int(current_time_sec // 60):02d}:{int(current_time_sec % 60):02d}",
        f"{START_DEPTH_M:.1f}",
        "",
        "",
        ""
    ])

    previous_position = initial_position
    current_depth = START_DEPTH_M

    # --------------------------------------------------------
    # CAMERA PATH SAMPLING
    # --------------------------------------------------------

    for frame in range(scene.frame_start + 1, scene.frame_end + 1):

        scene.frame_set(frame)

        mw = camera.matrix_world
        x, y, z = mw.to_translation()

        current_position = np.array([x, y, z])

        # Distance traveled since previous frame
        distance_m = np.linalg.norm(current_position - previous_position)

        previous_position = current_position

        # Time increment from diver speed
        delta_time_sec = distance_m / SWIM_SPEED_M_S

        current_time_sec += delta_time_sec

        # Blender Z-up -> depth positive downward
        current_depth = START_DEPTH_M + (z0 - z)

        # Prevent negative depth
        current_depth = max(0.0, current_depth)

        writer.writerow([
            DIVE_NUMBER,
            DIVE_DATE,
            DIVE_TIME,
            f"{int(current_time_sec // 60):02d}:{int(current_time_sec % 60):02d}",
            f"{current_depth:.1f}",
            "",
            "",
            ""
        ])

        print(
            f"Frame {frame:04d} | "
            f"Depth {current_depth:5.1f} m | "
            f"Distance {distance_m:5.2f} m | "
            f"Time {current_time_sec:6.1f} s"
        )

    # --------------------------------------------------------
    # ASCENT TO SAFETY STOP
    # --------------------------------------------------------

    if current_depth > SAFETY_STOP_DEPTH_M:

        ascent_distance = current_depth - SAFETY_STOP_DEPTH_M

        ascent_time_sec = (
            ascent_distance / ASCENT_RATE_M_MIN
        ) * 60.0

        current_time_sec += ascent_time_sec

        current_depth = SAFETY_STOP_DEPTH_M

        writer.writerow([
            DIVE_NUMBER,
            DIVE_DATE,
            DIVE_TIME,
            f"{int(current_time_sec // 60):02d}:{int(current_time_sec % 60):02d}",
            f"{current_depth:.1f}",
            "",
            "",
            ""
        ])

    # --------------------------------------------------------
    # SAFETY STOP
    # --------------------------------------------------------

    current_time_sec += SAFETY_STOP_DURATION_SEC

    writer.writerow([
        DIVE_NUMBER,
        DIVE_DATE,
        DIVE_TIME,
        f"{int(current_time_sec // 60):02d}:{int(current_time_sec % 60):02d}",
        f"{SAFETY_STOP_DEPTH_M:.1f}",
        "",
        "",
        ""
    ])

    # --------------------------------------------------------
    # FINAL ASCENT TO SURFACE
    # --------------------------------------------------------

    final_ascent_time_sec = (
        SAFETY_STOP_DEPTH_M / ASCENT_RATE_M_MIN
    ) * 60.0

    current_time_sec += final_ascent_time_sec

    writer.writerow([
        DIVE_NUMBER,
        DIVE_DATE,
        DIVE_TIME,
        f"{int(current_time_sec // 60):02d}:{int(current_time_sec % 60):02d}",
        "0.0",
        "",
        "",
        ""
    ])

print("====================================")
print("Export completed.")
print("CSV saved to:")
print(OUTPUT_FILE)
print("====================================")

