import sys
import numpy as np
from ActuatorAndGearbox import motor
from ActuatorAndGearbox import material
from ActuatorAndGearbox import compoundPlanetaryGearbox
from ActuatorAndGearbox import compoundPlanetaryActuator
from ActuatorAndGearbox import optimizationCompoundPlanetaryActuator
import os
import json

#--------------------------------------------------------
# Importing motor data
#--------------------------------------------------------
# Get the current directory
current_dir = os.path.dirname(__file__)

# Build the file path
config_path = os.path.join(current_dir, "config_files/config.json")
cpg_params_path = os.path.join(current_dir, "config_files/cpg_params.json")

# Load the JSON file
with open(config_path, "r") as config_file:
    config_data = json.load(config_file)

with open(cpg_params_path, "r") as cpg_params_file:
    cpg_params = json.load(cpg_params_file)

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

cpg_design_params       = cpg_params["cpg_3DP_design_parameters"]
cpg_optimization_params = cpg_params["cpg_optimization_parameters"]

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


#-------------------------------------------------------
# Gearbox 
#-------------------------------------------------------
compoundPlanetaryGearboxInstance = compoundPlanetaryGearbox(design_parameters         = cpg_design_params,
                                                            gear_standard_parameters  = Gear_standard_parameters,
                                                            densityGears              = PLA["density"],
                                                            densityStructure          = PLA["density"],
                                                            maxGearAllowableStressMPa = PLA["maxAllowableStressMPa"])

#-----------------------------------------------------
# Actuator
#-----------------------------------------------------
maxGBDia_multFactor           = cpg_optimization_params["MAX_GB_DIA_MULT_FACTOR"] # 1
#maxGBDia_multFactor_MAD_M6C12 = cpg_optimization_params["MAX_GB_DIA_MULT_FACTOR_MAD_M6C12"] # 1.25

maxGearboxDiameter_Motor6375       = Motor6375.motorDiaMM       * maxGBDia_multFactor - 2*cpg_design_params["ringRadialWidthMM"]
#maxGearboxDiameter_U8         = maxGBDia_multFactor * MotorU8.motorDiaMM       

# RT46110RB-Actuator
Actuator_Motor6375 = compoundPlanetaryActuator(design_parameters           = cpg_design_params,
                                            motor                       = Motor6375,  
                                            motor_driver_params         = Motor_Driver_OdrivePro_params,
                                            compoundPlanetaryGearbox = compoundPlanetaryGearboxInstance, 
                                            FOS                         = MIT_params["FOS"], 
                                            serviceFactor               = MIT_params["serviceFactor"], 
                                            maxGearboxDiameter          = maxGearboxDiameter_Motor6375,
                                            stressAnalysisMethodName    = "MIT")

'''
# U8-Actuator
Actuator_U8 = compoundPlanetaryActuator(design_parameters        = cpg_design_params,
                                        motor                    = MotorU8,  
                                        motor_driver_params      = Motor_Driver_OdrivePro_params,
                                        compoundPlanetaryGearbox = compoundPlanetaryGearboxInstance, 
                                        FOS                      = MIT_params["FOS"], 
                                        serviceFactor            = MIT_params["serviceFactor"], 
                                        maxGearboxDiameter       = maxGearboxDiameter_U8,
                                        stressAnalysisMethodName = "MIT")
'''

#-----------------------------------------------------
# Optimization
#-----------------------------------------------------
opt_param = config_data["Cost_gain_parameters"]

K_Mass = opt_param["K_Mass"]
K_Eff  = opt_param["K_Eff"]
K_Width = opt_param["K_Width"]

GEAR_RATIO_MIN  = cpg_optimization_params["GEAR_RATIO_MIN"]  # 4
GEAR_RATIO_MAX  = cpg_optimization_params["GEAR_RATIO_MAX"]  # 30
GEAR_RATIO_STEP = cpg_optimization_params["GEAR_RATIO_STEP"] # 1

