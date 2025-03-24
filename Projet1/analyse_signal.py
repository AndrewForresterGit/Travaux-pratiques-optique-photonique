import numpy as np
from scipy.signal import square
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def start_at_0(time):
    return time-time[0]

def clock_signal(time):
    return np.where(square(time)<0, 0, 1)

def detect_edges(signal):
    return np.where(signal[:-1] != signal[1:])[0]+1

def slew_rate(time, stage_changes):
    slew_rate = (time[stage_changes[0]+1] - time[stage_changes[0]])/2
    return slew_rate

def detect_state_change(time, signal, threshold=None, display=False, save=None):
    if threshold is None:
        threshold = (np.max(signal) - np.min(signal))/2

    digital_sig = np.where(signal > threshold, 1, 0)
    state_change_indices = detect_edges(digital_sig)

    if save is not None:
        display = True
        
    if display:
        fig = plt.figure()
        ax_analog = fig.add_subplot(211)
        ax_digital = fig.add_subplot(212)
        
        ax_analog.scatter(time, signal, s=1)
        ax_analog.axhline(y=threshold, color='r', linestyle='--')
        ax_digital.plot(time, digital_sig)

        for change in time[state_change_indices]:
            ax_analog.axvline(x=change, color='g', alpha=0.5, linestyle='--')
        
        plt.show()
        
    return digital_sig, state_change_indices

def encode_message(message):
    enc_message = [i for i in map(bin, message.encode('utf-8'))]
    for i, byte in enumerate(enc_message):
        enc_message[i] = byte.replace('b', '').zfill(8)
        
    num_bytes = len(enc_message)
    if num_bytes == 1:
        len_message = 10
    else:    
        len_message = num_bytes*10+1
        
    return enc_message, num_bytes, len_message

def write_message(message, time, freq, delay):
    enc_message, num_bytes, len_message = encode_message(message)

    clock_time = np.linspace(0, len_message*np.pi/freq, 4*int(np.ceil(freq)))
    clock = clock_signal(freq*(clock_time - delay))
    edges = detect_edges(clock)
    clock[clock == 0] = 1
    
    signal = clock
    enc_message[0] = '0' + enc_message[0]
    
    signal[edges[0]:edges[1]] = 0
    for i, byte in enumerate(enc_message):
        for j, bit in enumerate(reversed(byte)):
            signal[edges[10*i+j+1]:edges[10*i+j+2]] = 0 if bit == '0' else 1
##            print(bit)
        if i != num_bytes-1 or i != 0:
            signal[edges[9+i*10]:edges[9+i*10+1]] = 1
            signal[edges[9+i*10+1]:] = 0
        if i == 0 and num_bytes > 1:
            signal[edges[9]:edges[10]] = 1
            signal[edges[10]:] = 0
            
    return clock_time, clock

def detect_baud(time, signal, state_changes, display=False, save=None):
    # the first byte is know to be 'a'
    # so it has 6 state changes including
    # the leading 0 from arduino serial
    
    first_byte_time = time[state_changes[14]:state_changes[-6]+1]
    first_byte_sig = signal[state_changes[14]:state_changes[-6]+1]
    slew = slew_rate(time, state_changes)
    
    first_byte_time = start_at_0(first_byte_time)
    freq = 111*np.pi/first_byte_time[-1]

    delay = 0*slew
    clock_time = np.linspace(0, first_byte_time[-1], 4*int(np.ceil(freq)))
    clock = clock_signal(freq*(clock_time - delay))

    if save is not None:
        display = True

##    im = "72*73*105*120*118*125*116*95*70\n\
##0*114*2*105*62*114*60*117*60\n\
##88*7*29*124*155*144*122*138*60\n\
##94*103*143*164*181*179*148*71*45\n\
##109*159*141*202*256*202*141*159*109\n\
##45*71*148*179*181*164*143*103*94\n\
##60*138*122*144*155*124*29*7*88\n\
##60*117*60*114*62*105*2*114*0\n\
##70*95*116*125*118*120*105*73*72\n"
    
     
    if display:
        fig, axs = plt.subplots(3, 1, sharex=True)
        
        fig.subplots_adjust(hspace=0)
        axs[0].spines['bottom'].set_visible(False)
        axs[1].spines['top'].set_visible(False)
        axs[1].spines['bottom'].set_visible(False)
        axs[2].spines['top'].set_visible(False)
        
        axs[0].set_yticks([0,1])
        axs[0].set_ylim([-.5,1.5])
        axs[1].set_yticks([0,1])
        axs[1].set_ylim([-.5,1.5])
        axs[2].set_yticks([0,1])
        axs[2].set_ylim([-.5,1.5])
        axs[0].set_ylabel('Signal', labelpad=20, rotation=0)    
        axs[1].set_ylabel('CLK', labelpad=20, rotation=0)
        axs[2].set_ylabel('Ref', labelpad=20, rotation=0)

        time_scale = 1e-3
        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/time_scale))
        axs[1].xaxis.set_major_formatter(ticks_x)
        axs[2].set_xlabel(r'Temps $[\mu s]$')

        message = 'Hello world'
        _, _, len_message = encode_message(message)
        
        axs[0].plot(first_byte_time, first_byte_sig, color="black")
        axs[1].plot(clock_time, clock, color="black")
        axs[2].plot(*write_message(message, first_byte_time, freq, delay), color="black")

        for i in range(0, len_message):
            clock_timing = delay + i*np.pi/freq#np.pi/(2*freq) + 
            axs[0].axvline(x=clock_timing,ymin=0,ymax=1, c="black", alpha=0.5, linestyle='--', zorder=0,)# clip_on=False)
            axs[1].axvline(x=clock_timing,ymin=0,ymax=1, c="black", alpha=0.5, linestyle='--', zorder=0,)# clip_on=False)
            axs[2].axvline(x=clock_timing,ymin=0,ymax=1, c="black", alpha=0.5, linestyle='--', zorder=0,)# clip_on=False)

        plt.show()
        if save is not None:
            fig.savefig(f"{save}.svg")
            print(f"Figure saved at '{save}.svg")
            
    return freq

def read_bits(byte):
    pass

if __name__ == '__main__':
    data_dir = 'preprocessed_data'

    # experience type
    speed_test = 'speed_test/python_script'
    im_send = 'information_transmission'
    experience_type = speed_test

    experience = 'baud_test_600'

    temps = np.load(f'{data_dir}/{experience_type}/temps_{experience}.npy').T[0]
    tension = np.load(f'{data_dir}/{experience_type}/tension_{experience}.npy').T[0]

    temps = start_at_0(temps)

    signal_digital, changements_etat = detect_state_change(temps, tension, threshold=None, display=False)
    detect_baud(temps, signal_digital, changements_etat, display=True,)# save='figures/speed_test/baud_300_star_digital')
