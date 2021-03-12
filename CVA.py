import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
a = 0.10; # Mean reversion
b = 0.05; # Equilibrium
r0 = 0.05; # Spot Rate
sigma_ir = 0.01;
SwapRate = 0.05;
numSteps = 40;
numSimulations = 1000;
dt = 0.25;

T = np.arange(0,10.25,0.25)
Z = np.random.standard_normal(size=[numSimulations,numSteps])*np.sqrt(0.25)*sigma_ir

def ComputeAB(a, b, T, sigma_ir):
    B = (1 - np.exp(-a*T))/a;
    A = np.exp( (B - T) *(b - sigma_ir**2/(2*a**2)) - sigma_ir**2 * B**2/(4*a));
    return A,B

A,B = ComputeAB(a, b, T, sigma_ir)

#Create rate matrix
RateMat = np.zeros((numSteps+1,6),float)

#Initialise rate matrix
RateMat[0][2] = r0
RateMat[:,0]= np.arange(0,numSteps+1,1)
RateMat[:,1] = np.arange(0,10.25,0.25)

SimMat=np.zeros((numSteps+1,numSimulations),float)

for i in range(0,numSimulations):
    DFMat = np.zeros((numSteps,numSteps),float)

    for j in range(1,numSteps + 1):
        RateMat[j][2] = RateMat[j-1][2]+ a*(b -RateMat[j-1][2])*0.25+Z[i][j-1]

    for j in range(0,numSteps ):
        for k in range(0,numSteps-j):
            DFMat[j][k] = A[k+1]*np.exp(-B[k+1]*RateMat[j][2])

    for j in range(0,numSteps ):
        RateMat[j,3] = SwapRate*0.25*DFMat.sum(axis = 1)[j]
        RateMat[j,4] = 1 - DFMat[j,numSteps -1 - j]
        RateMat[j,5] = (RateMat[j,3] - RateMat[j,4])
        SimMat[j,i]  = RateMat[j,5]


EE = np.zeros((numSteps+1),float)
PFE= np.zeros((numSteps+1),float)

PFE = np.percentile(SimMat,95,axis=1)
SimMat[SimMat<=0] =0
EE = SimMat.sum(axis = 1)/numSimulations

fig = plt.figure()
plt.style.use('dark_background')
fig.suptitle('MonteCarlo Simulation of Interest Rate Swap', fontsize=14, fontweight='bold' )
line_pfe = plt.plot(PFE,linestyle='-', marker='o', label='Potential Future Exposure')
line_ee = plt.plot(EE,linestyle='-', marker='o', label='Expected Exposure')
plt.grid()
plt.xlabel('Time Point : Unit Quarter Year')
plt.ylabel('% Exposure')
plt.show()

print ("                           Max PF Value is", PFE.max())
print ("                          Average of the EE is", EE.mean())

print("\n\n                                Simulated PFE and EE")

print('_______________________________________________________________________________________________')

row = ['|Serial Number |','Time in Years |' ,'|Potential Future Exposure  |','Expected Exposure |']
print("{: >20} {: >20} {: >20} {: >20}".format(*row))
print('________________________________________________________________________________________________')

for i in range(0,numSteps + 1):
    row = [RateMat[i,0],RateMat[i,1], round(PFE[i],4),round(EE[i],4)]
    print("{: >20} {: >20} {: >20} {: >20}".format(*row))





