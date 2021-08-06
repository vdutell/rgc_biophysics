import numpy as np
from neuron import h
from neuron.units import ms, mV

#from mod files - removed for now
#import spike
#import capump

def calc_temporal_sin(temp_fq_hz, len_ms, n_timepoints, amplitude):
    '''
    Function to calculate a temporal sine wave for neuron stimluation

    Input:
        temp_fq_hz (int): Temporal frequency at which to modulate sime wave
        len_ms (int): Length of stimulation in miliseconds
        n_timepoints (int): Number of timepoints
        amplitude (int): Amplitude of stimulation
    Returns:
        timepoints (1D numpy array): Timepoint vector
        sin_stim_vec (1D numpy array, float32): Sine wave stim vector of stim values (in seconds)
    '''

    timepoints = np.linspace(0, len_ms, n_timepoints)
    sin_stim_vec = np.sin(2*np.pi*(temp_fq_hz/1000. * timepoints))*amplitude #calculate sine wave
    return(timepoints, sin_stim_vec)

# h.load_file('rgc_alpha_noax.hoc')

# #specify cell from morphology and conductance files
class RGC:
    def __init__(self, morph_fname, gid, soma_size_multiplier):
        self._gid = gid
        self.morph_fname = morph_fname
        self.soma_size_multiplier = soma_size_multiplier
        self._setup_morphology()
        #self._setup_biophysics() #need to debug this, why are realistic ion channels from .mod files not working?
        self._setup_biophysics_hh()
    def _setup_morphology(self):


#         self.soma = h.Section(name='soma', cell=self)
#         self.dend1 = h.Section(name='dend1', cell=self)
#         self.dend2 = h.Section(name='dend2', cell=self)
#         self.all = [self.soma, self.dend1, self.dend2]
#         self.dend1.connect(self.soma)
#         self.dend2.connect(self.soma)
        
        self.cell = h.Import3d_SWC_read()
        self.cell.input(self.morph_fname)
        i3d = h.Import3d_GUI(self.cell, 0)
        i3d.instantiate(None)
        #make section lists
        self.somalist = h.SectionList(s for s in h.allsec() if 'soma' in h.secname(sec=s))
        self.dendslist = h.SectionList(s for s in h.allsec() if 'dend' in h.secname(sec=s))
        self.all = h.SectionList(s for s in h.allsec())
        #self.all = [self.soma, self.dends]
    def _setup_biophysics_hh(self):
        #for sec in self.all:
        #    sec.Ra = 100    # Axial resistance in Ohm * cm
        #    sec.cm = 1      # Membrane capacitance in micro Farads / cm^2
        #self.soma.insert('hh')
        for sec in self.somalist:
            sec.insert('hh')
            #print(dir(seg))
            for seg in sec:
                seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
                seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
                seg.hh.gl = 0.0003    # Leak conductance in S/cm2
                seg.hh.el = -54.3     # Reversal potential in mV
            self.soma = sec
            self.soma.L = self.soma.diam = 200 * self.soma_size_multiplier 
        # Insert passive current in the dendrite                       # <-- NEW
        for sec in self.dendslist:  
            sec.insert('hh')# <-- NEW
            for seg in sec:
                seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
                seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
                seg.hh.gl = 0.0003    # Leak conductance in S/cm2
                seg.hh.el = -54.3     # Reversal potential in mV
                self.apicaldend = seg

#     def _setup_biophysics(self):
#         #properties common to all sections
#         for sec in self.all:
#             sec.Ra = 100    # Axial resistance in Ohm * cm
#             sec.cm = 1      # Membrane capacitance in micro 
#             #sec.insert('spike')
# #             sec.e_na = 35.0
# #             sec.e_k = -75
# #             sec.insert('cad')
# #             sec.g_pas = .000008
# #             sec.e_pas = -62.5
# #             sec.Ra=110
# #             sec.global_ra=110
#         #properties of soma only
#         self.soma.insert('hh')
#         self.soma.insert('ps')
#         for seg in self.soma:
#             seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
#             seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
#             seg.hh.gl = 0.0003    # Leak conductance in S/cm2
#             seg.hh.el = -54.3     # Reversal potential in mV
# #             seg.gcabar_spike = 0.00223
# #             seg.gkbar_spike = 0.0361
# #             seg.gabar_spike = 0.054
# #             seg.gkcbar_spike = 0.000065
# #             seg.gnabar_spike = 0.158
#         #properties of dendrites
#         #***NOTE** these are just copied from the 'narrowr' of the x/y cell data, should probably be updated
#         self.dends.insert('hh')
#         self.dends.insert('ps')
#         for seg in self.dends:
#             seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
#             seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
#             seg.hh.gl = 0.0003    # Leak conductance in S/cm2
#             seg.hh.el = -54.3     # Reversal potential in mV 
# #             seg.gcabar_spike = 0.0
# #             seg.gkbar_spike = 0.0467
# #             seg.gabar_spike = 0.0
# #             seg.gkcbar_spike = 0.000065
# #             seg.gnabar_spike = 0.4485

    def __repr__(self):
        return 'RGC[{}]'.format(self._gid)

class BallAndStick:
    def __init__(self, gid, soma_size_multiplier):
        self._gid = gid
        self.soma_size_multiplier = soma_size_multiplier
        self._setup_morphology()
        self._setup_biophysics()
    def _setup_morphology(self):
        self.soma = h.Section(name='soma', cell=self)
        self.dend = h.Section(name='dend', cell=self)
        self.all = [self.soma, self.dend]
        self.dend.connect(self.soma)
        self.soma.L = self.soma.diam = 200 * self.soma_size_multiplier #12.6157
        self.dend.L = 200
        self.dend.diam = 1
    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100    # Axial resistance in Ohm * cm
            sec.cm = 1      # Membrane capacitance in micro Farads / cm^2
        print('Ball and stick', self.soma)
        print(type(self.soma))
        self.soma.insert('hh')

        for seg in self.soma:
            seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
            seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
            seg.hh.gl = 0.0003    # Leak conductance in S/cm2
            seg.hh.el = -54.3     # Reversal potential in mV
        # Insert passive current in the dendrite                       # <-- NEW
        self.dend.insert('pas')                                        # <-- NEW
        for seg in self.dend:                                          # <-- NEW
            seg.pas.g = 0.001  # Passive conductance in S/cm2          # <-- NEW
            seg.pas.e = -65    # Leak reversal potential mV            # <-- NEW
    def __repr__(self):
        return 'BallAndStick[{}]'.format(self._gid)