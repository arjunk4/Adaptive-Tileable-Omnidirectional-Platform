import numpy as np  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
from bearing_calcs import bearing_dynamic_life, bearing_static_fos, bearing_frictional_torque  # type: ignore

# Engineering Constants
g = 9.81
cos10 = 0.9848
sin10 = 0.17365
RPM = 500
REV_TO_HOURS = 1 / (60 * RPM)

# Bearing Properties
C0_control = 5500
C10_control = 9800
f0_control = 1.3
C0_drive = 6500
C10_drive = 11000
f0_drive = 1.1

# Input Data
speed_vgrf_dict = {
    "0.4 m/s": {"VGRF": 1.0},
    "0.7 m/s": {"VGRF": 1.0},
    "1.0 m/s": {"VGRF": 1.1},
    "1.3 m/s": {"VGRF": 1.3},
    "1.6 m/s": {"VGRF": 1.4},
    "3.0 m/s": {"VGRF": 2.4},
    "3.33 m/s": {"VGRF": 2.8},
    "3.9 m/s": {"VGRF": 3.0},
    "4.4 m/s": {"VGRF": 3.2},
}

# Filter speeds to ≤ 1.6 m/s
speed_vgrf_dict = {k: v for k, v in speed_vgrf_dict.items() if float(k.split()[0]) <= 1.6}

human_weights = [60, 70, 80, 90, 100, 110, 120]
units_fixed = 15  # Keep number of units fixed

# Threshold conditions
LIFE_THRESHOLD = 8_640  # hours
FOS_THRESHOLD = 1.5

'''
# Calculations
results = []
for speed, values in speed_vgrf_dict.items():
    VGRF_value = values["VGRF"]
    for weight in human_weights:
        dynamic_life = bearing_dynamic_life(
            VGRF=VGRF_value, Weight=weight, nofunits=units_fixed,
            dynamic_load_rating_control=C10_control,
            dynamic_load_rating_drive=C10_drive,
            static_load_rating_control=C0_control,
            static_load_rating_drive=C0_drive,
            calculation_factor_control=f0_control,
            calculation_factor_drive=f0_drive
        )
        static_fos = bearing_static_fos(
            VGRF_factor=VGRF_value, Weight=weight, nofunits=units_fixed,
            static_load_rating_drive=C0_drive,
            static_load_rating_control=C0_control
        )

        results.append({
            "speed": speed,
            "weight": weight,
            "drive_life_hours": dynamic_life["drive_life_revs"] * REV_TO_HOURS,
            "control_life_hours": dynamic_life["control_life_revs"] * REV_TO_HOURS,
            "drive_fos": static_fos["drive_fos"],
            "control_fos": static_fos["control_fos"]
        })

# Plot setup
speed_list = list(speed_vgrf_dict.keys())
n_rows = len(speed_list)
fig, axes = plt.subplots(n_rows, 2, figsize=(12, 2.8 * n_rows), sharex='col')
axes = np.atleast_2d(axes)

legend_added_fos = False
legend_added_life = False

# Plotting
for i, speed in enumerate(speed_list):
    subset = [r for r in results if r["speed"] == speed]
    weights = np.array([r["weight"] for r in subset])

    drive_fos = np.array([r["drive_fos"] for r in subset])
    control_fos = np.array([r["control_fos"] for r in subset])
    drive_life = np.array([r["drive_life_hours"] for r in subset])
    control_life = np.array([r["control_life_hours"] for r in subset])

    # Critical points
    critical_fos = (drive_fos <= FOS_THRESHOLD) | (control_fos <= FOS_THRESHOLD)
    critical_life = (drive_life < LIFE_THRESHOLD) | (control_life < LIFE_THRESHOLD)

    # ===== STATIC FOS =====
    ax_fos = axes[i, 0]
    ax_fos.plot(weights, drive_fos, color='orange')
    ax_fos.plot(weights, control_fos, color='blue')
    ax_fos.scatter(weights[~critical_fos], drive_fos[~critical_fos], marker='o', color='orange')
    ax_fos.scatter(weights[~critical_fos], control_fos[~critical_fos], marker='s', color='blue')
    ax_fos.scatter(weights[critical_fos], np.minimum(drive_fos[critical_fos], control_fos[critical_fos]),
                   s=70, facecolors='red', edgecolors='none', zorder=5)
    ax_fos.axhline(1, linestyle='--', linewidth=1, color='red')
    ax_fos.set_ylabel("Static FOS")
    ax_fos.grid(True)

    ax_fos.text(0.98, 0.8, speed, transform=ax_fos.transAxes, fontsize=8, color='dimgray', ha='right')

    if not legend_added_fos:
        ax_fos.plot([], [], color='orange', label='Drive FOS')
        ax_fos.plot([], [], color='blue', label='Control FOS')
        ax_fos.plot([], [], marker='o', color='red', linestyle='', label='Crit. (≤ 1.5)')
        ax_fos.legend(loc='upper right', fontsize=8)
        legend_added_fos = True

    # ===== DYNAMIC LIFE =====
    ax_life = axes[i, 1]
    ax_life.plot(weights, drive_life, color='orange')
    ax_life.plot(weights, control_life, color='blue')
    ax_life.scatter(weights[~critical_life], drive_life[~critical_life], marker='o', color='orange')
    ax_life.scatter(weights[~critical_life], control_life[~critical_life], marker='s', color='blue')
    ax_life.scatter(weights[critical_life], np.minimum(drive_life[critical_life], control_life[critical_life]),
                    s=70, facecolors='red', edgecolors='none', zorder=5)
    ax_life.set_ylabel("Life [hours]")
    ax_life.grid(True)

    ax_life.text(0.98, 0.8, speed, transform=ax_life.transAxes, fontsize=8, color='dimgray', ha='right')

    if not legend_added_life:
        ax_life.plot([], [], color='orange', label='Drive Life')
        ax_life.plot([], [], color='blue', label='Control Life')
        ax_life.plot([], [], marker='o', color='red', linestyle='', label='Crit. (< 8640 h)')
        ax_life.legend(loc='upper right', fontsize=8)
        legend_added_life = True

# Final formatting
axes[-1, 0].set_xlabel("Weight [kg]")
axes[-1, 1].set_xlabel("Weight [kg]")

plt.suptitle(f"Bearing Static FOS & Dynamic Life vs Weight (Units in contact = {units_fixed}, at 500 RPM)", fontsize=11, y=0.995)
plt.tight_layout()
plt.show()
'''

