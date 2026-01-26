# Single Row Deep Groove Ball Bearings assumed

import numpy as np                                                                  # type: ignore


g = 9.81                                                                            # m/s²
r = 0.019                                                                           # m (radius of drive disk)
pi = 3.1416
sin_10 = 0.1736
sin_10_square = 0.03015                                                             # sin(10°)²
cos_10 = 0.9848                                                                     # cos(10°)
cof = 0.35                                                                          # coefficient of friction


def bearing_static_fos(VGRF_factor, Weight, nofunits, static_load_rating_drive, static_load_rating_control):
    weight_in_N = Weight * g
    total_VGRF = VGRF_factor * weight_in_N
    VGRF_onedisk = total_VGRF / nofunits

    # CONTROL BEARING (pure axial)
    control_fos = (static_load_rating_control * 0.1) / VGRF_onedisk            # SMB standard
    # control_fos = (static_load_rating * 0.5) / VGRF_onedisk          # SKF standard

    # DRIVE BEARING (axial + radial)
    axial_load = VGRF_onedisk * cos_10
    radial_load = VGRF_onedisk * sin_10
    equivalent_load = 0.6 * radial_load + 0.5 * axial_load             # SKF standard
    drive_fos = static_load_rating_drive / equivalent_load

    # Return result as dictionary
    return {
        "control_fos": control_fos,
        "drive_fos": drive_fos
    }



def bearing_dynamic_life(
    VGRF, Weight, nofunits,
    static_load_rating_control, static_load_rating_drive,
    dynamic_load_rating_control, dynamic_load_rating_drive,
    calculation_factor_control, calculation_factor_drive,
):
    
    # Step 1: Common load calculations
    weight_in_N = Weight * g
    total_VGRF = VGRF * weight_in_N
    VGRF_onedisk = total_VGRF / nofunits

    V = 1       # inner ring rotates
    L_R = 1e6   # catalog rating life
    a = 3       # ball bearings

    # Table data (same for both bearings)
    table_f0Fa_over_C0 = np.array([0.172, 0.345, 0.689, 1.03, 1.38, 2.07, 3.45, 5.17, 6.89])
    table_e = np.array([0.19, 0.22, 0.26, 0.28, 0.30, 0.34, 0.38, 0.42, 0.44])
    table_X = np.array([0.56]*9)
    table_Y = np.array([2.3, 1.99, 1.71, 1.55, 1.45, 1.31, 1.15, 1.04, 1.00])

    # Control Bearing (Pure Axial)
    F_a_c = VGRF_onedisk
    F_r_c = 0
    ratio_c = calculation_factor_control * (F_a_c / static_load_rating_control)

    e_c = np.interp(ratio_c, table_f0Fa_over_C0, table_e)
    Y_c = np.interp(ratio_c, table_f0Fa_over_C0, table_Y)

    F_e_c = Y_c * F_a_c  # pure axial
    control_life_revs = L_R * (dynamic_load_rating_control / F_e_c)**a


    # Drive Bearing (Axial + Radial)
    F_a_d = VGRF_onedisk * cos_10
    F_r_d = VGRF_onedisk * sin_10
    ratio_d = calculation_factor_drive * (F_a_d / static_load_rating_drive)

    e_d = np.interp(ratio_d, table_f0Fa_over_C0, table_e)
    X_d = np.interp(ratio_d, table_f0Fa_over_C0, table_X)
    Y_d = np.interp(ratio_d, table_f0Fa_over_C0, table_Y)

    if F_r_d == 0:
        F_e_d = Y_d * F_a_d
    else:
        if (F_a_d / (V * F_r_d)) <= e_d:
            F_e_d = V * F_r_d
        else:
            F_e_d = X_d * V * F_r_d + Y_d * F_a_d

    drive_life_revs = L_R * (dynamic_load_rating_drive / F_e_d)**a

    return {
        "control_life_revs": control_life_revs,
        "drive_life_revs": drive_life_revs
    }

def bearing_frictional_torque(
    VGRF, Weight, nofunits,
    static_load_rating_control, static_load_rating_drive,
    calculation_factor_control, calculation_factor_drive,
):
    # Common load calculations
    weight_in_N = Weight * g
    total_VGRF = VGRF * weight_in_N
    VGRF_onedisk = total_VGRF / nofunits

    V = 1  # inner ring rotates

    # ISO table data
    table_f0Fa_over_C0 = np.array([0.172, 0.345, 0.689, 1.03, 1.38, 2.07, 3.45, 5.17, 6.89])
    table_e = np.array([0.19, 0.22, 0.26, 0.28, 0.30, 0.34, 0.38, 0.42, 0.44])
    table_X = np.array([0.56]*9)
    table_Y = np.array([2.3, 1.99, 1.71, 1.55, 1.45, 1.31, 1.15, 1.04, 1.00])

    # ===== Control bearing (pure axial) =====
    F_a_c = VGRF_onedisk
    ratio_c = calculation_factor_control * (F_a_c / static_load_rating_control)

    Y_c = np.interp(ratio_c, table_f0Fa_over_C0, table_Y)
    F_e_c = Y_c * F_a_c

    # ===== Drive bearing (axial + radial) =====
    F_a_d = VGRF_onedisk * cos_10
    F_r_d = VGRF_onedisk * sin_10
    ratio_d = calculation_factor_drive * (F_a_d / static_load_rating_drive)

    e_d = np.interp(ratio_d, table_f0Fa_over_C0, table_e)
    X_d = np.interp(ratio_d, table_f0Fa_over_C0, table_X)
    Y_d = np.interp(ratio_d, table_f0Fa_over_C0, table_Y)

    if (F_a_d / (V * F_r_d)) <= e_d:
        F_e_d = V * F_r_d
    else:
        F_e_d = X_d * V * F_r_d + Y_d * F_a_d

    # Direction Bearing's frictional torque
    trq_c = 0.003 * F_e_c * (25 / 2) * 0.001   # Nm

    # Drive Bearing's frictional torque
    trq_d = 0.003 * F_e_d * (17 / 2) * 0.001   # Nm

    return {
        "Direction Bearing friction": trq_c,
        "Drive Bearing friction": trq_d
    }


def static_fos_71805(VGRF_factor, Weight, nofunits, static_load_rating, y_0):
    weight_in_N = Weight * g
    total_VGRF = VGRF_factor * weight_in_N
    VGRF_onedisk = total_VGRF / nofunits

    radial_load = 0

    fos = static_load_rating / (VGRF_onedisk * y_0 + radial_load * 0.5)

    return fos

def dynamic_life_71805(VGRF_factor, Weight, nofunits, dynamic_load_rating, y_2):
    weight_in_N = Weight * g
    total_VGRF = VGRF_factor * weight_in_N
    VGRF_onedisk = total_VGRF / nofunits

    L_R = 1e6   # catalog rating life
    a = 3       # ball bearings

    equivalent_dynamic_load = VGRF_onedisk * y_2   # radial_load = 0

    life_revs = L_R * (dynamic_load_rating / equivalent_dynamic_load)**a

    life_hours = life_revs / (60 * 100)    # Assuming its spinning at 100 rpm

    return life_hours
