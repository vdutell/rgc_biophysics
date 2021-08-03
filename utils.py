import numpy as np
from neuron import h
from neuron.units import ms, mV

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
# class RGC:
#     def __init__(self, morph_fname, gid):
#         self._gid = gid
#         self.morph_fname = morph_fname
#         self._setup_morphology()
#         self._setup_biophysics()
#     def _setup_morphology(self):
#         self.soma = soma #morph_params.soma
#         #self.initseg = morph_params.initset
#         #self.narrowr = morph_params.narrowr
#         #self.soma = h.Section(name='soma', cell=self)
#         #self.dend = h.Section(name='dend', cell=self)
#         self.all = [self.soma, self.initseg, self.narrowr]
#     def _setup_biophysics(self):
        
#         for seg in self.soma:
#             seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
#             seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
#             seg.hh.gl = 0.0003    # Leak conductance in S/cm2
#             seg.hh.el = -54.3     # Reversal potential in mV
#         # Insert passive current in the dendrite                       # <-- NEW
#         self.dend.insert('pas')
#         for seg in self.dend:                                          # <-- NEW
#             seg.pas.g = 0.001  # Passive conductance in S/cm2          # <-- NEW
#             seg.pas.e = -65    # Leak reversal potential mV            # <-- NEW
#     def __repr__(self):
#         return 'BallAndStick[{}]'.format(self._gid)

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