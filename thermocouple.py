import numpy as np
import matplotlib.pyplot as plt

# global variables
TCOE_BELOW0 = [0.0000000E+00, 2.5929192E-02, -2.1316967E-07, 7.9018692E-10, 4.2527777E-13, 1.3304473E-16, 2.0241446E-20, 1.2668171E-24]
TCOE_ABOVE0 = [0.000000E+00, 2.592800E-02, -7.602961E-07, 4.637791E-11, -2.165394E-15, 6.048144E-20, -7.293422E-25]

# unit: uV, return: Kelvin
class Thermocouple:
    def __init__(self, cp_type, ref_tmp=0.0):
        self.cp_type = cp_type
        self.ref_tmp = ref_tmp

    def get_temperature(self, volt):
        volt = self.__correct(volt)
        if self.cp_type == 'T':
            if volt < 0:
                poly_func = np.poly1d(np.flipud(TCOE_BELOW0))
            else:
                poly_func = np.poly1d(np.flipud(TCOE_ABOVE0))
        return poly_func(volt)

    def __get_voltage(self, tmp):
        if self.cp_type == 'T':
            if tmp < 0:
                poly_coe = np.flipud(TCOE_BELOW0)
            else:
                poly_coe = np.flipud(TCOE_ABOVE0)
            poly_coe[-1] = -tmp
            roots = np.roots(poly_coe)
            # find the real root at the specific region
            for root in roots:
                if np.isreal(root) and (30000>root >-6000):
                    volt = root.real
                    break
        return volt

    def __correct(self, volt):
        correct_volt = self.__get_voltage(self.ref_tmp) + volt
        return correct_volt

if __name__ == '__main__':
    volt = np.linspace(-5603, 20872, 1000)
    tmp = np.zeros(len(volt))
    tc_1 = Thermocouple('T', 0)
    for i in range(len(volt)):
        tmp[i] = tc_1.get_temperature(volt[i])
    plt.plot(volt, tmp)

    tc_2 = Thermocouple('T', 100)
    for i in range(len(volt)):
        tmp[i] = tc_2.get_temperature(volt[i])
    plt.plot(volt, tmp)

    plt.xlabel('Voltage (uV)') 
    plt.ylabel('Temperature (Celcius)')
    plt.title('Thermocouple T')
    plt.grid()
    plt.show()
