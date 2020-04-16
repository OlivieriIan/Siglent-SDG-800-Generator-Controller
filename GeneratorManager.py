import pyvisa # need pip install pyvisa and pyvisa-py
import os
import time

class SDG800():
    def __init__(self, name = ""):
        self.rm = pyvisa.ResourceManager()
        self.generator = None

    def connect(self, name = ""):
        success = False
        if name == "":
            name = "USB0::0xF4ED::0xEE3A::NDG08CBC3R0018::INSTR"
        try:
            self.generator = self.rm.open_resource(name)
        except:
            success = False
        
        if self.requestID()[0:4] == "*IDN":
            success = True

        return success

    def requestID(self):
        """ Request the instrument's ID
        @precondition: device must be connected 
        """
        id = ""
        if self.generator != None:
            id = self.generator.query("*IDN?")
        return id

    def getDeviceList(self):
        """ Get the connected divices list. Useful to search for the resource 
        name used in pyvisa.ResourceManager().open_resource(<name>)
        """
        return self.rm.list_resources()
    
    def turnOff(self):
        self.generator.write("C1:OUTP OFF")

    def turnOn(self):
        self.generator.write("C1:OUTP ON")
        
    def setSignal(self, waveform="SINE", freq = 13560000, amp = 0.1,
                  modShape = None, arbWfName = "", modFreq = 1000, modDepth = 100):
        """ Set the SDG 830 to output the indicated signal
        
        @param waveform: Waveform of the base signal.
        Waves available: SINE, SQUARE, RAMP, PULSE, NOISE, ARB, DC, PRBS
        @param freq: Frequency (Hz) of the base signal.
        @param amp: Amplitude (Volts) of the base signal.
        @param modShape: Shape of the AM modulating wave.
        Waves available: SINE, SQUARE, TRIANGLE, UPRAMP, DNRAMP, NOISE, ARB
        Setting it to "" or None disables modulation
        @param arbWfName: name of the Arbitrary Waveform. Only valid if shape = "ARB" was set.
        Built-in waveforms: StairUp, StairDn, StairUD ... (check the generator manual)
        Stored waveforms: "HLO", "LHO", "HL" (must be saved first. Read warning and note below)
        @param modFreq: Frequency (Hz) of the modulating signal (with arbitrary waveform shape) 
        
        
        @warning: IMPORTANT. If using an user-defined ARB modulation shape, 
        the waveform name passed must be valid (must be already stored in the
        generator's memory)
        
        @note: Apparently, there is a way to save the waveform inside the device with the command: 
        C1:WVDT <Mn>,WVNM,<wave_name>,TYPE,5,LENGTH,<length>,WAVEDATA, <data>
        But I was not able to make it work. 
        Therefore, in order to save an arb waveform it must be manually copied in the generator
        memory. 2 signal examples, HLO.csv and LHO.csv are saved inside this folder for reference.
        They were created using the software Siglent EasyWave. The official free version can
        be downloaded from: https://www.siglent.eu/firmware-waveform-generators.
        To copy the signals to the generator put them in an USB, insert it into the generator and:
        - Press Store/Recall
        - Change the FileType from State to Data
        - Navigate to the USB/ USB folder. The left arrow under the freq knob will expand folders
        - When the right folder is selected, Change Browser from Folder to File
        - Select the desired file and press Recall
        - Select the place to store them and press Save
        """
        sleepTime = 0.5 # Seconds. If too small (< 0.2) commands might fail
        
        # Turn off the generator output 
        self.turnOff()
        time.sleep(sleepTime)
        # Set the arbitrary signal that will modulate the carrier wave.
        # NOTE: with this command the output type will be set to be an Arbitrary
        # waveform, and that's the reason why the output is turned off first.
        # ATM there is no known way to change the AM modulation wave
        # of an arbitrary waveform without setting it like this first. 
        if modShape == "ARB":
            if arbWfName != "":
                self.generator.write("C1:ARWV NAME, " + arbWfName)
                time.sleep(sleepTime)
            else:
                modShape = "SQUARE"

        # Set the carrier waveform to a Sine wave
        self.generator.write("C1:BSWV WVTP," + waveform + ", FRQ," + str(freq) 
                             + ", AMP," + str(amp) + ", OFST,0V, PHSE,0")
        time.sleep(sleepTime)
        
        # Turn on AM modulation, with Frequency 1KHz, depth 100%, and Modulation
        # wave/Shape = Arbitrary 
        # Since the arbitrary waveform shape was selected before,
        # it will default to that one
        if (modShape != None) & (modShape != ""):
            self.generator.write("C1:MDWV AM, STATE,ON, SRC,INT, DEPTH," + 
                                 str(modDepth) + ", MDSP," + modShape +
                                 ", FRQ," + str(modFreq))

if __name__ == "__main__":

    gen = SDG800()
    gen.getDeviceList()
    # #gen.setSignal(freq = 13560000, amp = 0.1, modShape = "ARB", arbWfName = "HLO", modFreq = 1000, turnOn = False)
    # gen.setSignal(freq = 13560000, amp = 0.1, modShape = "SQUARE", modFreq = 1000, turnOn = True)
    # #gen.setSignal(freq = 13560000, amp = 0.1, modShape = None, turnOn = True)
    # time.sleep(5)
    
    #gen.turnOn()
