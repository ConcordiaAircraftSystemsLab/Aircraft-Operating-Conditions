# Operating Conditions
# This object defines the classes and functions used to define the oprating conditions

import math
import numpy as np

class opCond():
    '''
    # Definition of the operating conditions
    name: name of the operating conditions
    T_env: Static temperature of the environment in °C and speficied by the user
    altitude: altitude of the aircraft in ft
    speed: aircraft speed in Ma
    time: time of the day (day or night)
    RH: Relative Humidity of air in %
    '''
    # Sea level reference conditions
    pressureSL = 101325.
    densitySL = 1.225
    temperatureSL = 15.
    g = 9.80665
    gamma = 1.4
    R = 287.04

    def __init__(self,
                name: str,
                T_env: float,
                altitude: float,
                speed: float,
                time: str,
                RH: float,
                *args,
                **kwargs):

        self.name = name
        self.T_env = T_env
        self.altitude = altitude
        self.speed = speed
        self.time = time
        self.RH = RH

    def pressure(self):
        # Ambient pressure in Pa
        altitudeMeter = self.altitude / 3.28084
        T_ISA_K = opCond.T_ISA(self) + 273.15
        return opCond.pressureSL * (1.-(0.0065*altitudeMeter/T_ISA_K))**5.255

    def T_ISA(self):
        # International Standard Atmosphere Temperature
        if self.altitude<=36000.:
            return opCond.temperatureSL - 1.98 * self.altitude / 1000.
        else:
            return -56.5

    def Ttot(self):
        # Total air temperature
        T_stat = self.T_env + 273.15
        return (1+((opCond.gamma-1)/2) * self.speed**2) * T_stat

    def solarLoad(self):
        # Solar heat flux outside the atmosphere
        Q_sun = 1367.

        if self.altitude == 0.:
            # Percentages of solar heat flux that reaches the earth surface
            # Direct to Earth = 0.7
            # Scattered to Earth = 0.07
            return 0.77 * Q_sun
        else:
            if self.altitude <= 10000.:
            # Percentages of solar heat flux that is available at 10000 feet
            # Direct to Earth = 0.7
            # Scattered to Earth = 0.07
            # Absorbed by the layers below 10000. = 0.07
                return 0.84 * Q_sun
            else:
            # Percentages of solar heat flux that is available at 10000 feet
            # Direct to Earth = 0.7
            # Scattered to Earth = 0.07
            # Absorbed by the layers below 30000. = 0.15
                return 0.92 * Q_sun

    def radSky(self):
        # Dew point Temperature
        dewTemp = -34.56 + 0.446 * self.RH + 0.873 * (opCond.Ttot(self)-273.15)
        # Sky emissivity
        skyEmissivity = 0.741 + 0.0062 * dewTemp
        # Stefan-Boltzmann Constant
        sigmaB = 5.67E-8

        return skyEmissivity * sigmaB * (opCond.Ttot(self) - 273.15)**4