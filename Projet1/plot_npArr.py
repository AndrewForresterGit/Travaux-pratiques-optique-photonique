import numpy as np
import matplotlib.pyplot as plt

def crop_x(x, y):
    user_done = False
    
    while not user_done:
        plt.plot(x, y)
        plt.show()
        new_domain = input('nouveau domaine [a, b]: ')
        a, b = map(float, new_domain.split(' '))
        print(a, b)
        indexes = np.argwhere((x>a) & (x<b))
        
        new_x = x[indexes]
        new_y = y[indexes]
        plt.plot(new_x, new_y)
        plt.show()
        
        user_input = ''
        while user_input != 'y' and user_input != 'n':
            user_input = input('ok (y/n): ')
            if user_input == 'y':
                user_done = True
            elif user_input == 'n':
                user_done = False
            else:
                print("Answer must be 'y' or 'n'")
 
    return new_x, new_y

if __name__ == '__main__':
    data_dir = 'raw_data'
    save_data_dir = 'preprocessed_data'

    # experience type
    speed_test = 'speed_test/python_script'
    im_send = 'information_transmission'
    experience_type = speed_test

    experience = 'baud_test_38400'
    
    temps = np.load(f'{data_dir}/{experience_type}/temps_{experience}.npy')
    tension = np.load(f'{data_dir}/{experience_type}/tension_{experience}.npy')
    
    new_temps, new_tension = crop_x(temps, tension)

    np.save(f'{save_data_dir}/{experience_type}/temps_{experience}.npy', new_temps)
    np.save(f'{save_data_dir}/{experience_type}/tension_{experience}.npy', new_tension)
    
