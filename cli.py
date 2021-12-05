import sys

if len(sys.argv[1:]) == 0:
	print('Invalid usage (use -h for help)')
else:
	opt=sys.argv[1:][0]
	if len(sys.argv[1:]) == 2:
		num = float(sys.argv[1:][1])
		if opt == '-a' or opt == '--analog':
			print('your voltage is: ' + str(0.016456026104691296*num+0.21185720045950096))
		elif opt == '-v' or opt == '--voltage':
			print('your analog reading is: ' + str((num-0.21185720045950096)/0.016456026104691296))
		else:
			print('Invalid option (use -h for help)')
	elif opt == '-h' or opt == '--help':
		print('Usage: python conversion.py [OPTION] [VALUE]\n\nAvailable options:\n  -a, --analog; Converts analog data to voltage reading\n  -v, --voltage; Converts voltage reading to analog data\n  -h, --help; Displays this menu')
	else:
		print('Invalid usage (use -h for help)')