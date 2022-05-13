from jinja2 import Template
import json

json_file = open("./settings.json", "r")
settings = json.load(json_file)

activeSensors = settings["sensors"]

### sensorX.cpp ###

with open('./templates/templateSensorCpp.txt') as templateSensorCpp:
    template = Template(templateSensorCpp.read())
    for sensor in activeSensors:
        sensorName = sensor["name"]
        with open(f'{sensorName}' + '.cpp', 'w') as sensorCpp:
            sensorCpp.write(template.render(sensorName=sensorName))
    templateSensorCpp.close()

### sensorX.h ###
with open('./templates/templateSensorH.txt') as templateSensorH:
    template = Template(templateSensorH.read())
    for sensor in activeSensors:
        sensorName = sensor["name"]
        with open(f'{sensorName}' + '.h', 'w') as sensorH:
            sensorH.write(template.render(sensorName=sensorName))
    templateSensorH.close()

### config.h ###

# define generic params
with open("config.h", "w") as configH:
    configH.write("// generic simulator params\n")
    configH.write(f'#define SIM_STEP {settings["sim_step"]}\n')
    configH.write(f'#define VREF_CTI {settings["vref_cti"]}\n')
    configH.write(f'#define SOC_INIT {settings["soc_init"]}\n')
    configH.write(f'#define SELFDISCH_FACTOR {settings["selfdisch_factor"]}\n')
    configH.write(f'#define PERIOD {settings["period"]}\n')
    configH.close()

# define params for sensors
with open('./templates/templateConfigSensor.txt') as templateConfigSensor:
    template = Template(templateConfigSensor.read())
    sensorsEndAt = 0    # used to know when the MCU can start
    for sensor in activeSensors:
        sensorName = sensor["name"]
        onPower = sensor["power_on"]
        offPower = sensor["power_off"]
        actTime = sensor["activation_time"]
        onTime = sensor["time_on"]
        with open(f'config.h', 'a') as configH:
            configH.write(template.render(sensorName=sensorName, onPower=onPower, offPower=offPower, actTime=actTime, onTime=onTime))
        configH.close()
        possibleNewMax = int(actTime) + int(onTime)
        if possibleNewMax > sensorsEndAt:
            sensorsEndAt = possibleNewMax
        
# define params for MCU
with open('./templates/templateMCU.txt') as templateMCU:
    template = Template(templateMCU.read())
    mcu = settings["mcu"]
    mcu_p1 = mcu["mcu_p1"]
    mcu_p2 = mcu["mcu_p2"]
    mcu_t1 = mcu["mcu_t1"]
    mcu_t2 = mcu["mcu_t2"]
    mcu_idle = mcu["mcu_idle"]
    mcu_act_time = sensorsEndAt + 1
    with open(f'config.h', 'a') as configH:
        configH.write(template.render(mcu_p1=mcu_p1, mcu_p2=mcu_p2, mcu_t1=mcu_t1, mcu_t2=mcu_t2, mcu_idle=mcu_idle, mcu_act_time=mcu_act_time))
    configH.close()
    mcuEndAt1 = int(mcu_act_time) + int(mcu_t1)
    mcuEndAt2 = int(mcu_act_time) + int(mcu_t2)

# define params for RF
with open('./templates/templateRF.txt') as templateRF:
    template = Template(templateRF.read())
    rf = settings["rf"]
    rf_p1 = rf["rf_p1"]
    rf_p2 = rf["rf_p2"]
    rf_t1 = rf["rf_t1"]
    rf_t2 = rf["rf_t2"]
    rf_idle = rf["rf_idle"]
    rf_act_time1 = mcuEndAt1 + 1
    rf_act_time2 = mcuEndAt2 + 1
    with open(f'config.h', 'a') as configH:
        configH.write(template.render(rf_p1=rf_p1, rf_p2=rf_p2, rf_t1=rf_t1, rf_t2=rf_t2, rf_idle=rf_idle, rf_act_time1=rf_act_time1, rf_act_time2=rf_act_time2))
    configH.close()

### converterX.h ###

with open('./templates/templateConverterH.txt') as templateConverterH:
    template = Template(templateConverterH.read())
    sensorID = 0
    for sensor in activeSensors:
        sensorID += 1
        with open(f'converter{sensorID}' + '.h', 'w') as converterH:
            converterH.write(template.render(sensorID=sensorID))
    templateConverterH.close()

### converterX.cpp ###

with open('./templates/templateConverterCpp.txt') as templateConverterCpp:
    template = Template(templateConverterCpp.read())
    sensorID = 0
    for sensor in activeSensors:
        sensorID += 1
        with open(f'converter{sensorID}' + '.cpp', 'w') as converterCpp:
            converterCpp.write(template.render(sensorID=sensorID))
    templateConverterCpp.close()

### main.cpp ###

with open('./templates/templateMainCpp.txt') as templateMainCpp:
    template = Template(templateMainCpp.read())
    with open("main.cpp", "w") as mainCpp:  
        activeSensors = settings["sensors"]
        sensorNames = []
        sensorID = 0
        for sensor in activeSensors:
            sensorID += 1
            sensorNames.append(sensorID) 
        mainCpp.write(template.render(activeSensors=sensorNames))