import sys, logging
from mapping.fimmdaException import * 

log = logging.getLogger(__name__)

def main(args):
	#input_file = " ".join(args[0:])
	input_file = args
	test = 123
	test2 = "dfef"
	#print input_file
	#print ERROR_101
	
	#e = FimmdaException(ERROR_101,"really")
	#raise e
	print "printing something here"
	log.info("at module_test.py {} {} ".format(test, test2))
	
if __name__ == "__main__":
	main(sys.argv[1:])
