##from math import floor, ceil
import numpy as np
from scipy.signal import square
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def start_at_0(time, norm=False):
    new_time = time-time[0]
    if norm:
        new_time /= new_time[-1]
    return new_time

def clock_signal(time):
    return np.where(square(time)<0, 0, 1)

def detect_edges(signal):
    return np.where(signal[:-1] != signal[1:])[0]+1

def slew_rate(time, stage_changes):
    slew_rate = (time[stage_changes[0]+1] - time[stage_changes[0]])/2
    return slew_rate

def chop_into_messages(time, signal, wait_time, buffer=0, threshold=None, display=False, analog=False):
    sig, state_changes = detect_state_change(time, signal, threshold=threshold, display=display)

    if analog:
        sig = signal
    
    messages = []
    times = []
    current_message = np.array([])
    current_time = np.array([])
    
    for i in range(len(state_changes)-1):
        time_delta = time[state_changes[i+1]] - time[state_changes[i]]
        if time_delta < wait_time:
            if not len(current_message):
                current_message = np.concatenate((current_message, sig[state_changes[i]-buffer:state_changes[i+1]]))
                current_time = np.concatenate((current_time, time[state_changes[i]-buffer:state_changes[i+1]]))
            else:
                current_message = np.concatenate((current_message, sig[state_changes[i]:state_changes[i+1]]))
                current_time = np.concatenate((current_time, time[state_changes[i]:state_changes[i+1]]))
        elif time_delta > wait_time:
            current_message = np.concatenate((current_message, sig[state_changes[i]:state_changes[i]+buffer]))
            current_time = np.concatenate((current_time, time[state_changes[i]:state_changes[i]+buffer]))
            messages.append(current_message)
            times.append(current_time)
            current_message = np.array([])
            current_time = np.array([])
            
    messages.append(current_message)
    times.append(current_time)

    return times, messages

def decode_signal(time, signal, num_bits, display=False):
    message = ''
    time = start_at_0(time)
    bit_time = time[-1]/num_bits
    print(bit_time)
    
    digital_sig, state_changes = detect_state_change(time, signal)
    for i in range(len(state_changes)+1):
        plt.plot(time, digital_sig)
        if i == 0:
            time_0 = time[state_changes[0]]
            sig_0 = set(digital_sig[:state_changes[0]])
            plt.plot(time[:state_changes[0]],digital_sig[:state_changes[0]])
        elif i == len(state_changes):
            time_0 = time[-1] - time[state_changes[-1]]
            sig_0 = set(digital_sig[state_changes[-1]:])
            plt.plot(time[state_changes[-1]:],digital_sig[state_changes[-1]:])
        else:
            time_0 = time[state_changes[i]] - time[state_changes[i-1]]
            sig_0 = set(digital_sig[state_changes[i-1]:state_changes[i]])
            plt.plot(time[state_changes[i-1]:state_changes[i]],digital_sig[state_changes[i-1]:state_changes[i]])
        if display:
            plt.show()

        bits = int(np.round(time_0/bit_time))
        a = bits*str(sig_0.pop())
        message += a
    print(message)

    

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

        ax_analog.scatter(time, signal, s=2)
        ax_analog.axhline(y=threshold, color='r', linestyle='--')
        ax_digital.plot(time, digital_sig)
        ax_digital.set_ylim([-.1,1.1])
        ax_digital.set_yticks([0,1])

##        for change in time[state_change_indices]:
##            ax_analog.axvline(x=change, color='g', alpha=0.5, linestyle='--')

        plt.show()
        if save is not None:
            fig.savefig(f"{save}.svg", bbox_inches='tight')
            print(f"Figure saved at '{save}.svg")

    return digital_sig, state_change_indices

def encode_message(message):
    enc_message = [i for i in map(bin, message.encode('utf-8'))]
##    print('0')
    for i, byte in enumerate(enc_message):
        enc_message[i] = byte.replace('b', '').zfill(8)
##        print(enc_message[i][::-1])
##        print('10')

    num_bytes = len(enc_message)
    if num_bytes == 1:
        len_message = 10
    else:
        len_message = num_bytes*10+1

    return enc_message, num_bytes, len_message

