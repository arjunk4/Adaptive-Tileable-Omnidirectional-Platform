import numpy as np

g = 9.81                                                                            # m/s²
r = 0.019                                                                           # m (radius of drive disk)
pi = 3.1416
sin_10 = 0.1736
sin_10_square = 0.03015                                                             # sin(10°)²
cos_10 = 0.9848                                                                     # cos(10°)
cof = 0.35                                                                          # coefficient of friction

speed_vgrf_hgrf_dict = {
    "0.4 m/s":  {"VGRF": 1.0,  "HGRF": cof * 1.0},
    "0.7 m/s":  {"VGRF": 1.0,  "HGRF": cof * 1.0},
    "1.0 m/s":  {"VGRF": 1.1,  "HGRF": cof * 1.1},
    "1.3 m/s":  {"VGRF": 1.3,  "HGRF": cof * 1.3},
    "1.6 m/s":  {"VGRF": 1.4,  "HGRF": cof * 1.4},
    "3.0 m/s":  {"VGRF": 2.4,  "HGRF": cof * 2.4},
    "3.33 m/s": {"VGRF": 2.8,  "HGRF": cof * 2.8},
    "3.9 m/s":  {"VGRF": 3.0,  "HGRF": cof * 3.0},
    "4.4 m/s":  {"VGRF": 3.2,  "HGRF": cof * 3.2}
}

human_weights = [60, 70, 80, 90, 100, 110, 120]
infill_percentages = [30, 40, 50, 60, 70, 80, 90, 100]
nof_units_in_contact = [1, 2, 3, 4, 5, 6, 7, 10, 13, 15, 18]

def iteration():
    for infill in infill_percentages:
        print(f"\n=== INFILL {infill}% ===")

        for units in nof_units_in_contact:
            print(f"\n--- Units in Contact: {units} ---")

            # ---- VGRF loop ----
            print("\n[VGRF Iteration]")
            for speed, grfs in speed_vgrf_hgrf_dict.items():
                vgrf = grfs["VGRF"]

                print(f"\nSpeed: {speed} | VGRF: {vgrf}")
                for weight in human_weights:
                    print(f"  Weight {weight} kg → use VGRF = {vgrf}")

            # ---- HGRF loop ----
            print("\n[HGRF Iteration]")
            for speed, grfs in speed_vgrf_hgrf_dict.items():
                hgrf = grfs["HGRF"]

                print(f"\nSpeed: {speed} | HGRF: {hgrf}")
                for weight in human_weights:
                    print(f"  Weight {weight} kg → use HGRF = {hgrf}")


def vertical_force(walk_speed, VGRF_multiplier, Weight_in_kg, nofunits):
    weight_in_N = Weight_in_kg * g

    VGRF = VGRF_multiplier * weight_in_N
    print(f"Vertical Ground Reaction Force for {walk_speed} m/s is {VGRF:.3f} N")

    force_per_unit = VGRF / nofunits
    print(f"VGRF per unit is {force_per_unit:.3f} N")
    
    return None

def drive_torque(VGRF_multiplier, Weight, nofunits, walking_speed, COF = cof):
    cell_internal_inertia = 0.018                                                   # To rotate all 7 disks, in Nm
    gratio = 20/26
    weight_in_N = Weight * g
    VGRF = VGRF_multiplier * weight_in_N

    HGRF = COF * VGRF
    print(f"Total HGRF: {HGRF:.3f} N")

    HGRF_onedisk = HGRF / nofunits
    print(f"HGRF on one disk: {HGRF_onedisk:.3f} N")

    t_in_ujoint = HGRF_onedisk * r
    t_out_ujoint = t_in_ujoint * ((1 - sin_10_square) / cos_10)                     # Torque out of U-joint assumiung maximum loss of power
    torque_drivetransmission = t_out_ujoint

#   disk_ang_accel = torque_drivetransmission / (0.1 * (r ** 2) * 0.5)              # Disk moment of inertia = m*r^2; m = 100 g assumed for calc
#   print(f"Disk angular acceleration: {disk_ang_accel:.3f} rad/s² = {(disk_ang_accel * ((60 ** 2)/ (2 * pi))):.3f} rev/min² = {(disk_ang_accel / (2 * pi)):.3f} rev/s²")

    if nofunits > 7:
        torque_drivegear = torque_drivetransmission * gratio * 7
    else:
        torque_drivegear = torque_drivetransmission * gratio * nofunits

    total_torque = torque_drivegear + cell_internal_inertia
    print(f"Drive Motor's torque at {walking_speed:.3f} m/s: {total_torque:.3f} Nm = {(total_torque * 10.1972):.3f} kg cm")
    
    return total_torque



''' 
    Drive inertia calc:
    Torque with nothing on tiles: 0.36 kg cm
    No-load torque: 0.18 kg cm
    So torque read to overcome inertia of components: 0.18 kg cm
'''



def drive_speed(walkspeed):
    ang_velo = walkspeed / r
    sratio = 26 / 20

    w_in_ujoint = ang_velo * (60 / (2 * pi))
    rpm_drivetransmission = w_in_ujoint * ((cos_10) / (1 - sin_10_square))          # Speed out of U-joint assuming maximum loss of power
    rpm_drivegear = rpm_drivetransmission * sratio
    
    print(f"Drive Motor's RPM at {walkspeed:.3f} m/s: {rpm_drivegear:.3f} RPM")

    return rpm_drivegear

