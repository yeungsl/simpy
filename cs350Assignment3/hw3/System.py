from SimPy.Simulation import *
from numpy.random import seed, uniform
import math, argparse, sys

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

    lambdaP = 0.1 
    Ts = 8.0
    mu = 1.0/Ts
    interarrivalTimeMin = 1.5
    interarrivalTimeMax = 3.5
    serviceTimeMin = 2.5
    serviceTimeMax = 6.5
    numberOfServers = 0
    simulationTime = 120 #change this to modify the range of time you wanted to record data
    distypeR = 0  # the type setting the distribution 0 = uniform, 1 = exponential for arrivel rate
    distypeS = 0  # the type setting the distribution 0 = uniform, 1 = exponential for service rate
    generateRawResults = False # chekc to make sure if running the expirement or not
    StedyTime = 120 # change this to modify the acutal time you wanted to run
    prevTime = StedyTime - simulationTime


data = []        
def record(t, cs):
    if t >= (Parameters.StedyTime- Parameters.simulationTime):
        data.append([t - Parameters.prevTime, len(cs.waitQ)])
        Parameters.prevTime = t

def avgQue(d, Tt):
    r = 0
    for e in d:
        r += e[0] * e[1]
    return r / Tt

def conditionalPrint(s):
    if Parameters.generateRawResults:
        return
    else:
        print s
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
        conditionalPrint("Time " + str(now()) + ": Packet "+ str(self.name) + " arrived and about to join the queue")
        arrive = now()
        record(arrive, cs)
        yield request, self, cs
        wait = now() - arrive
        #if now() >= (Parameters.StedyTime- Parameters.simulationTime):
        wM.observe(wait)
        conditionalPrint("Time " + str(now()) + ": Packet "+ str(self.name) +" is about to get its service initiated")
        if Parameters.distypeS == 0:
            u = uniform(Parameters.serviceTimeMin, Parameters.serviceTimeMax)
        elif Parameters.distypeS == 1:
            u = -(math.log(1 - uniform())/ Parameters.mu)
        else:
            u = Parameters.Ts
        yield hold, self, u
        yield release, self, cs
        conditionalPrint("Time "+ str(now()) + ": Packet "+ str(self.name) +" service terminated and exists")
        record(now(), cs)

# Packet Generator class.
class PacketGenerator(Process):
        def createPackets(self,cs):
            '''You must complete this method. This method generates and creates packets as per the
            arrival rate distribution defined'''
            name = 0
            while True :
                if Parameters.distypeR == 0:
                    u = uniform(Parameters.interarrivalTimeMin, Parameters.interarrivalTimeMax)
                else:
                    u = -(math.log(1 - uniform())/ Parameters.lambdaP)
                yield hold, self, u
                p = Packet(str(name))
                activate(p, p.behavior_of_single_packet(cs))
                name += 1


#You do not need to modify this class.
class ComputingSystem(Resource):
    pass


#You can modify this model method#.
def model():
    # Seed the generator using seed value of 123.
    seed(123)
    cs = ComputingSystem(capacity = Parameters.numberOfServers, monitored = True)
    initialize()
    pg = PacketGenerator("pg")
    activate(pg, pg.createPackets(cs))
    simulate(until = Parameters.StedyTime)
    conditionalPrint("")
    conditionalPrint("Process finished with exits code 0")
    #conditionalPrint("Average waiting time was "+ str(wM.mean()) +" minutes.")
    #print "Average queue lengthe was %f packets. " %cs.waitMon.timeAverage()
    r = avgQue(data, Parameters.simulationTime)
    #conditionalPrint("Average queue length was "+ str(r) +" packets.")
    #print cs.waitMon.timeAverage()
    #print len(data)
    return r


# Argument parsing function
# getting from the python library website
def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("-generateRawResults", help="get the raw results", action="store_true")
    parser.add_argument("--type", help="the type of distribution wanted to simulate")    
    args = parser.parse_args()
    if args.type[0] == 'U' or args.type[0] == 'u':
        #print "distribution type: uniform"
        Parameters.distypeR = 0
        Parameters.distypeS = 0
    elif args.type[0] == 'M' or args.type[0] == 'm':
        #print "distribution type: exponential"
        Parameters.distypeR = 1
        Parameters.distypeS = 1
    else:
        print "invalid distribution type:", args.type
        sys.exit(2)
    Parameters.numberOfServers = int(args.type[2])
    #print "Number of servers:", Parameters.numberOfServers
    
    if args.generateRawResults:
        Parameters.generateRawResults = True
        Parameters.distypeS = 2
    return


#Change the below, as per the requirements of the assignment.
if __name__ == "__main__":
    parsing()
    wM = Monitor()
    if Parameters.generateRawResults:
        i = 0
        while i <= 11:
            Parameters.Ts = i
            for j in range(0, 10):
                m = model()
                print "%f,%f" %(i, m)
            i += 0.5
    else:
        model()
    sys.exit(0)