def write_message(message, time, freq, delay):
    enc_message, num_bytes, len_message = encode_message(message)

    clock_time = np.arange(0, len_message*np.pi/freq, 1/(4*freq))
    clock = clock_signal(freq*(clock_time - delay))
    edges = detect_edges(clock)
    clock[clock == 0] = 1

    signal = clock

    signal[edges[0]:edges[1]] = 0
    for i, byte in enumerate(enc_message):
        for j, bit in enumerate(reversed(byte)):
            signal[edges[10*i+j+1]:edges[10*i+j+2]] = 0 if bit == '0' else 1
        if i != num_bytes-1 or i != 0:
            signal[edges[9+i*10]:edges[9+i*10+1]] = 1
            signal[edges[9+i*10+1]:] = 0
        if i == 0 and num_bytes > 1:
            signal[edges[9]:edges[10]] = 1
            signal[edges[10]:edges[11]] = 0
##        elif i == 0 and num_bytes == 1:
##            signal[edges[9]:] = 1

    return clock_time, clock

def graph_sig(time, signal, state_changes, num_bits, ref=None, display=False, save=None):
    slew = slew_rate(time, state_changes)

    time = start_at_0(time)
    freq = num_bits*np.pi/time[-1]

    delay = 1*slew
    clock_time = np.arange(0, time[-1], 1/(4*freq))
    clock = clock_signal(freq*(clock_time - delay))

    if save is not None:
        display = True

    num_axs = 2
    if ref is not None:
        num_axs = 3

    if display:
        fig, axs = plt.subplots(num_axs, 1, sharex=True)

        fig.subplots_adjust(hspace=0)
        axs[0].spines['bottom'].set_visible(False)
        axs[1].spines['top'].set_visible(False)
        axs[1].spines['bottom'].set_visible(False)

        axs[0].set_yticks([0,1])
        axs[0].set_ylim([-.5,1.5])
        axs[1].set_yticks([0,1])
        axs[1].set_ylim([-.5,1.5])

        axs[0].set_ylabel('Signal', labelpad=20, rotation=0)
        axs[1].set_ylabel('CLK', labelpad=20, rotation=0)

        time_scale = 1e-3
        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/time_scale))
        axs[num_axs-1].xaxis.set_major_formatter(ticks_x)

        axs[0].plot(time, signal, color="black")
        axs[1].plot(clock_time, clock, color="black")

        if ref is not None:
            message = write_message(ref, time, freq, delay)
            _, _, num_bits = encode_message(ref)
            
            axs[2].set_yticks([0,1])
            axs[2].set_ylim([-.5,1.5])
            axs[2].set_ylabel('Ref', labelpad=20, rotation=0)
            axs[2].set_xlabel(r'Temps $[\mu s]$')
            axs[2].spines['top'].set_visible(False)
            axs[2].plot(*message, color="black")

##        for i in range(0, num_bits):
##            clock_timing = delay + i*np.pi/freq#np.pi/(2*freq) +
##            axs[0].axvline(x=clock_timing,ymin=0,ymax=1, c="black", alpha=0.5, linestyle='--', zorder=0,)# clip_on=False)
##            axs[1].axvline(x=clock_timing,ymin=0,ymax=1, c="black", alpha=0.5, linestyle='--', zorder=0,)# clip_on=False)
##            if ref is not None:
##                axs[2].axvline(x=clock_timing,ymin=0,ymax=1, c="black", alpha=0.5, linestyle='--', zorder=0,)# clip_on=False)

        plt.show()
        if save is not None:
            fig.savefig(f"{save}.svg", bbox_inches='tight')
            print(f"Figure saved at '{save}.svg")

if __name__ == '__main__':
    data_dir = 'preprocessed_data'
    save_dir = 'figures/speed_test'

    # experience type
    speed_test = 'speed_test/python_script'
    im_send = 'information_transmission'
    experience_type = im_send
    experience = 'image'

    temps = start_at_0(np.load(f'{data_dir}/{experience_type}/temps_{experience}.npy').T[0])
    tension = np.load(f'{data_dir}/{experience_type}/tension_{experience}.npy').T[0]
    signal_digital, changements_etat = detect_state_change(start_at_0(temps), tension,
                                                           threshold=None, display=False)#, save='figures/speed_test/digital_300')
    graph_sig(temps, signal_digital, changements_etat, num_bits=2591, ref=None, display=True,)# save='baud_300_star_digital')

##    experiences = ['baud_test_300', 'baud_test_600', 'baud_test_1200',
##                   'baud_test_2400', 'baud_test_4800', 'baud_test_9600',]
##                   'baud_test_19200', 'baud_test_38400']
##    experiences = ['baud_test_300', 'baud_test_600', 'baud_test_2400', 'baud_test_9600',]

