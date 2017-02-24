from SimPy.Simulation import *
from numpy.random import seed, uniform
import sys, getopt, math

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

    lambdaP = 0.0 
    Ts = 0.0
    interarrivalTimeMin = 1.5
    interarrivalTimeMax = 3.5
    serviceTimeMin = 2.5
    serviceTimeMax = 6.5
    numberOfServers = 0
    simulationTime = 1
    distype = 0  # the type setting the distribution 0 = uniform, 1 = exponential
    



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
        print "Time %s: Packet %s arrived and about to join the queue" %(now(), self.name)
        yield request, self, cs
        print "Time %s: Packet %s is about to get its service initiated" %(now(), self.name)
        yield hold, self, model(1)
        yield release, self, cs
        print "Time %s: Packet %s service terminated and exists" %(now(), self.name)

# Packet Generator class.
class PacketGenerator(Process):
        def createPackets(self,cs):
            '''You must complete this method. This method generates and creates packets as per the
            arrival rate distribution defined'''
            name = 0
            while 1 :
                yield hold, self, model(0)
                p = Packet(str(name))
                activate(p, p.behavior_of_single_packet(cs))
                name += 1


#You do not need to modify this class.
class ComputingSystem(Resource):
    pass


#You can modify this model method#.
def model(s):
    # Seed the generator using seed value of 123.

    if Parameters.distype == 0:
        # this is the case for the uniform distribution
        # a,b should be the range of the uniform distribution
        if s == 0:
            # s is to mark if it is the service time or not
            seed(123)
            u = uniform(Parameters.interarrivalTimeMin, Parameters.interarrivalTimeMax)
            print u
            return u
        else:
            seed(123)
            u = uniform(Parameters.serviceTimeMin, Parameters.serviceTimeMax)
            print u 
            return u
    else:
        # this is the case for the exponential distribution
        # lam should be the lambda and the uniform distribution from 0,1
        if s == 0:
            seed(123)
            u = uniform()
            return -(math.log(1 - u)/ Parameters.lambdaP)
        else:
            return Parameters.Ts


# Argument parsing function
# getting from the python library website
def parsing(argv):
    if argv == []:
        print "System.py -h or --help for usage"
        sys.exit(2)
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
            if arg[0] == 'U' or arg[0] == 'u':
                print "distribution type: uniform"
                Parameters.disttype = 0
            elif arg[0] == 'M' or arg[0] == 'm':
                print "distribution type: exponential"
                Parameters.distype = 1
            else:
                print "invalid distribution type:", arg
                sys.exit(2)
            Parameters.numberOfServers = int(arg[2])
            print "Number of servers:", Parameters.numberOfServers 


#Change the below, as per the requirements of the assignment.
if __name__ == "__main__":
    parsing(sys.argv[1:])
    cs = ComputingSystem(capacity = 1)
    initialize()
    pg = PacketGenerator("pg")
    activate(pg, pg.createPackets(cs))
    simulate(until = 6)
    print ""
    print "Process finished with exits code 0"
    sys.exit(0)