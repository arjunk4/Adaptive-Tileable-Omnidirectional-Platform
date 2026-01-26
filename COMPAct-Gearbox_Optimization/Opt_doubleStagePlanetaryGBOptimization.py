import sys
import numpy as np
from ActuatorAndGearbox import motor
from ActuatorAndGearbox import material
from ActuatorAndGearbox import doubleStagePlanetaryGearbox
from ActuatorAndGearbox import doubleStagePlanetaryActuator
from ActuatorAndGearbox import optimizationDoubleStagePlanetaryActuator
import sys
import os
import json

#--------------------------------------------------------
# Importing Config data
#--------------------------------------------------------
# Get the current directory
current_dir = os.path.dirname(__file__)

# Build the file path
config_path      = os.path.join(current_dir, "config_files/config.json")
dspg_params_path = os.path.join(current_dir, "config_files/dspg_params.json")

# Load the JSON file
with open(config_path, "r") as config_file:
    config_data = json.load(config_file)

with open(dspg_params_path, "r") as dspg_params_file:
    dspg_params = json.load(dspg_params_file)

#---------------------------------------------------
# Transferring relevant data to individual variables
#---------------------------------------------------
motor_data          = config_data["Motors"]
material_properties = config_data["Material_properties"]

Gear_standard_parameters = config_data["Gear_standard_parameters"]
Lewis_params             = config_data["Lewis_params"]
MIT_params               = config_data["MIT_params"]

Steel    = material_properties["Steel"]
Aluminum = material_properties["Aluminum"]
PLA      = material_properties["PLA"]

dspg_design_params       = dspg_params["dspg_design_parameters_3DP"]
dspg_optimization_params = dspg_params["dspg_optimization_parameters"]

motor_driver_data = config_data["Motor_drivers"]

#--------------------------------------------------------
# Motors Drivers
#--------------------------------------------------------
Motor_Driver_Moteus_params    = motor_driver_data["Moteus"]
Motor_Driver_OdrivePro_params = motor_driver_data["OdrivePro"]

#--------------------------------------------------------
# Motors
#--------------------------------------------------------

# T motor Motor6375
Motor6375_Kv                         = motor_data["Motor6375_framed"]["Kv"]                   # rpm/V
Motor6375_maxContinuousCurrent       = motor_data["Motor6375_framed"]["maxContinuousCurrent"] # A

Motor6375_maxTorque                  = Motor6375_maxContinuousCurrent / (Motor6375_Kv * 2 * np.pi / 60)
Motor6375_power                      = motor_data["Motor6375_framed"]["power"]                 # W 
Motor6375_ratedVoltage               = motor_data["Motor6375_framed"]["ratedVoltage"]   
Motor6375_maxMotorAngVelRPM          = Motor6375_Kv * Motor6375_ratedVoltage   # RPM
Motor6375_mass                       = motor_data["Motor6375_framed"]["mass"]                  # kg 
Motor6375_dia                        = motor_data["Motor6375_framed"]["dia"]                   # mm 
Motor6375_length                     = motor_data["Motor6375_framed"]["length"]                # mm
Motor6375_motor_mount_hole_PCD       = motor_data["Motor6375_framed"]["motor_mount_hole_PCD"]
Motor6375_motor_mount_hole_dia       = motor_data["Motor6375_framed"]["motor_mount_hole_dia"]
Motor6375_motor_mount_hole_num       = motor_data["Motor6375_framed"]["motor_mount_hole_num"]
Motor6375_motor_output_hole_PCD      = motor_data["Motor6375_framed"]["motor_output_hole_PCD"]
Motor6375_motor_output_hole_dia      = motor_data["Motor6375_framed"]["motor_output_hole_dia"]
Motor6375_motor_output_hole_num      = motor_data["Motor6375_framed"]["motor_output_hole_num"]
Motor6375_wire_slot_dist_from_center = motor_data["Motor6375_framed"]["wire_slot_dist_from_center"]
Motor6375_wire_slot_length           = motor_data["Motor6375_framed"]["wire_slot_length"]
Motor6375_wire_slot_radius           = motor_data["Motor6375_framed"]["wire_slot_radius"]