MODULE_BIG_MIN             = cpg_optimization_params["MODULE_MIN"]           # 0.8
MODULE_BIG_MAX             = cpg_optimization_params["MODULE_MAX"]           # 1.2
MODULE_SMALL_MIN           = cpg_optimization_params["MODULE_MIN"]           # 0.8
MODULE_SMALL_MAX           = cpg_optimization_params["MODULE_MAX"]           # 1.2
NUM_PLANET_MIN             = cpg_optimization_params["NUM_PLANET_MIN"]       # 3  
NUM_PLANET_MAX             = cpg_optimization_params["NUM_PLANET_MAX"]       # 5  
NUM_TEETH_SUN_MIN          = cpg_optimization_params["NUM_TEETH_SUN_MIN"]    # 20 
NUM_TEETH_PLANET_BIG_MIN   = cpg_optimization_params["NUM_TEETH_PLANET_MIN"] # 20 
NUM_TEETH_PLANET_SMALL_MIN = cpg_optimization_params["NUM_TEETH_PLANET_MIN"] # 20 


Optimizer_Motor6375     = optimizationCompoundPlanetaryActuator(design_parameters          = cpg_design_params,
                                                         gear_standard_parameters   = Gear_standard_parameters,
                                                         K_Mass                     = K_Mass                     ,
                                                         K_Eff                      = K_Eff                      ,
                                                         K_Width                    = K_Width                    ,
                                                         MODULE_BIG_MIN             = MODULE_BIG_MIN             ,
                                                         MODULE_BIG_MAX             = MODULE_BIG_MAX             ,
                                                         MODULE_SMALL_MIN           = MODULE_SMALL_MIN           ,
                                                         MODULE_SMALL_MAX           = MODULE_SMALL_MAX           ,
                                                         NUM_PLANET_MIN             = NUM_PLANET_MIN             ,
                                                         NUM_PLANET_MAX             = NUM_PLANET_MAX             ,
                                                         NUM_TEETH_SUN_MIN          = NUM_TEETH_SUN_MIN          ,
                                                         NUM_TEETH_PLANET_BIG_MIN   = NUM_TEETH_PLANET_BIG_MIN   ,
                                                         NUM_TEETH_PLANET_SMALL_MIN = NUM_TEETH_PLANET_SMALL_MIN ,
                                                         GEAR_RATIO_MIN             = GEAR_RATIO_MIN             ,
                                                         GEAR_RATIO_MAX             = GEAR_RATIO_MAX             ,
                                                         GEAR_RATIO_STEP            = GEAR_RATIO_STEP            )

totalTime_Motor6375 = Optimizer_Motor6375.optimizeActuator(Actuator_Motor6375, UsePSCasVariable = 0, log=0, csv=1, printOptParams=1, gearRatioReq = 0)
print("Optimization Completed : CPG Motor6375 : Total Time:", totalTime_Motor6375)

'''
Optimizer_U8     = optimizationCompoundPlanetaryActuator(design_parameters          = cpg_design_params,
                                                         gear_standard_parameters   = Gear_standard_parameters,
                                                         K_Mass                     = K_Mass                     ,
                                                         K_Eff                      = K_Eff                      ,
                                                         K_Width                    = K_Width                    ,
                                                         MODULE_BIG_MIN             = MODULE_BIG_MIN             ,
                                                         MODULE_BIG_MAX             = MODULE_BIG_MAX             ,
                                                         MODULE_SMALL_MIN           = MODULE_SMALL_MIN           ,
                                                         MODULE_SMALL_MAX           = MODULE_SMALL_MAX           ,
                                                         NUM_PLANET_MIN             = NUM_PLANET_MIN             ,
                                                         NUM_PLANET_MAX             = NUM_PLANET_MAX             ,
                                                         NUM_TEETH_SUN_MIN          = NUM_TEETH_SUN_MIN          ,
                                                         NUM_TEETH_PLANET_BIG_MIN   = NUM_TEETH_PLANET_BIG_MIN   ,
                                                         NUM_TEETH_PLANET_SMALL_MIN = NUM_TEETH_PLANET_SMALL_MIN ,
                                                         GEAR_RATIO_MIN             = GEAR_RATIO_MIN             ,
                                                         GEAR_RATIO_MAX             = GEAR_RATIO_MAX             ,
                                                         GEAR_RATIO_STEP            = GEAR_RATIO_STEP            )


#-------------------------------------------------
# Optimize
#-------------------------------------------------
totalTime_U8 = Optimizer_U8.optimizeActuator(Actuator_U8, UsePSCasVariable = 0, log=0, csv=1, printOptParams=1, gearRatioReq = 0)
print("Optimization Completed : CPG U8 : Total Time:", totalTime_U8)
'''