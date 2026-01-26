import matplotlib.pyplot as plt
import numpy as np
from trq_and_speed import drive_torque, dirn_torque2      # type: ignore

COF = 0.4                   
Weight = 115                
nofunits = 15
vgrf = 1
speed = 0           

# Walking speeds (m/s) and corresponding VGRF multipliers (BW)
nofunits = [5, 7, 9, 11, 13, 15, 17, 19]

drive_torques = []
dirn_torques = []

# ---- MAIN CALCULATION ----
for n in nofunits:
    print(f"\nCalculating for {n} units in contact...")
    drive_t = drive_torque(COF, vgrf, Weight, n, speed)
    dirn_t = dirn_torque2(COF, vgrf, Weight, n, speed)
    drive_torques.append(drive_t)
    dirn_torques.append(dirn_t)

# ---- PLOTTING ----
plt.figure(figsize=(8,5))
plt.scatter(nofunits, drive_torques, color='tab:blue', label='Drive Torque', s=70)
plt.scatter(nofunits, dirn_torques, color='tab:orange', label='Direction Torque', s=70)
plt.xticks(np.arange(3, 20, 2), np.arange(3, 20, 2))
plt.title("Torque vs # units in contact", fontsize=14)
plt.text(16, 5.3, "VGRF = 1 BW", fontsize = 9, color = 'blue')
plt.text(16, 5.0, "COF = 0.4", fontsize = 9, color = 'blue')
plt.text(16, 4.7, "Weight = 115 kg", fontsize = 9, color = 'blue')
plt.text(16, 4.4, "Negligible walking speed", fontsize = 9, color = 'blue')
plt.xlabel("# units in contact")
plt.ylabel("Torque (Nm)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
