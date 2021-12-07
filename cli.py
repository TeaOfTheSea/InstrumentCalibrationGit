import sys
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

def calibrate(data):
    if len(sys.argv[1:]) == 4:
        #import the PressureSensorData
        sensorData = pd.read_csv('PressureSensorData.csv')
        
        #update it
        sensorData.loc[-1] = [data[0], data[1], data[2], data[3]]
        sensorData.to_csv('PressureSensorData.csv', index=False)
        
    #elif len(sys.argv[1:]) == 3:
    else: print('Invalid usage (use -h for help)')
#math to generate numbers used for calculation
def theMath():
    #import the PressureSensorData
    sensorData = pd.read_csv('PressureSensorData.csv')

    #reformat the data
    sensorData.columns = ['testID', 'truePressure', 'analogPressure', 'voltage'] #renaming columns for easier understanding
    sensorData.set_index('testID') #indexing the table by the test ID

    #Build a model
    apvr = np.corrcoef(sensorData['analogPressure'], sensorData['voltage'])[0,1] #Analogue Pressure Voltage Correlation Coefficient
    apvSlopeOU = (apvr*np.std(sensorData['voltage']))/(np.std(sensorData['analogPressure']))
    apvInterOU = np.mean(sensorData['voltage']) - (apvSlopeOU*np.mean(sensorData['analogPressure']))


    #calculating standard deviations
    truePressureValues = sensorData['truePressure'].unique()
    voltagestdArr = []
    analogstdArr = []

    for i in truePressureValues:
        truePressureData = sensorData[sensorData['truePressure']==i]
        voltagestdArr.append(np.std(truePressureData['voltage']))
        analogstdArr.append(np.std(truePressureData['analogPressure']))

    voltagestd = np.mean(voltagestdArr)
    analogstd = np.mean(analogstdArr)
    
    return apvr, apvSlopeOU, apvInterOU, voltagestd, analogstd

#Actual CLI arguments
if len(sys.argv[1:]) == 0:
    print('Invalid usage (use -h for help)')
else:
    opt=sys.argv[1:][0]
    if(opt == '-c' or opt == '--calibrate'):
        calibrate(sys.argv[1:])
    elif len(sys.argv[1:]) == 2:
        apvr, apvSlopeOU, apvInterOU, voltagestd, analogstd = theMath()
        num = float(sys.argv[1:][1])
        if opt == '-a' or opt == '--analog':
            print('We are 95% confident that the voltage is within ' + str(apvSlopeOU*num+apvInterOU-2*voltagestd) + ' and ' + str(apvSlopeOU*num+apvInterOU+2*voltagestd) + '.')
        elif opt == '-v' or opt == '--voltage':
            print('We are 95% confident that the analog reading is within ' + str(((num-apvInterOU)/apvSlopeOU)-2*analogstd) + ' and ' + str(((num-apvInterOU)/apvSlopeOU)+2*analogstd) + '.')
        else:
            print('Invalid option (use -h for help)')
    elif opt == '-h' or opt == '--help':
        print('Usage: python cli.py [OPTION] [VALUE(S)]\n\nAvailable options:\n  -a, --analog; Converts analog data to voltage reading\n  -v, --voltage; Converts voltage reading to analog data\n  -c, --calibrate; Provide a True Pressure, an Analog Pressure, and a Voltage\n  -h, --help; Displays this menu')
    else:
        print('Invalid usage (use -h for help)')