def dirn_torque1(Weight, nofunits):
    internal_inertia = 0.12                                                         # To precess all 7 disks, in Nm
    gratio = 7 / 29

    mass_on_onedisk = ((Weight * g) / nofunits) / g
    human_m_of_inertia = mass_on_onedisk * (r ** 2)

    #ang_accel = accel / r

    torque_upperstage = human_m_of_inertia * ang_accel
    torque_cntrlgear = torque_upperstage * gratio * nofunits

    total_torque = torque_cntrlgear + internal_inertia
    print(f"Direction Motor's torque at angular acceleration of {ang_accel:.3f} rad/s²: {total_torque:.3f} Nm = {(total_torque * 10.1972):.3f} kg cm")
    
    return total_torque

''' 
    Dirn inertia calc:
    Torque with nothing on tiles: 0.3 kg cm
    No-load torque: 0.18 kg cm
    So torque read to overcome inertia of components: 0.12 kg cm
'''

def dirn_torque2(VGRF, Weight, nofunits, walking_speed, COF = cof):
    internal_inertia = 0.12                                                        # To precess all 7 disks, in Nm
    gratio = 7 / 29

    HGRF = (VGRF * (Weight * g)) * COF
    print(f"Total HGRF: {HGRF:.3f} N")
    
    HGRF_onedisk = HGRF / nofunits
    print(f"HGRF on one disk: {HGRF_onedisk:.3f} N")
    
    torque_upperstage = r * HGRF_onedisk

    if nofunits > 7:
        torque_cntrlgear = torque_upperstage * gratio * 7
    else:
        torque_cntrlgear = torque_upperstage * gratio * nofunits
    
    total_torque = torque_cntrlgear + internal_inertia
    print(f"Direction Motor's torque at {walking_speed:.3f} m/s: {total_torque:.3f} Nm = {(total_torque * 10.1972):.3f} kg cm")
    
    return total_torque

''' 
    In reality, the disks won't undergo bending necessarily, so the load of the person will be taken up solely by it.
    Hence, the direction motor's torque would just be used to overcome 17 mm bearing's friction.
'''

def dirn_speed(turnspeed):
    ang_velo = turnspeed / r
    sratio = 29 / 7

    rpm_upperstage = ang_velo * (60 / (2 * pi))
    
    rpm_cntrlgear = rpm_upperstage * sratio
    print(f"Direction Motor's RPM at {turnspeed:.3f} m/s: {rpm_cntrlgear:.3f} RPM")

    return rpm_cntrlgear





# Main program loop

if __name__ == "__main__":
    while True:
        print("\nSelect a function to run:")
        print("1. Drive Torque")
        print("2. Drive Speed")
        print("3. Direction Torque (angular acceleration)")
        print("4. Direction Torque (HGRF)")
        print("5. Direction Speed")
        print("6. VGRF")
        choice = input("\nEnter your choice (1–6): ")

        print()

        if choice == "1":
            VGRF_multiplier = float(input("Enter VGRF multiplier (BW): ")); print()
            Weight = float(input("Enter your weight (kg): ")); print()
            nofunits = int(input("Enter number of units in contact: ")); print()
            walking_speed = float(input("Enter walking speed (m/s): ")); print()
            print("Results:"); print()
            drive_torque(VGRF_multiplier, Weight, nofunits, walking_speed)

        elif choice == "2":
            walkspeed = float(input("Enter walking speed (m/s): ")); print()
            print("Results:"); print()
            drive_speed(walkspeed)

        elif choice == "3":
            ang_accel = float(input("Enter angular acceleration (rad/s²): ")); print()
            Weight = float(input("Enter your weight (kg): ")); print()
            nofunits = int(input("Enter number of units in contact: ")); print()
            print("Results:"); print()
            dirn_torque1(ang_accel, Weight, nofunits)

        elif choice == "4":
            VGRF = float(input("Enter VGRF (BW): ")); print()
            Weight = float(input("Enter your weight (kg): ")); print()
            nofunits = int(input("Enter number of units in contact: ")); print()
            walking_speed = float(input("Enter walking speed (m/s): ")); print()
            print("Results:"); print()
            dirn_torque2(VGRF, Weight, nofunits, walking_speed)

        elif choice == "5":
            turnspeed = float(input("Enter speed at which you're turning (m/s): ")); print()
            print("Results:"); print()
            dirn_speed(turnspeed)

        elif choice == "6":
            VGRF_multiplier = float(input("Enter VGRF multiplier (BW): ")); print()
            Weight_in_kg = float(input("Enter your weight (kg): ")); print()
            nofunits = int(input("Enter number of units in contact: ")); print()
            walk_speed = float(input("Enter walking speed (m/s): ")); print()
            print("Results"); print()
            vertical_force(walk_speed, VGRF_multiplier, Weight_in_kg, nofunits)

        else:
            print("Invalid choice. Please select 1–5.")

        again = input("\nDo you want to run another calculation? (y/n): ")
        if again.lower() != "y":
            print("\nExiting program.")
            break