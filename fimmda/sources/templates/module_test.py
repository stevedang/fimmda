import sys
from mapping.fimmdaException import * 

def main(args):
	#input_file = " ".join(args[0:])
	input_file = args
	#print input_file
	#print ERROR_101
	
	e = FimmdaException(ERROR_101,"really")
	raise e
if __name__ == "__main__":
	main(sys.argv[1:])
