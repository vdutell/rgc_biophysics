import utils as utils
from neuron import h
from neuron.units import ms, mV
import matplotlib.pyplot as plt

h.load_file('stdrun.hoc')


# load morphology and conductance properties from .hoc file
#cell_conduct_fname = 'rgc_conduct.hoc'
#alpha_cell_morph = h.load_file('rgc_alpha_noax.hoc')
#beta_cell_morph = h.load_file('rgc_beta_noax.hoc')
#cell_morph = alpha_cell_morph #beta_cell_morph
#cell_conduct = h.load_file('rgc_conduct.hoc')

# set timing properties of cell stimulation
stim_fq_hz = 100
stim_fq_amp = 10
dt_ms = 0.01
dur_ms = 100
timesteps = int(dur_ms / dt_ms)
#get time and stim vector
time_vec, stim_vec = utils.calc_temporal_sin(stim_fq_hz, dur_ms, timesteps, stim_fq_amp)

#create current clamp
def create_stim(soma_size_multiplier=1):
    #specify cell
    #my_cell = utils.RGC('rgc_alpha_noax.hoc', 0)
    my_cell = utils.BallAndStick(0, soma_size_multiplier)
    #create current clamp - midget cell
    stim = h.IClamp(my_cell.dend(1))
    stim.delay = 0
    stim.dur = 1e9
    VecTime = h.Vector(time_vec)
    VecStim = h.Vector(stim_vec)
    VecStim.play(stim._ref_amp, VecTime, 1)

    #record from cell
    soma_v = h.Vector().record(my_cell.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    h.finitialize(-65 * mV)
    h.continuerun(dur_ms * ms)
    
    return(t, soma_v)

#midget_t_tenth, midget_v_tenth = create_stim(soma_size_multiplier=0.1)
midget_t_half, midget_v_half = create_stim(soma_size_multiplier=0.5)
midget_t, midget_v = create_stim(soma_size_multiplier=1)
midget_t_2x, midget_v_2x = create_stim(soma_size_multiplier=2)
midget_t_10x, midget_v_10x = create_stim(soma_size_multiplier=10)


#plot resuls

plt.figure(figsize=(10,10))

plt.subplot(2,1,1)
plt.plot(time_vec, stim_vec,'.')
plt.xlabel('Time (ms)')
plt.ylabel('Current (Amps)')
plt.title('Current Stimulation')
plt.subplot(2,1,2)
#plt.plot(midget_t_tenth, midget_v_tenth, label='soma 0.1x')
plt.plot(midget_t_half, midget_v_half, label='soma 0.5x')
plt.plot(midget_t, midget_v, label='soma 1x')
plt.plot(midget_t_2x, midget_v_2x, label='soma 2x')
plt.plot(midget_t_10x, midget_v_10x, label='soma 10x')
plt.xlabel('Time (ms)')
plt.ylabel('Soma Voltage (mV)')
plt.title(f'Cell Response to Sine Wave at {stim_fq_hz} Hz')
plt.legend()
plt.savefig(f'soma_voltage_{stim_fq_hz}hz.png')
#plt.show()

#print(time_vec, stim_vec)

# //Run parameters
# dt = 0.025
# dly = 1


# // Patch on soma
# objref siclamp
# soma siclamp = new IClamp(0.5)
# siclamp.amp = 0 // units n
# siclamp.dur = tstop // units ms
# siclamp.del = dly // units ms


# //patch on dendrites
# objref thisone, diclamp[segsize]
# id = 0

# forsec dends {
# 	thisone = new SectionRef()
# 	thisone diclamp[id] = new IClamp(0.5)
# 	diclamp[id].amp = 0 // units n
# 	diclamp[id].dur = tstop// units ms
# 	diclamp[id].del = dly // units ms
# 	id+=1
# }


# //calc sine wave stimulation as a fucntion of position and time
# func calc_sin() {
# 	xpos_um = $1
# 	time_ms = $2
# 	xpos_mm = xpos_um*1000

# 	temp_fq_ms = temp_fq_sec/1000 //convert temp fq from hz to cyc per ms
# 	cat_mmpdeg = 0.218 // vis_ang for cat: 1 deg = 0.218mm (Visual Perception: The Neurophysiological Foundations)
# 	spac_fq_mm = spac_fq_deg/cat_mmpdeg //convert spat fq from cpd to cyc per mm

# 	fx = xpos_mm*spac_fq_mm //spatial frequency component
# 	wt = time_ms*temp_fq_ms //temporal frequency component
# 	res = sin(2*PI*(fx-wt)) //calculate sine wave
	
# 	return(res)
# }


# //proc init(){
# //	Iin = 0
# //}

# proc advance() {
#  	fadvance()
#  	time_delayed = t-siclamp.del

#  	dends{ //for i=0,n3d()-1{
#  		i=0
#  		xcoord = x3d(i)
#  		sine_val = calc_sin(xcoord,t)
#  		dend[i] diclamp.amp = ampl+ampl*sine_val
 		
#  	}	
#  	Iin = ampl+ampl*sine_val
# }

# //init()

# proc pp() {
# 	spac_fq_deg = $1 //fq in cpd
# 	temp_fq_sec = $2 //fq in hz
# 	ampl = $3 //amplitude
# 	soma_multiplier = $4 //soma size multiplier

# 	soma_original = soma.diam
# 	soma.diam = soma_original*soma_multiplier

# 	init()
# 	advance()
# 	run()

# 	soma.diam = soma_original

# }

