import numpy as np
import matplotlib.pyplot as plt

dT = 0.01
accVect = np.array([1,2,1,2,1,1,2,1]) #dane pobrane w czsie rzeczywistem z akcelerometra
speedVect = np.array([])

for acc in accVect:
    instantSpeed = acc*dT
    speedVect = np.append(speedVect,instantSpeed)

print([speedVect])