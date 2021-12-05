# argv.py
import sys

print(f"Name of the script      : {sys.argv[0]=}")
print(f"Arguments of the script : {sys.argv[1:]=}")
print("argument 1 is " + sys.argv[1:][0])
print("argument 2 is " + sys.argv[1:][1])