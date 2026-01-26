import sys
import numpy as np
from ActuatorAndGearbox import singleStagePlanetaryGearbox
from ActuatorAndGearbox import motor
from ActuatorAndGearbox import motor_driver
from ActuatorAndGearbox import singleStagePlanetaryActuator
from ActuatorAndGearbox import optimizationSingleStageActuator
import json
import os

#--------------------------------------------------------
# Importing Config data
#--------------------------------------------------------
# Get the current directory
current_dir = os.path.dirname(__file__)

# Build the file path
config_path      = os.path.join(current_dir, "config_files/config.json")
sspg_params_path = os.path.join(current_dir, "config_files/sspg_params.json")

# Load the JSON file
with open(config_path, "r") as config_file:
    config_data = json.load(config_file)

with open(sspg_params_path, "r") as sspg_params_file:
    sspg_params = json.load(sspg_params_file)

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

sspg_design_params       = sspg_params["sspg_3DP_design_parameters"]
sspg_optimization_params = sspg_params["sspg_optimization_parameters"]

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
# T motor U8
MotorU8_Kv                         = motor_data["MotorU8_framed"]["Kv"]                   # rpm/V
MotorU8_maxContinuousCurrent       = motor_data["MotorU8_framed"]["maxContinuousCurrent"] # A

MotorU8_maxTorque                  = MotorU8_maxContinuousCurrent / (MotorU8_Kv * 2 * np.pi / 60)
MotorU8_power                      = motor_data["MotorU8_framed"]["power"]                 # W 

MotorU8_ratedVoltage               = motor_data["MotorU8_framed"]["ratedVoltage"]   
MotorU8_maxMotorAngVelRPM          = MotorU8_Kv * MotorU8_ratedVoltage # RPM 
MotorU8_mass                       = motor_data["MotorU8_framed"]["mass"]                  # kg 
MotorU8_dia                        = motor_data["MotorU8_framed"]["dia"]                   # mm 
MotorU8_length                     = motor_data["MotorU8_framed"]["length"]                # mm
MotorU8_motor_mount_hole_PCD       = motor_data["MotorU8_framed"]["motor_mount_hole_PCD"]
MotorU8_motor_mount_hole_dia       = motor_data["MotorU8_framed"]["motor_mount_hole_dia"]
MotorU8_motor_mount_hole_num       = motor_data["MotorU8_framed"]["motor_mount_hole_num"]
MotorU8_motor_output_hole_PCD      = motor_data["MotorU8_framed"]["motor_output_hole_PCD"]
MotorU8_motor_output_hole_dia      = motor_data["MotorU8_framed"]["motor_output_hole_dia"]
MotorU8_motor_output_hole_num      = motor_data["MotorU8_framed"]["motor_output_hole_num"]
MotorU8_wire_slot_dist_from_center = motor_data["MotorU8_framed"]["wire_slot_dist_from_center"]
MotorU8_wire_slot_length           = motor_data["MotorU8_framed"]["wire_slot_length"]
MotorU8_wire_slot_radius           = motor_data["MotorU8_framed"]["wire_slot_radius"]

# Motor-U8
MotorU8 = motor(maxMotorAngVelRPM           = MotorU8_maxMotorAngVelRPM, 
                 maxMotorTorque             = MotorU8_maxTorque,
                 maxMotorPower              = MotorU8_power,
                 motorMass                  = MotorU8_mass,
                 motorDia                   = MotorU8_dia,
                 motorLength                = MotorU8_length,
                 motor_mount_hole_PCD       = MotorU8_motor_mount_hole_PCD,
                 motor_mount_hole_dia       = MotorU8_motor_mount_hole_dia,
                 motor_mount_hole_num       = MotorU8_motor_mount_hole_num,
                 motor_output_hole_PCD      = MotorU8_motor_output_hole_PCD,
                 motor_output_hole_dia      = MotorU8_motor_output_hole_dia,
                 motor_output_hole_num      = MotorU8_motor_output_hole_num,
                 wire_slot_dist_from_center = MotorU8_wire_slot_dist_from_center,
                 wire_slot_length           = MotorU8_wire_slot_length,
                 wire_slot_radius           = MotorU8_wire_slot_radius,
                 motorName                  = "U8")
