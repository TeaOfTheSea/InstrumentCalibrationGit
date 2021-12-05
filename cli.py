import sys
import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np

#math to generate numbers used for calculation
#import the PressureSensorData
if sys.platform == 'darwin': #for Patrick's Mac because Tim Cook runs a terrible company
    sensorData = pd.read_csv('PressureSensorData.csv')
else:
    sensorData = pd.read_csv('../PressureSensorData.csv')

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

#Actual CLI arguments
if len(sys.argv[1:]) == 0:
	print('Invalid usage (use -h for help)')
else:
	opt=sys.argv[1:][0]
	if len(sys.argv[1:]) == 2:
		num = float(sys.argv[1:][1])
		if opt == '-a' or opt == '--analog':
			print('We are 95% confident that the voltage is within ' + str(apvSlopeOU*num+apvInterOU-2*voltagestd) + ' and ' + str(apvSlopeOU*num+apvInterOU+2*voltagestd) + '.')
		elif opt == '-v' or opt == '--voltage':
			print('We are 95% confident that the analog reading is within ' + str(((num-apvInterOU)/apvSlopeOU)-2*analogstd) + ' and ' + str(((num-apvInterOU)/apvSlopeOU)+2*analogstd) + '.')
		else:
			print('Invalid option (use -h for help)')
	elif opt == '-h' or opt == '--help':
		print('Usage: python cli.py [OPTION] [VALUE]\n\nAvailable options:\n  -a, --analog; Converts analog data to voltage reading\n  -v, --voltage; Converts voltage reading to analog data\n  -h, --help; Displays this menu')
	else:
		print('Invalid usage (use -h for help)')