results = []

for speed, values in speed_vgrf_dict.items():
    VGRF_value = values["VGRF"]

    for weight in human_weights:
        Fe = bearing_frictional_torque(
            VGRF=VGRF_value,
            Weight=weight,
            nofunits=units_fixed,
            static_load_rating_control=C0_control,
            static_load_rating_drive=C0_drive,
            calculation_factor_control=f0_control,
            calculation_factor_drive=f0_drive
        )

        results.append({
            "speed": speed,
            "weight": weight,
            "Drive Bearing friction": Fe["Drive Bearing friction"],
            "Direction Bearing friction": Fe["Direction Bearing friction"]
        })

speed_list = list(speed_vgrf_dict.keys())
n_rows = len(speed_list)

fig, axes = plt.subplots(n_rows, 1, figsize=(8, 2.5 * n_rows), sharex=True)
axes = np.atleast_1d(axes)

legend_added = False

for i, speed in enumerate(speed_list):
    subset = [r for r in results if r["speed"] == speed]

    weights = np.array([r["weight"] for r in subset])
    drive_fr = np.array([r["Drive Bearing friction"] for r in subset])
    control_fr = np.array([r["Direction Bearing friction"] for r in subset])

    total_fr_unit = drive_fr + control_fr
    if units_fixed > 7:
        total_fr = total_fr_unit * 7
    else:
        total_fr = total_fr_unit * units_fixed

    ax = axes[i]
    #ax.plot(weights, drive_fr, color='orange')
    #ax.plot(weights, control_fr, color='blue')
    #ax.plot(weights, total_fr_unit, color='black', linestyle='--')
    ax.plot(weights, total_fr, color='black', linestyle='-')

    #ax.scatter(weights, drive_fr, color='orange', marker='o')
    #ax.scatter(weights, control_fr, color='blue', marker='s')
    #ax.scatter(weights, total_fr_unit, color='black', marker='^')
    ax.scatter(weights, total_fr, color='black', marker='o')
    ax.set_ylabel("Torque (Nm)")
    ax.grid(True)

    ax.text(0.98, 0.85, speed, transform=ax.transAxes,
            ha='right', va='top', fontsize=8, color='dimgray')

    if not legend_added:
        #ax.plot([], [], color='orange', label='Drive bearing')
        #ax.plot([], [], color='blue', label='Control bearing')
        #ax.plot([], [], color='black', linestyle='--', label='Torque per unit')
        ax.plot([], [], color='black', linestyle='-', label='Total Torque')
        ax.legend(fontsize=8)
        legend_added = True

axes[-1].set_xlabel("Human Weight [kg]")

plt.suptitle(
    f"Total Frictional Torque vs Weight   "
    f"(Units in contact = {units_fixed})",
    fontsize=11,
    y = 0.98
)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
