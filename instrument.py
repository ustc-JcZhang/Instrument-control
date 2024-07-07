import pyvisa

class KEIYHLEY_2182():
    def __init__(self, resource_name):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(resource_name)
        self.inst.write("*RST")

    # channel (ch): 1/2
    # range: 
    def set_range(self, ch=1, rng=":AUTO ON"):
        # self.inst.write(":SENS:CHAN " + str(ch))
        # self.inst.write(":SENS:FUNC " + "VOLT")
        if rng.isdigit():
            rng = ':UPP ' + str(rng)
        self.inst.write(":SENS:VOLT:CHAN" + str(ch) + ":RANG" + rng)
        
    # channel (ch): 1/2
    # sensor: TC / INT
    # ref: INT / 0 ~ 60
    # tco: J / K / T / E / N / S / R / B
    # uint: C / F / K
    def set_tco(self, sensor="TC", ref="INT", tco="J", uint="C"):
        # self.inst.write(":SENS:CHAN " + str(ch))
        # self.inst.write(":SENS:FUNC " + "TEMP")
        self.inst.write(":SENS:TEMP:TRAN " + sensor)
        if ref.isdigit():
            self.inst.write(":SENS:TEMP:RJUN:RSEL: SIM")
            self.inst.write(":SENS:TEMP:RJUN:SIM " + str(ref))
        else:
            self.inst.write(":SENS:TEMP:RJUN:RSEL " + ref)
        self.inst.write(":SENS:TEMP:TC: " + tco)
        self.inst.write(":SENS:UNIT:TEMP: " + uint)
        
    # channel (ch): 1/2
    # a_status: analog filter status, True (ON) / False (OFF)
    # d_status: digital filter status, True (ON) / False (OFF)
    # count: 0 ~ 100
    # type: MOV / REP
    # window: 0 ~ 10
    # auto_zero: True (ON) / False (OFF)
    # nplc: 0.01 ~ 50 (for 50Hz) / 0.01 ~ 60 (for 60Hz)
    # timeout unit: milliseconds
    # Note: Changing function or range causes the Filter to reset.
    def set_measure_parameter(self, ch=1, func="VOLT", a_status=False, d_status=False, count=10, type="MOV", window=0.01, auto_zero=False, nplc=5):
        status = {True: "ON", False: "OFF"}
        root = ":SENS:" + func + ":CHAN" + str(ch)
        self.inst.write(root + ":DFIL:COUNt " + str(count))
        self.inst.write(root + ":DFIL:TCON " + type)
        self.inst.write(root + ":DFIL:WIND " + str(window))
        self.inst.write(root + ":LPAS " + status[a_status])
        self.inst.write(root + ":DFIL " + status[d_status])
        self.inst.write(":SENS:" + func + ":NPLC " + str(nplc))
        self.inst.write(":SYST:AZER " + status[auto_zero])       
    
    # channel (ch): 1/2
    # func: VOLT / TEMP
    def select_measure(self, func="VOLT", ch=1, timeout=5000):
        self.inst.timeout = timeout
        self.inst.write(":SENS:FUNC " + func)
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


class KEIYHLEY_6221():
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
        



# =================================================================================================
# moudule test code
if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

    keiythley_2182 = KEIYHLEY_2182('GPIB0::1::INSTR')