# Motor-Motor6375 - Object Assignment
Motor6375 = motor(maxMotorAngVelRPM = Motor6375_maxMotorAngVelRPM,
                 maxMotorTorque    = Motor6375_maxTorque        ,
                 maxMotorPower     = Motor6375_power            ,
                 motorMass         = Motor6375_mass             , 
                 motorDia          = Motor6375_dia              ,
                 motorLength       = Motor6375_length           ,
                 motor_mount_hole_PCD       = Motor6375_motor_mount_hole_PCD,
                 motor_mount_hole_dia       = Motor6375_motor_mount_hole_dia,
                 motor_mount_hole_num       = Motor6375_motor_mount_hole_num,
                 motor_output_hole_PCD      = Motor6375_motor_output_hole_PCD,
                 motor_output_hole_dia      = Motor6375_motor_output_hole_dia,
                 motor_output_hole_num      = Motor6375_motor_output_hole_num,
                 wire_slot_dist_from_center = Motor6375_wire_slot_dist_from_center,
                 wire_slot_length           = Motor6375_wire_slot_length,
                 wire_slot_radius           = Motor6375_wire_slot_radius, 
                 motorName         = "Motor6375")


'''
MotorU12_Kv                         = motor_data["MotorU12_framed"]["Kv"]                   # rpm/V
MotorU12_maxContinuousCurrent       = motor_data["MotorU12_framed"]["maxContinuousCurrent"] # A

MotorU12_maxTorque                  = MotorU12_maxContinuousCurrent / (MotorU12_Kv * 2 * np.pi / 60)
MotorU12_power                      = motor_data["MotorU12_framed"]["power"]                 # W 
MotorU12_ratedVoltage               = motor_data["MotorU12_framed"]["ratedVoltage"]   
MotorU12_maxMotorAngVelRPM          = MotorU12_Kv * MotorU12_ratedVoltage   # RPM
MotorU12_mass                       = motor_data["MotorU12_framed"]["mass"]                  # kg 
MotorU12_dia                        = motor_data["MotorU12_framed"]["dia"]                   # mm 
MotorU12_length                     = motor_data["MotorU12_framed"]["length"]                # mm
MotorU12_motor_mount_hole_PCD       = motor_data["MotorU12_framed"]["motor_mount_hole_PCD"]
MotorU12_motor_mount_hole_dia       = motor_data["MotorU12_framed"]["motor_mount_hole_dia"]
MotorU12_motor_mount_hole_num       = motor_data["MotorU12_framed"]["motor_mount_hole_num"]
MotorU12_motor_output_hole_PCD      = motor_data["MotorU12_framed"]["motor_output_hole_PCD"]
MotorU12_motor_output_hole_dia      = motor_data["MotorU12_framed"]["motor_output_hole_dia"]
MotorU12_motor_output_hole_num      = motor_data["MotorU12_framed"]["motor_output_hole_num"]
MotorU12_wire_slot_dist_from_center = motor_data["MotorU12_framed"]["wire_slot_dist_from_center"]
MotorU12_wire_slot_length           = motor_data["MotorU12_framed"]["wire_slot_length"]
MotorU12_wire_slot_radius           = motor_data["MotorU12_framed"]["wire_slot_radius"]


# Motor-U12 - Object Assignment
MotorU12 = motor(maxMotorAngVelRPM = MotorU12_maxMotorAngVelRPM,
                 maxMotorTorque    = MotorU12_maxTorque        ,
                 maxMotorPower     = MotorU12_power            ,
                 motorMass         = MotorU12_mass             , 
                 motorDia          = MotorU12_dia              ,
                 motorLength       = MotorU12_length           ,
                 motor_mount_hole_PCD       = MotorU12_motor_mount_hole_PCD,
                 motor_mount_hole_dia       = MotorU12_motor_mount_hole_dia,
                 motor_mount_hole_num       = MotorU12_motor_mount_hole_num,
                 motor_output_hole_PCD      = MotorU12_motor_output_hole_PCD,
                 motor_output_hole_dia      = MotorU12_motor_output_hole_dia,
                 motor_output_hole_num      = MotorU12_motor_output_hole_num,
                 wire_slot_dist_from_center = MotorU12_wire_slot_dist_from_center,
                 wire_slot_length           = MotorU12_wire_slot_length,
                 wire_slot_radius           = MotorU12_wire_slot_radius, 
                 motorName         = "U12")
'''



