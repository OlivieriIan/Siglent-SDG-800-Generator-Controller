try: # Python 3
    import tkinter as tk
    from tkinter import ttk
except: # Python 2
    import Tkinter as tk
    from Tkinter import ttk
import GeneratorManager

class GeneratorGUI():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Siglent SDG 800 Remote Controller")
        self.generator = GeneratorManager.SDG800()
        self.devices = self.generator.getDeviceList()

        self.onColor = "#5e9517"
        self.offColor = "#9b9b9b"
        self.errorColor = "#e65050"

        colSize = 15
        rowNum = 0
        
        ####### Connection #######
        rowNum += 1 # Go to next row
        self.device_frame = tk.LabelFrame(self.window, text="Device Connection")
        self.device_frame.grid(column=0, columnspan = 3, row=rowNum, padx=0, pady=15)
        rowNum += 1 # Go to next row
        colNum = 0
        self.device_list = ttk.Combobox(self.device_frame, width=colSize+10, values=self.devices)
        self.device_list.grid(column=colNum, row=rowNum)
        if(len(self.devices) > 0):
            self.device_list.current(0)
        colNum += 1
        self.device_refresh_btn = tk.Button(self.device_frame, width=colSize-5, text="Refresh List", command = self.refresh_devices)
        self.device_refresh_btn.grid(column=colNum, row=rowNum, padx=5, pady=5)
        colNum += 1
        self.device_connect_btn = tk.Button(self.device_frame, width=colSize-5, text="Connect", command = self.connect_to_device)
        self.device_connect_btn.grid(column=colNum, row=rowNum, padx=5, pady=5)
        rowNum += 1 # Go to next row
        colNum = 0
        self.device_status = tk.Label(self.device_frame,text="No device connected")
        self.device_status.grid(column=colNum, row=rowNum, columnspan = 3, padx=5, pady=5)

        ####### Base Signal #######
        rowNum += 1 # Go to next row
        self.base_signal_frame = tk.LabelFrame(self.window, text="Base Signal configuration")
        self.base_signal_frame.grid(column=0, columnspan = 3, row=rowNum, padx=5, pady=15)
        rowNum += 1 # Go to next row
        colNum = 0
        self.base_waveform_label = tk.Label(self.base_signal_frame, width=colSize, text="Waveform")
        self.base_waveform_label.grid(column=colNum, row=rowNum, padx=5, pady=5)
        colNum += 1
        self.base_freq_label = tk.Label(self.base_signal_frame, width=colSize, text="Frequency [Hz]")
        self.base_freq_label.grid(column=colNum, row=rowNum, padx=5, pady=5)
        colNum += 1
        self.base_freq_label = tk.Label(self.base_signal_frame, width=colSize, text="Amplitude [Volt]")
        self.base_freq_label.grid(column=colNum, row=rowNum, padx=5, pady=5)
        rowNum += 1 # Go to next row
        colNum = 0
        baseWaves = ["SINE", "SQUARE", "RAMP", "ARB"] #, "PULSE", "NOISE", "DC", "PRBS"]
        self.base_waveform = ttk.Combobox(self.base_signal_frame, width=10, values=baseWaves, state="readonly")
        self.base_waveform.current(0)
        self.base_waveform.grid(column=colNum, row=rowNum, padx=5, pady=5)
        colNum += 1
        self.base_freq = PosFloatEntry(self.base_signal_frame, limits=[0,30e6], width=10)
        self.base_freq.insert(tk.END, "13560000")
        self.base_freq.grid(column=colNum, row=rowNum, padx=5, pady=5)
        colNum += 1
        self.base_amp = PosFloatEntry(self.base_signal_frame, limits=[0,100], width=5)
        self.base_amp.insert(tk.END, "0.1")
        self.base_amp.grid(column=colNum, row=rowNum, padx=5, pady=5)

        ####### Modulating Signal #######
        rowNum += 1 # Go to next row
        self.mod_signal_frame = tk.LabelFrame(self.window, text="Modulating Signal configuration")
        self.mod_signal_frame.grid(column=0, columnspan = 3, row=rowNum, padx=5, pady=15)
        rowNum += 1 # Go to next row
        colNum = 0
        self.mod_signal_enabled = tk.BooleanVar()
        self.mod_signal_enabled.set(False)
        self.mod_signal_enable = tk.Checkbutton(self.mod_signal_frame,
                                                text="Enable",
                                                variable=self.mod_signal_enabled,
                                                command=self.enable_modulating_signal)
        self.mod_signal_enable.grid(column=0, row=rowNum, padx=5, pady=0, sticky=tk.W)
        rowNum += 1 # Go to next row
        colNum = 0
        self.mod_waveform_label = tk.Label(self.mod_signal_frame,  width=colSize, text="Waveform")
        self.mod_waveform_label.grid(column=colNum, row=rowNum, padx=5, pady=5)
        colNum += 1
        self.mod_freq_label = tk.Label(self.mod_signal_frame, width=colSize, text="Frequency [Hz]")
        self.mod_freq_label.grid(column=colNum, row=rowNum, padx=5, pady=5)
        colNum += 1
        self.mod_freq_label = tk.Label(self.mod_signal_frame, width=colSize, text="Depth [%]")
        self.mod_freq_label.grid(column=colNum, row=rowNum, padx=5, pady=5)
        
        rowNum += 1 # Go to next row
        colNum = 0
        modWaves = ["SINE", "SQUARE", "TRIANGLE", "UPRAMP", "DNRAMP", "ARB"] #"NOISE",
        self.mod_waveform = ttk.Combobox(self.mod_signal_frame, width=10, values=modWaves, state="disabled")
        self.mod_waveform.current(0)
        self.mod_waveform.grid(column=colNum, row=rowNum, padx=5, pady=5)
        self.mod_waveform.bind("<<ComboboxSelected>>", self.enable_arbWf_name)
        colNum += 1
        self.mod_freq = PosFloatEntry(self.mod_signal_frame, limits=[0,10e3], width=10, state="disabled")
        self.mod_freq.grid(column=colNum, row=rowNum, padx=5, pady=5)
        colNum += 1
        self.mod_depth = PosFloatEntry(self.mod_signal_frame, limits=[0,120], width=5, state="disabled")
        self.mod_depth.insert(tk.END, "100")
        self.mod_depth.grid(column=colNum, row=rowNum, padx=5, pady=5)

        rowNum += 1 # Go to next row
        colNum = 0
        self.mod_arb_name_label = tk.Label(self.mod_signal_frame, text="Arb. waveform name")
        self.mod_arb_name_label.grid(column=colNum, row=rowNum, padx=5, pady=5)
        self.mod_arb_name_label.grid_remove()
        colNum += 1
        self.mod_arb_name = tk.Entry(self.mod_signal_frame, width=15)
        self.mod_arb_name.grid(column=colNum, row=rowNum, padx=5, pady=5)
        self.mod_arb_name.grid_remove()

        ####### Configure Device #######
        rowNum += 1 # Go to next row
        colNum = 0
        self.send_btn = tk.Button(self.window,
                                  text="Send Configuration",
                                  command = self.send_configuration,
                                  state="disabled")
        self.send_btn.grid(column=colNum, row=rowNum, pady=10)
        ####### Turn Output on/off #######
        colNum += 1
        self.turnonoff_btn = tk.Button(self.window,
                                      text="Turn device output On/Off",
                                      command = self.turn_device_onoff,
                                      state="disabled",
                                      bg = self.offColor)
        self.turned_on = False
        self.turnonoff_btn.grid(column=colNum, row=rowNum, pady=10)

        ####### Close Window #######
        rowNum += 1 # Go to next row
        self.close_btn = tk.Button(self.window, text="Close", command = self.close_window)
        self.close_btn.grid(column=2, row=rowNum, pady=30)

        #self.window.geometry('380x480')

        self.window.mainloop()

    def connect_to_device(self):
        deviceName = self.device_list.get()
        connectionSuccessful = False

        if deviceName != "":
            connectionSuccessful = self.generator.connect()

        if connectionSuccessful == True:
            self.device_status['text'] = "Device connected successfully"
            self.device_status['bg'] = self.onColor
            self.send_btn.configure(state="normal")
            self.turnonoff_btn.configure(state="normal")
        else:
            self.device_status['text'] = "Connection error"
            self.device_status['bg'] = self.errorColor

    def refresh_devices(self):
        self.devices = self.generator.getDeviceList()
        self.device_list['values'] = self.devices
        if(len(self.devices) > 0):
            self.device_list.current(0)

    def send_configuration(self):
        # SDG800.setSignal turns the generator off so indicate that changing 
        # the turnonoff button color
        self.turned_on = False
        self.turnonoff_btn['bg'] = self.offColor
        # Initialize modulation variables in case modulation is not enabled
        modulationShape = None
        modulationFreq = 1000
        modulationDepth = 100
        arbWaveformName = ""
        if self.mod_signal_enabled.get() == True:
            modulationShape = self.mod_waveform.get()
            modulationFreq = int(self.mod_freq.get())
            modulationDepth = int(self.mod_depth.get())
            if modulationShape == "ARB":
                arbWaveformName = self.mod_arb_name.get()

        self.generator.setSignal(waveform = self.base_waveform.get(),
                                 freq = int(self.base_freq.get()),
                                 amp = float(self.base_amp.get()),
                                 modShape = modulationShape,
                                 arbWfName = arbWaveformName,
                                 modFreq = modulationFreq,
                                 modDepth = modulationDepth)

    def close_window(self):
        self.window.destroy()

    def turn_device_onoff(self):
        self.turned_on = not self.turned_on

        if self.turned_on == True:
            self.generator.turnOn()
            self.turnonoff_btn['bg'] = self.onColor
        else:
            self.generator.turnOff()
            self.turnonoff_btn['bg'] = self.offColor

    def enable_modulating_signal(self):
        state = ("disabled","normal")[self.mod_signal_enabled.get() == True]
        cbState = ("disabled","readonly")[self.mod_signal_enabled.get() == True]
        self.mod_waveform.configure(state = cbState)
        self.mod_freq.configure(state = state)
        self.mod_freq.insert(tk.END, "1000")
        self.mod_depth.configure(state = state)
        self.mod_depth.insert(tk.END, "100")
    
    def enable_arbWf_name(self, evt):
        if self.mod_waveform.get() == "ARB":
            self.mod_arb_name.grid()
            self.mod_arb_name.insert(tk.END, "StairDn")
            self.mod_arb_name_label.grid()
        else:
            self.mod_arb_name.grid_remove()
            self.mod_arb_name_label.grid_remove()
            

class PosFloatEntry(tk.Entry):
    """ Entry that only allows positive float numbers
    """
    def __init__(self, master=None, limits=None, **kwargs):
        """ FloatEntry constructor
        @param master: parent class
        @param limits: 2 element list with the limits of the Entry. eg [0, 100]
        @param kwargs: Entry arguments
        """
        self.limits = limits
        if self.limits != None:
            assert(len(self.limits) == 2)
            assert(self.limits[0] >= 0)

        self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_input = ''
        self.var.trace_variable('w', self.check)

    def check(self, *args):
        new_input = self.var.get()
        try:
            input_float = float(new_input)
            if (self.limits == None):
                self.old_input = new_input
            else:
                if (input_float >= self.limits[0]) & (input_float <= self.limits[1]):
                    self.old_input = new_input
                else:
                    self.var.set(self.old_input)
        except:
            # If the value entered is not valid (not a float, or outside limits)
            # use the old value stored
            self.var.set(self.old_input)

if __name__ == "__main__":
    # Launch the GUI
    gui = GeneratorGUI()
