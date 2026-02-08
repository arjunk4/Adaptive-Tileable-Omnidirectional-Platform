import matplotlib.pyplot as plt

# Import from your existing file
from torque_and_speed import drive_torque, speed_vgrf_hgrf_dict

# -------------------------------
# Data
# -------------------------------
human_weights = [60, 70, 80, 90, 100, 110, 120]
nofunits = 10  # fixed as requested

# Speeds to plot (subset)
speeds_to_plot = [
    "0.4 m/s",
    "0.7 m/s",
    "1.0 m/s",
    "1.3 m/s",
    "1.6 m/s"
]

# -------------------------------
# Plot setup
# -------------------------------
fig, axes = plt.subplots(
    nrows=len(speeds_to_plot),
    ncols=1,
    figsize=(8, 12),
    sharex=True
)

fig.suptitle("Drive Torque vs Human Weight", fontsize=14)
fig.text(
    0.5, 0.94,
    "Ten units in contact",
    ha="center",
    fontsize=10,
    color="gray"
)
# -------------------------------
# Plot each speed
# -------------------------------
for ax, speed_label in zip(axes, speeds_to_plot):
    VGRF_multiplier = speed_vgrf_hgrf_dict[speed_label]["VGRF"]
    walking_speed = float(speed_label.split()[0])

    torques = []

    for weight in human_weights:
        torque = drive_torque(
            VGRF_multiplier=VGRF_multiplier,
            Weight=weight,
            nofunits=nofunits,
            walking_speed=walking_speed
        )
        torques.append(torque)

    ax.plot(
        human_weights,
        torques,
        marker="o",
        linewidth=1.8,
        color="black",
        label="Total Torque"
    )

    ax.set_ylabel("Torque (Nm)")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="upper left")

    # Speed annotation (top-right, like your image)
    ax.text(
        0.97, 0.90,
        speed_label,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        color="gray"
    )

# -------------------------------
# X-axis label
# -------------------------------
axes[-1].set_xlabel("Human Weight [kg]")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