#--------------------------------------------------------
# Gearbox 
#--------------------------------------------------------
doubleStagePlanetaryGearboxInstance = doubleStagePlanetaryGearbox(design_parameters         = dspg_design_params,
                                                                  gear_standard_parameters  = Gear_standard_parameters,
                                                                  densityGears              = PLA["density"],
                                                                  densityStructure          = PLA["density"],
                                                                  maxGearAllowableStressMPa = PLA["maxAllowableStressMPa"])
                                                                  


#----------------------------------------
# Actuator
#----------------------------------------

maxGBDia_multFactor           = dspg_optimization_params["MAX_GB_DIA_MULT_FACTOR"] # 1
#maxGBDia_multFactor_MAD_M6C12 = dspg_optimization_params["MAX_GB_DIA_MULT_FACTOR_MAD_M6C12"] # 1.25


maxGearboxDiameter_Motor6375       = Motor6375.motorDiaMM       * maxGBDia_multFactor - 2*dspg_design_params["ring_radial_thickness"]
# maxGearboxDiameter_U10       = MotorU10.motorDiaMM       * maxGBDia_multFactor - 2*dspg_design_params["ring_radial_thickness"]

# RT46110RB-Actuator
Actuator_Motor6375 = doubleStagePlanetaryActuator(design_parameters           = dspg_design_params,
                                            motor                       = Motor6375,  
                                            motor_driver_params         = Motor_Driver_OdrivePro_params,
                                            doubleStagePlanetaryGearbox = doubleStagePlanetaryGearboxInstance, 
                                            FOS                         = MIT_params["FOS"], 
                                            serviceFactor               = MIT_params["serviceFactor"], 
                                            maxGearboxDiameter          = maxGearboxDiameter_Motor6375,
                                            stressAnalysisMethodName    = "MIT")



'''
# U10-Actuator
Actuator_U10 = doubleStagePlanetaryActuator(design_parameters           = dspg_design_params,
                                            motor                       = MotorU10,  
                                            motor_driver_params         = Motor_Driver_OdrivePro_params,
                                            doubleStagePlanetaryGearbox = doubleStagePlanetaryGearboxInstance, 
                                            FOS                         = MIT_params["FOS"], 
                                            serviceFactor               = MIT_params["serviceFactor"], 
                                            maxGearboxDiameter          = maxGearboxDiameter_U10,
                                            stressAnalysisMethodName    = "MIT")
'''





#---------------------------------------
# Optimization
#---------------------------------------

opt_param = config_data["Cost_gain_parameters"]

K_Mass = opt_param["K_Mass"]
K_Eff  = opt_param["K_Eff"]
K_Width  = opt_param["K_Width"]

GEAR_RATIO_MIN  = dspg_optimization_params["GEAR_RATIO_MIN"]        # 4   
GEAR_RATIO_MAX  = dspg_optimization_params["GEAR_RATIO_MAX"]        # 45  
GEAR_RATIO_STEP = dspg_optimization_params["GEAR_RATIO_STEP"]       # 1  

MODULE_STAGE1_MIN     = dspg_optimization_params["MODULE_STAGE1_MIN"]     # 0.5 
MODULE_STAGE1_MAX     = dspg_optimization_params["MODULE_STAGE1_MAX"]     # 0.8 
MODULE_STAGE2_MIN     = dspg_optimization_params["MODULE_STAGE2_MIN"]     # 0.9 
MODULE_STAGE2_MAX     = dspg_optimization_params["MODULE_STAGE2_MAX"]     # 1.2 
NUM_PLANET_STAGE1_MIN = dspg_optimization_params["NUM_PLANET_STAGE1_MIN"] # 3   
NUM_PLANET_STAGE1_MAX = dspg_optimization_params["NUM_PLANET_STAGE1_MAX"] # 5   
NUM_PLANET_STAGE2_MIN = dspg_optimization_params["NUM_PLANET_STAGE2_MIN"] # 3   
NUM_PLANET_STAGE2_MAX = dspg_optimization_params["NUM_PLANET_STAGE2_MAX"] # 5   
NUM_TEETH_SUN_MIN     = dspg_optimization_params["NUM_TEETH_SUN_MIN"]     # 20  
NUM_TEETH_PLANET_MIN  = dspg_optimization_params["NUM_TEETH_PLANET_MIN"]  # 20   



