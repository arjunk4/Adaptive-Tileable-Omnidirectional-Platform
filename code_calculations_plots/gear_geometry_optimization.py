import math
import matplotlib.pyplot as plt

# -------------------------------------------------
# Geometry constraints
# -------------------------------------------------
CENTER_DISTANCE = 23.27          # mm
MIN_MODULE = 0.7
MAX_GEAR2_OUTER_DIAMETER = 11.93   # mm
MIN_GEAR2_OUTER_DIAMETER = 6.5
MAX_GEAR1_OUTER_DIAMETER = 39.3   # mm

MAX_TEETH_1 = 150
MAX_TEETH_2 = 30

# -------------------------------------------------
# AGMA / material parameters
# -------------------------------------------------
J = 0.2                 # geometry factor
b = 7.0                 # face width (mm)
sigma_allow = 70.0      # MPa = N/mm^2

# -------------------------------------------------
# Enumerate feasible gear sets
# -------------------------------------------------
gear_sets = []  # index → parameters

for z2 in range(2, MAX_TEETH_2 + 1):
    for z1 in range(2, MAX_TEETH_1 + 1):

        m = (2 * CENTER_DISTANCE) / (z1 + z2)
        if m < MIN_MODULE:
            continue

        d_o2 = m * (z2 + 2)
        if not (MIN_GEAR2_OUTER_DIAMETER < d_o2 <= MAX_GEAR2_OUTER_DIAMETER):
            continue

        d_o1 = m * (z1 + 2)
        if d_o1 > MAX_GEAR1_OUTER_DIAMETER:
            continue

        d1 = m * z1  # pitch diameter of gear 1 (mm)

        gear_sets.append({
            "z1": z1,
            "z2": z2,
            "module": m,
            "pitch_diameter_mm": d1,
            "gear2_outer_diameter_mm": d_o2,
            "gear1_outer_diameter_mm": (m * (z1 + 2)),
        })

if not gear_sets:
    print("No valid gear sets found.")
else: 
    # -------------------------------------------------
    # Compute maximum allowable torque
    # -------------------------------------------------
    set_index = []
    max_torque = []  # N·m

    for i, g in enumerate(gear_sets, start=1):

        m = g["module"]
        d = g["pitch_diameter_mm"]

        # AGMA bending-limited tangential load
        Wt = sigma_allow * b * m * J      # N

        # Torque capacity
        T_Nmm = Wt * d / 2                # N·mm
        T_Nm = T_Nmm / 1000.0             # N·m

        set_index.append(i)
        max_torque.append(T_Nm)

        # Map set number → torque
        g["max_allowable_torque_Nm"] = T_Nm

    # -------------------------------------------------
    # Normalization
    # -------------------------------------------------
    m_vals = [g["module"] for g in gear_sets]
    d_vals = [g["gear2_outer_diameter_mm"] for g in gear_sets]
    T_vals = [g["max_allowable_torque_Nm"] for g in gear_sets]

    m_min, m_max = min(m_vals), max(m_vals)
    d_min, d_max = min(d_vals), max(d_vals)
    T_min, T_max = min(T_vals), max(T_vals)

    def norm(x, xmin, xmax):
        return (x - xmin) / (xmax - xmin)

    PRIORITY_MODULE = 3.0
    PRIORITY_OUTERDIA = 2.0

    best_set = None
    best_C = -float("inf")

    for g in gear_sets:
        C = (
            PRIORITY_MODULE * norm(g["module"], m_min, m_max)
            - PRIORITY_OUTERDIA * norm(g["gear2_outer_diameter_mm"], d_min, d_max)
            + norm(g["max_allowable_torque_Nm"], T_min, T_max)
        )
        g["cost_function"] = C

        if C > best_C:
            best_C = C
            best_set = g

    print("\nSummary:")
    print(f"Number of feasible gear sets: {len(gear_sets)}")
    print("\nBest gear set (normalized cost function):")
    #print(f"C = {best_C:.4f}")
    print(
        f"z1 = {best_set['z1']}, "
        f"z2 = {best_set['z2']}, "
        f"module = {best_set['module']:.4f} mm, "
        f"T_max = {best_set['max_allowable_torque_Nm']:.3f} N·m, "
        f"d_o2 = {best_set['gear2_outer_diameter_mm']:.2f} mm, "
        f"d_o1 = {best_set['gear1_outer_diameter_mm']:.2f} mm"
    )

    '''
    # -------------------------------------------------
    # Mapping output
    # -------------------------------------------------
    print("Set number → gear parameters:\n")
    for i, g in enumerate(gear_sets, start=1):
        print(
            f"Set {i:2d}: "
            f"z1={g['z1']:3d}, "
            f"z2={g['z2']:2d}, "
            f"m={g['module']:.4f} mm, "
            f"T_max={g['max_allowable_torque_Nm']:.3f} N·m, "
            f"d_o2={g['gear2_outer_diameter_mm']:.2f} mm, "
            f"d_o1={g['gear1_outer_diameter_mm']:.2f} mm"
        )

    # -------------------------------------------------
    # Scatter plot
    # -------------------------------------------------
    plt.figure()
    plt.scatter(set_index, max_torque)
    plt.xlabel("Gear set number")
    plt.ylabel("Maximum allowable torque (N·m)")
    plt.title("AGMA Bending-Limited Maximum Torque vs Gear Set")
    plt.grid(True)
    plt.show()
    '''
