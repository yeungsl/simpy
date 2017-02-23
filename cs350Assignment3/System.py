from SimPy.Simulation import *
from numpy.random import seed, uniform
import sys, getopt

# First Name: Sailung
# Last Name: Yeung
# BU ID: U73325730

#You can add any extra helper methods to these classes as you see fit#.


#You must modify this class#
class Parameters:
    '''In this class, you must just define the following variables of your distribution:
    These variables will be hardcoded with values. Please refer to the assignment handout what
    these values must be. You can use the values appropiately in your code by calling Parameters.NAME_OF_VARIABLE
    --For Poisson Arrivals and Exponential Service Time
      1) lambda for poisson arrivals
      2) Ts for service time

    --For Uniform Arrivals and Uniform Service Time
       3) interarrivalTimeMin and interarrivalTimeMax for Uniform distribution.
       4) serviceTimeMin and serviceTimeMax for Uniform distribution.
    5. numberOfServers in your computing system
    6. simulationTime in hrs. '''

    lambdaP = 0 
    Ts = 0
    interarrivalTimeMin = 1.5
    interarrivalTimeMax = 3.5
    serviceTimeMin = 2.5
    serviceTimeMax = 6.5
    numberOfServers = 0
    simulationTime = 1




##### Processes #####
# Customer
class Packet(Process):
    def behavior_of_single_packet(self,cs):
        '''You must implement this method. This method is the behavior of a single packet
        when it interacts with the queue of your computing system. These are some questions you will want to think about
        1. What happens when the packet arrives? Does it get serviced immediately or gets put in the queue?
        2. If it does get serviced, how long will it be serviced for? Or does it get put in the queue?
        3. When does it depart?

        The cs in the method is an instance of the Computing System class'''

        # Customer arrives, joins queue



# Packet Generator class.
class PacketGenerator(Process):
        def createPackets(self,cs):
            '''You must complete this method. This method generates and creates packets as per the
            arrival rate distribution defined'''


#You do not need to modify this class.
class ComputingSystem(Resource):
    pass


#You can modify this model method#.
def model():
    # Seed the generator using seed value of 123.
    seed(123)

# Argument parsing function
# getting from the python library website
def parsing(argv):
    try:
        opts, args = getopt.getopt(argv, "ht:", ["help=","type="])
    except getopt.GetoptError:
        print "System.py -h or --help for usage"
        sys.exit(2)
    for opt, arg in opts:
        if opt  in ("-h", "--help"):
            print "System.py -t or --type <SimulationModel>"
            sys.exit()
        elif opt in ("-t", "--type"):
            print "Simulation model is:", arg
            return arg

#Change the below, as per the requirements of the assignment.
if __name__ == "__main__":
    parsing(sys.argv[1:])
    model()