Optimizer_Motor6375    = optimizationDoubleStagePlanetaryActuator(design_parameters        = dspg_design_params,
                                                            gear_standard_parameters = Gear_standard_parameters,
                                                            K_Mass                   = K_Mass                ,
                                                            K_Eff                    = K_Eff                 ,
                                                            K_Width                  = K_Width               ,
                                                            MODULE_STAGE1_MIN        = MODULE_STAGE1_MIN     ,
                                                            MODULE_STAGE1_MAX        = MODULE_STAGE1_MAX     ,
                                                            MODULE_STAGE2_MIN        = MODULE_STAGE2_MIN     ,
                                                            MODULE_STAGE2_MAX        = MODULE_STAGE2_MAX     ,
                                                            NUM_PLANET_STAGE1_MIN    = NUM_PLANET_STAGE1_MIN ,
                                                            NUM_PLANET_STAGE1_MAX    = NUM_PLANET_STAGE1_MAX ,
                                                            NUM_PLANET_STAGE2_MIN    = NUM_PLANET_STAGE2_MIN ,
                                                            NUM_PLANET_STAGE2_MAX    = NUM_PLANET_STAGE2_MAX ,
                                                            NUM_TEETH_SUN_MIN        = NUM_TEETH_SUN_MIN     ,
                                                            NUM_TEETH_PLANET_MIN     = NUM_TEETH_PLANET_MIN  ,
                                                            GEAR_RATIO_MIN           = GEAR_RATIO_MIN        ,
                                                            GEAR_RATIO_MAX           = GEAR_RATIO_MAX        ,
                                                            GEAR_RATIO_STEP          = GEAR_RATIO_STEP       )




totalTime_Motor6375 = Optimizer_Motor6375.optimizeActuator(Actuator_Motor6375, UsePSCasVariable = 0, log=0, csv=1, printOptParams=1, gearRatioReq=0)

# Convert to hours, minutes, and seconds
hours_Motor6375, remainder_Motor6375 = divmod(totalTime_Motor6375, 3600)
minutes_Motor6375, seconds_Motor6375 = divmod(remainder_Motor6375, 60)

# Print
print("Optimization Completed : DSPG Motor6375")
print(f"Time taken: {hours_Motor6375} hours, {minutes_Motor6375} minutes, and {seconds_Motor6375} seconds")





'''
Optimizer_U10    = optimizationDoubleStagePlanetaryActuator(design_parameters        = dspg_design_params,
                                                            gear_standard_parameters = Gear_standard_parameters,
                                                            K_Mass                   = K_Mass                ,
                                                            K_Eff                    = K_Eff                 ,
                                                            K_Width                  = K_Width               ,
                                                            MODULE_STAGE1_MIN        = MODULE_STAGE1_MIN     ,
                                                            MODULE_STAGE1_MAX        = MODULE_STAGE1_MAX     ,
                                                            MODULE_STAGE2_MIN        = MODULE_STAGE2_MIN     ,
                                                            MODULE_STAGE2_MAX        = MODULE_STAGE2_MAX     ,
                                                            NUM_PLANET_STAGE1_MIN    = NUM_PLANET_STAGE1_MIN ,
                                                            NUM_PLANET_STAGE1_MAX    = NUM_PLANET_STAGE1_MAX ,
                                                            NUM_PLANET_STAGE2_MIN    = NUM_PLANET_STAGE2_MIN ,
                                                            NUM_PLANET_STAGE2_MAX    = NUM_PLANET_STAGE2_MAX ,
                                                            NUM_TEETH_SUN_MIN        = NUM_TEETH_SUN_MIN     ,
                                                            NUM_TEETH_PLANET_MIN     = NUM_TEETH_PLANET_MIN  ,
                                                            GEAR_RATIO_MIN           = GEAR_RATIO_MIN        ,
                                                            GEAR_RATIO_MAX           = GEAR_RATIO_MAX        ,
                                                            GEAR_RATIO_STEP          = GEAR_RATIO_STEP       )

totalTime_U10 = Optimizer_U10.optimizeActuator(Actuator_U10, UsePSCasVariable = 0, log=0, csv=1, printOptParams=1, gearRatioReq=0)

# Convert to hours, minutes, and seconds
hours_U10, remainder_U10 = divmod(totalTime_U10, 3600)
minutes_U10, seconds_U10 = divmod(remainder_U10, 60)

# Print
print("Optimization Completed : DSPG U10")
print(f"Time taken: {hours_U10} hours, {minutes_U10} minutes, and {seconds_U10} seconds")
'''