##    fig1, axs1 = plt.subplots(len(experiences), 1, figsize=(7, 8))
##
##    for i in range(axs1.shape[0]):
####        for j in range(axs1.shape[1]):
##        axs1[i].set_yticks([0,1])
##        axs1[i].set_xticks([])
##        axs1[i].set_ylim([-.5,1.5])
##        axs1[i].tick_params(labelsize=10)
####        
####        time_scale = 1e-3
##        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/time_scale))
##        axs1[i].xaxis.set_major_formatter(ticks_x)
            
##
##    temps = []
##    tensions = []
##    wait_times = [.1, .1, .05, .01, .005, .004, .005, 0.01]
##    mes = ['a', '*', 'Hello world!']
##    bits = [9, 9, 112]
##    for i, experience in enumerate(experiences):
##        baud = int(experience.split('_')[-1])
##        print(baud)
##        temps.append(start_at_0(np.load(f'{data_dir}/{experience_type}/temps_{experience}.npy').T[0]))
##        tensions.append(np.load(f'{data_dir}/{experience_type}/tension_{experience}.npy').T[0])
##        print((temps[i][-1] - temps[i][0])/len(temps))
####        plt.plot(temps[i], tensions[i]*5/1024)
####        plt.show()
##        if wait_times == 0.:
##            wait_times[i] = float(input('Wait time :'))
##        
##        times, messages = chop_into_messages(temps[i], tensions[i], wait_time=wait_times[i], buffer=0, analog=False, display=False)
##
##        if len(messages) == 0:
##            continue
##        fig, axs = plt.subplots(len(messages), 1)
##        for j, message in enumerate(messages):
##            decode_signal(times[j], messages[j], bits[j], display=False)
####            if j == 0:
####                continue
##            if type(axs) is not np.ndarray:
##                axs.plot(start_at_0(times[j]), messages[j], color="black")
##                axs.plot(start_at_0(times[j]), messages[j], color="black")
##                axs.set_yticks([0,1])
##                axs.set_ylim([-.5,1.5])
##                
##                time_scale = 1e-3
##                ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/time_scale))
##                axs.xaxis.set_major_formatter(ticks_x)
##                axs.set_xlabel(r'Temps [ms]', labelsize=50)
##                break
####            if len(message) == 1:
####                fig1.delaxes(axs1[i, j-1])                
####            else:
####                axs1[i, j-1].plot(start_at_0(times[j]), messages[j], color="black")
####            axs[j].plot(start_at_0(times[j]), messages[j], color="black")
##            axs[j].set_yticks([0,1])
##            axs[j].set_ylim([-.2,1.2])
##            
##            time_scale = 1e-3
##            ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/time_scale))
##            axs[j].xaxis.set_major_formatter(ticks_x)
##            if j ==2:
##                axs1[i].plot(start_at_0(times[j], norm=True), messages[j], color="black")
##                axs1[i].text(1, -.5 + 0.1, f'{baud} baud', fontsize=10, ha='right', va='bottom', color='black')
##
##                
##            
####        if type(axs) is np.ndarray:    
####            axs[-1].set_xlabel(r'Temps [ms]')
####    axs1[-1, 0].set_xlabel(r'Temps [ms]')
##    axs1[-1].set_xlabel(r'Temps normalisé [-]')
####    fig1.savefig(f"{save_dir}/comparaison_hello_world.svg", bbox_inches='tight')
####    fig1.savefig(f"{save_dir}/comparaison_hello_world.png", bbox_inches='tight', dpi=600)
##    plt.show()

##        fig.savefig(f"{save_dir}/{experience}.svg", bbox_inches='tight')
##        print(f"Figure saved at '{save_dir}/{experience}.svg'")

##    print(wait_times)
            

    # processe the image reference message
##    im = "72*73*105*120*118*125*116*95*70\\n0*114*2*105*62*114*60*117*60\\n88*7*29*124*155*144*122*138*60\\n94*103*143*164*181*179*148*71*45\\n109*159*141*202*256*202*141*159*109\\n45*71*148*179*181*164*143*103*94\\n60*138*122*144*155*124*29*7*88\\n60*117*60*114*62*105*2*114*0\\n70*95*116*125*118*120*105*73*72\\n"
##    im_mes, num_bytes_im, num_bits_im = encode_message(im)

##    times, messages = chop_into_messages(temps, tension, wait_time=wait_time, threshold=500, analog=False, display=False)
    
##    decode_signal(times[0], messages[0], num_bits_im, display=False)
##    decode_signal(times[1], messages[1], 9, display=True)
##
##    signal_digital, changements_etat = detect_state_change(start_at_0(times[0]), messages[0], threshold=None, display=True, save='figures/speed_test/digital_300')
##    graph_sig(times[1], messages[1], changements_etat, num_bits=9, ref='*', display=True,)# save='baud_300_star_digital')
