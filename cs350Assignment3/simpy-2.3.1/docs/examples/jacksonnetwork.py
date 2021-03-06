"""
  jacksonnetwork.py

  Messages arrive randomly at rate 1.5 per second
  at a communication network with 3 nodes
  (computers). Each computer (node) can queue
  messages. Service-times are exponential with
  mean m_i at node i. These values are given in
  the column headed n_i in the table below.  On
  completing service at node i a message transfers
  to node j with probability p_ij and leaves the
  system with probability p_i3.
   
  These transition probabilities are as follows:
    Node     m_i  p_i0   p_i1  p_i2    p_i3  
     i                                (leave)   
     0       1.0   0      0.5  0.5     0     
     1       2.0   0      0    0.8     0.2  
     2       1.0   0.2    0    0       0.8  
   
  Your task is to estimate
  (1) the average time taken for jobs going
      through the system and
  (2) the average number of jobs in the system.
   
"""
from SimPy.Simulation import *
##from SimPy.SimulationTrace import *
import random as ran

## Model components ------------------------

def choose2dA(i,P):
    """  return a random choice from a set j = 0..n-1
       with probs held in list of lists P[j] (n by n)
       using row i
       call:  next = choose2d(i,P)
    """
    U = ran.random()
    sumP = 0.0
    for j in range(len(P[i])):  # j = 0..n-1
        sumP +=  P[i][j]
        if U < sumP: break
    return(j)

class Msg(Process):
    """a message."""
    noInSystem=0
    def execute(self,i):
        """ executing a message """
        startTime = now()
        Msg.noInSystem += 1
        ##print "DEBUG noInSystm = ",Msg.noInSystem
        NoInSystem.observe(Msg.noInSystem)
        self.trace("Arrived node  %d"%(i,))
        while i <> 3:
            yield request,self,node[i]
            self.trace("Got node %d"%(i,))
            st = ran.expovariate(1.0/mean[i])
            yield hold,self,st
            yield release,self,node[i]
            self.trace("Finished with %d"%(i,))
            i = choose2dA(i,P)
            self.trace("Transfer to   %d"%(i,))
        TimeInSystem.tally(now()-startTime)        
        self.trace(    "leaving       %d %d in system"%(i,Msg.noInSystem))
        Msg.noInSystem -= 1
        NoInSystem.accum(Msg.noInSystem)
        
    def trace(self,message):
        if MTRACING: print "%7.4f %3s %10s"%(now(),self.name, message)


class MsgSource(Process):
   """ generates a sequence of msgs """    
     
   def execute(self,rate,maxN):
       self.count=0   # hold number of messages generated
       self.trace("starting MsgSource")
       while  (self.count < maxN):
           self.count+=1
           p = Msg("Message %d"%(self.count,))
           activate(p,p.execute(startNode))
           yield hold,self,ran.expovariate(rate)
       self.trace("generator finished with "+`self.count`+" ========")

   def trace(self,message):
       if GTRACING: print "%7.4f \t%s"%(now(), message)

## Experiment data -------------------------

rate = 1.5        ## arrivals per second
maxNumber = 1000  ## of Messages
GTRACING = False ## tracing Messages Source?

startNode = 0     ## Messages always enter at node 0
ran.seed(77777)
MTRACING =  False ## tracing Message action?

TimeInSystem = Monitor("time")
NoInSystem =   Monitor("Number")

node = [Resource(1),Resource(1),Resource(1)]

mean=[1.0, 2.0, 1.0]       ## service times, seconds
P = [[0,   0.5, 0.5, 0  ], ## transition matrix P_ij
     [0,   0,   0.8, 0.2],
     [0.2, 0,   0,   0.8]]

## Model/Experiment ------------------------------

initialize()
g = MsgSource(name="MsgSource")
activate(g,g.execute(rate,maxNumber))
simulate(until=5000.0)

## Analysis/output -------------------------

print 'jacksonnetwork'
print "Mean number in system = %10.4f"%(NoInSystem.timeAverage(),)
print "Mean delay in system  = %10.4f"%(TimeInSystem.mean(),)
print "Total time run        = %10.4f"%(now(),)
print "Total jobs arrived    = %10d"%(g.count)
print "Total jobs completed  = %10d"%(TimeInSystem.count(),)
print "Average arrival rate  = %10.4f"%(g.count/now(),)


# jacksonnetwork.py:  Jackson network Littles law
# pyt090b.py. See sms090b.tex for simscript version
#        updated and simplified, 2004 Dec gav
#        $Author$    $Revision$
#        $Date$ 