'''


#--------------------------------------------------------
# Gearboxes  
#--------------------------------------------------------
PlanetaryGearbox = singleStagePlanetaryGearbox(design_params             = sspg_design_params,
                                               gear_standard_parameters  = Gear_standard_parameters,
                                               maxGearAllowableStressMPa = PLA["maxAllowableStressMPa"], # MPa
                                               densityGears              = PLA["density"], # kg/m^3
                                               densityStructure          = PLA["density"]) # kg/m^3

#--------------------------------------------------------
# Actuators
#--------------------------------------------------------
maxGBDia_multFactor           = sspg_optimization_params["MAX_GB_DIA_MULT_FACTOR"] # 1
#maxGBDia_multFactor_MAD_M6C12 = sspg_optimization_params["MAX_GB_DIA_MULT_FACTOR_MAD_M6C12"] # 1.25

maxGearboxDiameter_Motor6375        = maxGBDia_multFactor * Motor6375.motorDiaMM     - 2*sspg_design_params["ringRadialWidthMM"]
#maxGearboxDiameter_U8        = maxGBDia_multFactor * MotorU8.motorDiaMM     - 2*sspg_design_params["ringRadialWidthMM"] 

# Motor6375-Actuator
Actuator_Motor6375    = singleStagePlanetaryActuator(design_params             = sspg_design_params,
                                               motor                    = Motor6375,
                                               motor_driver_params      = Motor_Driver_OdrivePro_params,
                                               planetaryGearbox         = PlanetaryGearbox,
                                               FOS                      = MIT_params["FOS"],
                                               serviceFactor            = MIT_params["serviceFactor"],
                                               maxGearboxDiameter       = maxGearboxDiameter_Motor6375 , # mm 
                                               stressAnalysisMethodName = "MIT") # Lewis or AGMA

'''
# U8-Actuator
Actuator_U8    = singleStagePlanetaryActuator(design_params             = sspg_design_params,
                                               motor                    = MotorU8,
                                               motor_driver_params      = Motor_Driver_OdrivePro_params,
                                               planetaryGearbox         = PlanetaryGearbox,
                                               FOS                      = MIT_params["FOS"],
                                               serviceFactor            = MIT_params["serviceFactor"],
                                               maxGearboxDiameter       = maxGearboxDiameter_U8 , # mm 
                                               stressAnalysisMethodName = "MIT") # Lewis or AGMA
'''

#--------------------------------------------------------
# Optimization
#--------------------------------------------------------
cost_gains = config_data["Cost_gain_parameters"]

K_Mass = cost_gains["K_Mass"]
K_Eff  = cost_gains["K_Eff"]
K_Width = cost_gains["K_Width"]

GEAR_RATIO_MIN       = sspg_optimization_params["GEAR_RATIO_MIN"]       # 4   
GEAR_RATIO_MAX       = sspg_optimization_params["GEAR_RATIO_MAX"]       # 15 
GEAR_RATIO_STEP      = sspg_optimization_params["GEAR_RATIO_STEP"]      # 1  

MODULE_MIN           = sspg_optimization_params["MODULE_MIN"]           # 0.5 
MODULE_MAX           = sspg_optimization_params["MODULE_MAX"]           # 1.2 
NUM_PLANET_MIN       = sspg_optimization_params["NUM_PLANET_MIN"]       # 3   
NUM_PLANET_MAX       = sspg_optimization_params["NUM_PLANET_MAX"]       # 7   
NUM_TEETH_SUN_MIN    = sspg_optimization_params["NUM_TEETH_SUN_MIN"]    # 20  
NUM_TEETH_PLANET_MIN = sspg_optimization_params["NUM_TEETH_PLANET_MIN"] # 20

Optimizer_Motor6375     = optimizationSingleStageActuator(design_params             = sspg_design_params  ,
                                                   gear_standard_paramaeters = Gear_standard_parameters,
                                                   K_Mass                    = K_Mass              ,
                                                   K_Eff                     = K_Eff               ,
                                                   K_Width                   = K_Width             ,
                                                   MODULE_MIN                = MODULE_MIN          ,
                                                   MODULE_MAX                = MODULE_MAX          ,
                                                   NUM_PLANET_MIN            = NUM_PLANET_MIN      ,
                                                   NUM_PLANET_MAX            = NUM_PLANET_MAX      ,
                                                   NUM_TEETH_SUN_MIN         = NUM_TEETH_SUN_MIN   ,
                                                   NUM_TEETH_PLANET_MIN      = NUM_TEETH_PLANET_MIN,
                                                   GEAR_RATIO_MIN            = GEAR_RATIO_MIN      ,
                                                   GEAR_RATIO_MAX            = GEAR_RATIO_MAX      ,
                                                   GEAR_RATIO_STEP           = GEAR_RATIO_STEP     )


#Motor6375
totalTime_Motor6375 = Optimizer_Motor6375.optimizeActuator(Actuator_Motor6375, UsePSCasVariable = 0, log=0, csv=1, printOptParams=1, gearRatioReq = 0)
print("Optimization Completed : Motor6375 SSPG : Time taken:", totalTime_Motor6375, " sec")

'''
Optimizer_U8     = optimizationSingleStageActuator(design_params             = sspg_design_params  ,
                                                   gear_standard_paramaeters = Gear_standard_parameters,
                                                   K_Mass                    = K_Mass              ,
                                                   K_Eff                     = K_Eff               ,
                                                   K_Width                   = K_Width             ,
                                                   MODULE_MIN                = MODULE_MIN          ,
                                                   MODULE_MAX                = MODULE_MAX          ,
                                                   NUM_PLANET_MIN            = NUM_PLANET_MIN      ,
                                                   NUM_PLANET_MAX            = NUM_PLANET_MAX      ,
                                                   NUM_TEETH_SUN_MIN         = NUM_TEETH_SUN_MIN   ,
                                                   NUM_TEETH_PLANET_MIN      = NUM_TEETH_PLANET_MIN,
                                                   GEAR_RATIO_MIN            = GEAR_RATIO_MIN      ,
                                                   GEAR_RATIO_MAX            = GEAR_RATIO_MAX      ,
                                                   GEAR_RATIO_STEP           = GEAR_RATIO_STEP     )


#U8
totalTime_U8 = Optimizer_U8.optimizeActuator(Actuator_U8, UsePSCasVariable = 0, log=0, csv=1, printOptParams=1, gearRatioReq = 0)
print("Optimization Completed : U8 SSPG : Time taken:", totalTime_U8, " sec")
'''