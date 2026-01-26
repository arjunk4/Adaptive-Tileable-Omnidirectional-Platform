# Code for plotting fos and life of a single bearing

'''
import numpy as np
import matplotlib.pyplot as plt
from bearing_calcs import static_fos_71805, dynamic_life_71805  # type: ignore

# Constants
g = 9.81
FOS_THRESHOLD = 1.5
LIFE_THRESHOLD = 1e5  # 100,000 hours

# Fixed RPM and number of bearing units
RPM = 100
units_fixed = 1

# Bearing ratings (Angular contact 71805)
C0_angular = 3050  # N
C10_angular = 5720  # N

# Speeds (only upto 1.6 m/s)
speed_vgrf_dict = {
    "0.4 m/s": {"VGRF": 1.0},
    "0.7 m/s": {"VGRF": 1.0},
    "1.0 m/s": {"VGRF": 1.1},
    "1.3 m/s": {"VGRF": 1.3},
    "1.6 m/s": {"VGRF": 1.4},
}

# Human weights
human_weights = [60, 70, 80, 90, 100, 110, 120]

# Collecting results
results = []

for speed, values in speed_vgrf_dict.items():
    VGRF_value = values["VGRF"]
    for weight in human_weights:
        fos = static_fos_71805(
            VGRF_factor=VGRF_value,
            Weight=weight,
            nofunits=units_fixed,
            static_load_rating=C0_angular,
        )
        life = dynamic_life_71805(
            VGRF_factor=VGRF_value,
            Weight=weight,
            nofunits=units_fixed,
            dynamic_load_rating=C10_angular,
        )
        results.append({
            "speed": speed,
            "weight": weight,
            "fos": fos,
            "life_hours": life,
        })

# Plot setup
speed_list = list(speed_vgrf_dict.keys())
n_rows = len(speed_list)
fig, axes = plt.subplots(n_rows, 2, figsize=(12, 3.2 * n_rows), sharex='col')
axes = np.atleast_2d(axes)

legend_added_fos = False
legend_added_life = False

for i, speed in enumerate(speed_list):
    subset = [r for r in results if r["speed"] == speed]
    weights = np.array([r["weight"] for r in subset])
    fos = np.array([r["fos"] for r in subset])
    life = np.array([r["life_hours"] for r in subset])

    critical_fos = fos <= FOS_THRESHOLD
    # critical_life = life < LIFE_THRESHOLD

    # --- Static FOS plot ---
    ax_fos = axes[i, 0]
    ax_fos.plot(weights, fos, color='blue')
    ax_fos.plot(weights[~critical_fos], fos[~critical_fos], marker='o', color='blue', linestyle='None')
    ax_fos.scatter(weights[critical_fos], fos[critical_fos], s=70, facecolors='red', edgecolors='none', zorder=5)
    ax_fos.axhline(1, linestyle='--', linewidth=1, color='gray')
    ax_fos.set_ylabel("Static FOS")
    ax_fos.grid(True)
    ax_fos.text(0.98, 0.8, speed, transform=ax_fos.transAxes, fontsize=8, color='dimgray', ha='right')

    if not legend_added_fos:
        ax_fos.plot([], [], color='blue', label='FOS')
        ax_fos.plot([], [], marker='o', linestyle='', color='red', label='Critical (≤1.5)')
        ax_fos.legend(loc='upper right', fontsize=8)
        legend_added_fos = True

    # --- Dynamic Life plot ---
    ax_life = axes[i, 1]
    ax_life.plot(weights, life, color='orange')
    ax_life.scatter(weights, life, s=70, facecolors='orange', edgecolors='none', zorder=5)
    # ax_life.plot(weights[~critical_life], life[~critical_life], marker='o', color='orange', linestyle='None')
    # ax_life.scatter(weights[critical_life], life[critical_life], s=70, facecolors='red', edgecolors='none', zorder=5)
    ax_life.set_ylabel("Life (hours)")
    ax_life.grid(True)
    ax_life.text(0.98, 0.8, speed, transform=ax_life.transAxes, fontsize=8, color='dimgray', ha='right')

    if not legend_added_life:
        ax_life.plot([], [], color='orange', label='Life')
        # ax_life.plot([], [], marker='o', linestyle='', color='red', label='Critical (<100k h)')
        ax_life.legend(loc='upper right', fontsize=8)
        legend_added_life = True

    # Find and annotate minimum life
    min_life = np.min(life)
    min_weight = weights[np.argmin(life)]

    ax_life.text(
        0.98, 0.15, 
        f"Min: {min_life:.1e} h", 
        transform=ax_life.transAxes,
        fontsize=7, 
        color='black',
        ha='right'
    )


# X-label shared only on the bottom row
axes[-1, 0].set_xlabel("Weight [kg]")
axes[-1, 1].set_xlabel("Weight [kg]")

plt.suptitle("Angular Contact Bearing 71904: Static FOS and Life vs Weight    (100 RPM, Units = 1)", y=0.995)
plt.tight_layout()
plt.show()

'''



