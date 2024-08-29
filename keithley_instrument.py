import pyvisa

class KEITHLEY_2182():
    def __init__(self, resource_name):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(resource_name)
        self.inst.write("*RST")

    # channel (ch): 1/2
    # range (rng): 0 ~ 120
    def set_range(self, ch=1, rng="AUTO"):
        if isinstance(rng, (int, float)):
            rng = ":UPP " + str(rng)
        else:
            rng = ":AUTO ON"
        self.inst.write(":SENS:VOLT:CHAN" + str(ch) + ":RANG" + rng)
        
    # channel (ch): 1/2
    # sensor: TC / INT
    # ref: INT / 0 ~ 60
    # tco: J / K / T / E / N / S / R / B
    # unit: C / F / K
    def set_tco(self, sensor="TC", ref="INT", tco="J", unit="C"):
        self.inst.write(":SENS:TEMP:TRAN " + sensor)
        if isinstance(ref, (int, float)):
            self.inst.write(":SENS:TEMP:RJUN:RSEL SIM")
            self.inst.write(":SENS:TEMP:RJUN:SIM " + str(ref))
        else:
            self.inst.write(":SENS:TEMP:RJUN:RSEL " + ref)
        self.inst.write(":SENS:TEMP:TC " + tco)
        self.inst.write(":UNIT:TEMP " + unit)
        
    # channel (ch): 1/2
    # func: VOLT / TEMP
    # a_status: analog filter status, True (ON) / False (OFF)
    # d_status: digital filter status, True (ON) / False (OFF)
    # count: 0 ~ 100
    # type: MOV / REP
    # window: 0 ~ 10
    # auto_zero: True (ON) / False (OFF)
    # nplc: 0.01 ~ 50 (for 50Hz) / 0.01 ~ 60 (for 60Hz)
    # timeout unit: milliseconds
    # Note: Changing function or range causes the Filter to reset.
    def set_measure_parameter(self, ch=1, func="VOLT", a_status=False, d_status=False, count=10, f_type="MOV", window=0.01, auto_zero=False, nplc=5, timeout=5000):
        status = {True: "ON", False: "OFF"}
        root = ":SENS:" + func + ":CHAN" + str(ch)
        self.inst.write(root + ":DFIL:COUNt " + str(count))
        self.inst.write(root + ":DFIL:TCON " + f_type)
        self.inst.write(root + ":DFIL:WIND " + str(window))
        self.inst.write(root + ":LPAS " + status[a_status])
        self.inst.write(root + ":DFIL " + status[d_status])
        self.inst.write(":SENS:" + func + ":NPLC " + str(nplc))
        self.inst.write(":SYST:AZER " + status[auto_zero])   
        self.inst.timeout = timeout    
    
    # channel (ch): 1/2
    # func: VOLT / TEMP
    def select_measure(self, func="VOLT", ch=1):
        self.inst.write(":SENS:FUNC " + "'" + func + "'")
        self.inst.write(":SENS:CHAN " + str(ch))

    # return unit: volt (func="VOLT") / C,F or K (func="TEMP")
    def act_measure(self) -> float:
        volt = self.inst.query(":READ?")
        return float(volt)

    # user operation
    def user_command(self, string):
        self.inst.write(string)
    def user_query(self, string):
        ret = self.inst.query(string)
        return ret


class KEITHLEY_6221():
    def __init__(self, resource_name) -> None:
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(resource_name)
        self.inst.write("*RST")

    def set_output(self, curr, comp):
        self.inst.write("SOUR:CURR " + str(curr))
        self.inst.write("SOUR:CURR:COMP " + str(comp))

    def power_on(self):
        self.inst.write("OUTP ON")

    def power_off(self):
        self.inst.write("OUTP OFF")

    # user operation
    def user_command(self, string):
        self.inst.write(string)
    def user_query(self, string):
        ret = self.inst.query(string)
        return ret
    
class KEITHLEY_2400():
    def __init__(self, resource_name) -> None:
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(resource_name)
        self.inst.write("*RST")
        self.inst.write(":SYST:BEEP:STAT OFF")

    def measure_only_volt(self, cmpl=1, rng=0.2, nplc=10):
        self.inst.write(":SENS:VOLT:NPLC " + str(nplc))
        self.inst.write(":SOUR:FUNC CURR")
        self.inst.write(":SOUR:CURR:MODE FIXED")
        self.inst.write(":SENS:FUNC 'VOLT'")
        self.inst.write(":SOUR:CURR:RANG MIN")
        self.inst.write(":SOUR:CURR:LEV 0")
        self.inst.write(":SENS:VOLT:PROT " + str(cmpl))
        self.inst.write(":SENS:VOLT:RANG " + str(rng))
        self.inst.write(":FORM:ELEM VOLT")
        self.inst.write(":OUTP ON")

    def act_measure(self) -> float:
        volt = self.inst.query(":READ?")
        return float(volt)

# =================================================================================================
# moudule test code
if __name__ == "__main__":
    # rm = pyvisa.ResourceManager()
    # print(rm.list_resources())

    # keithley_2182 = KEITHLEY_2182('GPIB0::1::INSTR')
    # keithley_2182.set_range()
    # keithley_2182.set_tco()
    # keithley_2182.select_measure()
    # keithley_2182.set_measure_parameter()
    # keithley_2182.act_measure()

    keithley_2400 = KEITHLEY_2400('GPIB0::10::INSTR')
    keithley_2400.measure_only_volt()
    while True:
        print(keithley_2400.act_measure())
