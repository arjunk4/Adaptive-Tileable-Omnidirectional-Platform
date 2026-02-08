import math

# -------------------------------
# Given constraints
# -------------------------------
CENTER_DISTANCE = 28.85        # mm
PRESSURE_ANGLE = 20            # degrees
CLEARANCE = 0.05               # mm
MIN_MODULE = 0.6
MAX_GEAR2_OUTER_DIAMETER = 7.3   # mm (adjusted to match real geometry)

# Search limits
MAX_TEETH_1 = 150
MAX_TEETH_2 = 20
MIN_GEAR2_OUTER_DIAMETER = 6.5   # mm

solutions = []

# Sweep integer tooth counts
for z2 in range(6, MAX_TEETH_2 + 1):
    for z1 in range(4, MAX_TEETH_1 + 1):

        # Compute exact module to satisfy center distance
        m = (2 * CENTER_DISTANCE) / (z1 + z2)

        if m < MIN_MODULE:
            continue

        # Gear 2 outer diameter
        d_o2 = m * (z2 + 2)
        if d_o2 > MAX_GEAR2_OUTER_DIAMETER or d_o2 <= MIN_GEAR2_OUTER_DIAMETER:
            continue

        # Diameters
        d1 = m * z1
        d2 = m * z2
        d_o1 = m * (z1 + 2)

        solutions.append({
            "z1": z1,
            "z2": z2,
            "module": round(m, 4),
            #"gear1_pitch_dia": round(d1, 3),
            #"gear2_pitch_dia": round(d2, 3),
            #"gear1_outer_dia": round(d_o1, 3),
            "gear2_outer_dia": round(d_o2, 3)
        })

# -------------------------------
# Output results
# -------------------------------
if not solutions:
    print("No valid gear sets found.")
else:
    print(f"Found {len(solutions)} valid gear set(s):\n")
    for s in solutions:   # print first 20 to keep output sane
        print(s)