# Code for comparing bearings


import numpy as np
import matplotlib.pyplot as plt
from bearing_calcs import static_fos_71805, dynamic_life_71805  # type: ignore

# Engineering constants
g = 9.81
RPM = 100
FOS_THRESHOLD = 1.5
# LIFE_THRESHOLD = 1e5  # hours
units_fixed = 1  # Fixed number of bearings in contact

# Bearing definitions: (name, C0 (N), C10 (N), y0, y2)
bearings = [
    ("71805", 3050, 3900, 0.38, 0.87),
    ("71904", 3050, 5720, 0.38, 0.87),
    ("7301", 5000, 10600, 0.26, 0.57),
]

# Speed values (up to 1.6 m/s only)
speed_vgrf_dict = {
    "0.4 m/s": {"VGRF": 1.0},
    "0.7 m/s": {"VGRF": 1.0},
    "1.0 m/s": {"VGRF": 1.1},
    "1.3 m/s": {"VGRF": 1.3},
    "1.6 m/s": {"VGRF": 1.4},
}

# Human weights
human_weights = [60, 70, 80, 90, 100, 110, 120]


# --- Plot for each speed ---
for speed, values in speed_vgrf_dict.items():
    VGRF_value = values["VGRF"]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharex=True)
    ax_fos, ax_life = axes

    for name, C0, C10, y0, y2 in bearings:
        fos_vals = []
        life_vals = []

        for weight in human_weights:
            fos = static_fos_71805(VGRF_value, weight, units_fixed, C0, y0)
            life = dynamic_life_71805(VGRF_value, weight, units_fixed, C10, y2)

            fos_vals.append(fos)
            life_vals.append(life)

        fos_vals = np.array(fos_vals)
        life_vals = np.array(life_vals)

        # Plot FOS
        ax_fos.plot(human_weights, fos_vals, marker='o', label=f"FOS - {name}")
        critical_fos = fos_vals <= FOS_THRESHOLD
        ax_fos.scatter(
            np.array(human_weights)[critical_fos],
            fos_vals[critical_fos],
            color='red',
            s=70,
            zorder=5,
        )

        # Plot LIFE
        ax_life.plot(human_weights, life_vals, marker='o', label=f"Life - {name}")
        # critical_life = life_vals < LIFE_THRESHOLD
        '''ax_life.scatter(
            np.array(human_weights)[critical_life],
            life_vals[critical_life],
            color='red',
            s=70,
            zorder=5,
        )'''

    # Formatting FOS plot
    ax_fos.set_title("Static FOS")
    ax_fos.set_ylabel("FOS")
    ax_fos.axhline(1, linestyle='--', color='gray', linewidth=1)
    ax_fos.text(0.97, 0.92, speed, transform=ax_fos.transAxes, fontsize=9, ha='right')
    ax_fos.grid(True)

    # Formatting LIFE plot
    ax_life.set_title("Dynamic Life (hours)")
    ax_life.text(0.97, 0.92, speed, transform=ax_life.transAxes, fontsize=9, ha='right')
    ax_life.grid(True)

    ax_fos.set_xlabel("Weight [kg]")
    ax_life.set_xlabel("Weight [kg]")

    # Legend
    handles, labels = ax_life.get_legend_handles_labels()
    fig.legend(
    handles, labels,
    loc='lower center',
    bbox_to_anchor=(0.5, 0.01),
    ncol=3,
    fontsize=9)


    plt.suptitle(f"Bearing Comparison at {speed} – Units = {units_fixed}\n(Static FOS & Life vs Weight)", fontsize=11)
    plt.tight_layout(rect=[0, 0.05, 1, 0.93])
    plt.show()
