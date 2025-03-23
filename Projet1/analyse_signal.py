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

def detect_state_change(time, signal, threshold=None, display=False):
    if threshold is None:
        threshold = (np.max(signal) - np.min(signal))/2

    digital_sig = np.where(signal > threshold, 1, 0)
    state_change_indices = detect_edges(digital_sig)

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

def write_message(message, time, freq, delay):
    enc_message = [i for i in map(bin, message.encode('ascii'))]
    for i, byte in enumerate(enc_message):
        enc_message[i] = byte.replace('b', '')
    num_bytes = len(enc_message)
    len_message = num_bytes*10+1

    clock_time = np.linspace(0, len_message*np.pi/freq, 4*int(np.ceil(freq)))
    clock = clock_signal(freq*(clock_time - delay))
    edges = detect_edges(clock)
    
    signal = clock
    
    signal[edges[0]:edges[1]] = 0
    for i, byte in enumerate(enc_message):
        for j, bit in enumerate(reversed(byte)):
            if bit == 'b':
                continue
##            print(10*i+j+1, i, j, bit) 
            signal[edges[10*i+j+1]:edges[10*i+j+2]] = 0 if bit == '0' else 1
        if i != num_bytes-1 or i != 0:
            print(i)
            signal[edges[9+i*10]:edges[9+i*10+1]] = 0
            signal[edges[9+i*10+1]:edges[9+i*10+2]] = 0
        if i == 0:
            signal[edges[9]:edges[10]] = 1
            signal[edges[10]:edges[11]] = 0
    return clock_time, clock

def detect_baud(time, signal, state_changes, display=False, save=None):
    # the first byte is know to be 'a'
    # so it has 6 state changes including
    # the leading 0 from arduino serial
    
    first_byte_time = time[state_changes[0]:state_changes[5]+2]
    first_byte_sig = signal[state_changes[0]:state_changes[5]+2]
    slew = slew_rate(time, state_changes)
    
    first_byte_time = start_at_0(first_byte_time)
    freq = 9*np.pi/first_byte_time[-1]

    delay = 2*slew
    clock_time = np.linspace(0, first_byte_time[-1], 4*int(np.ceil(freq)))
    clock = clock_signal(freq*(clock_time - delay))

    if save is not None:
        display = True
        
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
        axs[1].set_xlabel(r'Temps $[\mu s]$')
        
        axs[0].plot(first_byte_time, first_byte_sig, color="black")
        axs[1].plot(clock_time, clock, color="black")
        axs[2].plot(*write_message('aaa', first_byte_time, freq, delay), color="black")

        for i in range(0, 9):
            clock_timing = delay + i*np.pi/freq#np.pi/(2*freq) + 
            axs[0].axvline(x=clock_timing,ymin=0,ymax=1, c="black", alpha=0.5, linestyle='--', zorder=0, clip_on=False)
            axs[1].axvline(x=clock_timing,ymin=0,ymax=1, c="black", alpha=0.5, linestyle='--', zorder=0, clip_on=False)
            axs[2].axvline(x=clock_timing,ymin=0,ymax=1, c="black", alpha=0.5, linestyle='--', zorder=0, clip_on=False)

        plt.show()

    return freq

def read_bits(byte):
    pass

if __name__ == '__main__':
    data_dir = 'preprocessed_data'

    # experience type
    speed_test = 'speed_test/python_script'
    im_send = 'information_transmission'
    experience_type = speed_test

    experience = 'baud_test_300'

    temps = np.load(f'{data_dir}/{experience_type}/temps_{experience}.npy').T[0]
    tension = np.load(f'{data_dir}/{experience_type}/tension_{experience}.npy').T[0]

    temps = start_at_0(temps)

    signal_digital, changements_etat = detect_state_change(temps, tension, threshold=400, display=False)
    detect_baud(temps, signal_digital, changements_etat, display=True)

##    plt.plot(temps, tension)
##    plt.show()
