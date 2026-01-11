import numpy as np
import matplotlib.pyplot as plt

"""
Obliczenia zmiany położenie robota: odometria

Mamy do dyspozycji 4 czujniki pomiarowe:
-dwa enkodery dla każdego z kół, pomira obrotów na sekunde
-akcelerometr do pomiaru przyspieszenie robota
-żyroskop do pomiaru prędkości kątowej robota

Zaczniemy od przetworzenia danych z enkoderów:
(wyprowadzenie wzorów i uzupełnienie znadują się na stronie 76)

Mając pomiar prędkości obrotowej z kół w_i możemy policzyć przemieszczenie koła ze wzoru:

    d_i = 2*pi*r*w_i(t)*dt ; i:l,r

    r - promień koła[cm],
    w_i(t) - pedkosc oborotwa koła [obr/s],
    dt - próbkowkowanie czasu, co ile wierzymy prędkość [s].

Robot posiada trzy stopnie swobody polozenie wzdłóż osi x, y oraz kąt oborotu wokół własnej osi
Inczej możemy nazwać to jego posturą zapisując: (x[cm],y[cm],phi[stopnie])

Żeby policzyć zmianę postury musimy przyjąć następujace założenie:

    -przemieszczenie jest dość małe żeby móc przybliżyć wartość kąta wartościami długości
    -wynika z powyzszego ze musimy mieć częsty pomiar prędkości obrotowej

Wzory: 

    1) theta = (d_r - d_l)/b 

     theat - kąt o jaki zmienia swoją posture robot,
     b - odległość miedzy kołami

    2) d_c = (d_l +d_r)/2

     d_c - wartość przemieszczenie środka robota

    3) d_x = d_c*cos(phi+theta)

     d_x - zmiana polozenie wzloz osi x

    4) d_y = d_c*sin(phi+theta)

"""

#pomiary z czujników
dataFromLeftWheel = np.array([1,1,1,1,1]) #obr/s
dataFromRightWheel = np.array([1,1,1,1,1]) #obr/s
dataFromAccelerator = np.array([])
dataFromGyroscope = np.array([])
timeStep = 0.2 #czas co jaki pobierana jest wartosc z czujników
radiusOfWheel = 5 #cm
distanceBetweenwheels = 20 #cm

#wyznaczenie chwilowych zmian przemieszczenia
distanceLeftWheel = 0
distanceRightWheel = 0
vecTemporaryDistanceLW = np.array([])
vecTemporaryDistanceRW = np.array([])

for i in range(min(len(dataFromLeftWheel),len(dataFromRightWheel))):
    dl = np.pi * radiusOfWheel * 2 * dataFromLeftWheel[i] * timeStep
    dr = np.pi * radiusOfWheel * 2 * dataFromRightWheel[i] * timeStep
    vecTemporaryDistanceLW = np.append(vecTemporaryDistanceLW,dl)
    vecTemporaryDistanceRW = np.append(vecTemporaryDistanceRW,dr)

#obliczanie zmiany pozycji
posX = np.array([100]) #cm
posY = np.array([0])
phi = np.array([90]) #stopnie

for i in range(len(dataFromLeftWheel)):

    #theta = (d_r - d_l)/b
    theta = (vecTemporaryDistanceRW[i]-vecTemporaryDistanceRW[i])/distanceBetweenwheels
    phi = np.append(phi,phi[i]+theta)

    #d_c = (d_l +d_r)/2
    d_c = (vecTemporaryDistanceRW[i]+vecTemporaryDistanceRW[i])/2

    d_x = d_c * np.cos((phi[i]+theta)*(np.pi/180))
    d_y = d_c * np.sin((phi[i]+theta)*(np.pi/180))
    posX = np.append(posX,posX[i]+d_x)
    posY = np.append(posY,posY[i]+d_y)

    print(f"postura: (x:{posX[i]}, y:{posY[i]}, phi:{phi[i]}), d_x = {d_x}, d_y = {d_y}, theta = {theta}",end='\n')


#wizulaizacjas
plt.figure(figsize=(8,8))
plt.plot(posX,posY,label='Wizualizacja przemieszczenia sie robota')
plt.grid()
plt.show()



