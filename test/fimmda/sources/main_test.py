from mapping.fimmdaException import *
from templates import module_test, utilities
import sys, logging

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#logging.basicConfig(format='%(asctime)s  - [%(levelname)s] - %(message)s')
logging.basicConfig(format='%(asctime)s - [%(levelname)s][%(name)s] - %(message)s', stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)
#test_file = "sfdadf"
#print ERROR_101
#print ERROR_101, test_file
#module_test.main("fasdfafa asfdafa")

#maturity="0.25"
#print utilities.getMaturity(maturity)
#maturity="2.5"
#print utilities.getMaturity(maturity)
#maturity="3"
#print utilities.getMaturity(maturity)

def main():	
	#logging.basicConfig(filename='fimmda.log', level=logging.DEBUG)
	#logging.basicConfig(format='[%(asctime)s] - %(name) - %(message)s')
	#logger.warning("My message is very important")
	#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
	#logging.basicConfig(format='%(asctime)s  - [%(levelname)s] - %(message)s')
	#logger = logging.getLogger(__name__)	
	log.warning('at main.py')
	module_test.main("fasdfafa asfdafa")
	
if __name__ == '__main__':
    main()