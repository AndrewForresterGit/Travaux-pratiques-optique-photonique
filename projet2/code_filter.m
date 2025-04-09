load('dat_440hz.mat'); 
t = moku.data(:,1);
v = moku.data(:, 2);

%% Paramètres d'échantillonnage
% Calcul de la fréquence d'échantillonnage
f = 1 / (t(2) - t(1)); 
fprintf('Fréquence d''échantillonnage: %.2f Hz\n', f);

%% Conception d'un filtre passe-bande Butterworth
low_cutoff  = 100;    % par exemple, 20 Hz
high_cutoff = 3000; % par exemple, 20 kHz (vérifiez que cela correspond à votre système)

% Ordre du filtre
order = 4; 

% Conception du filtre
[b, a] = butter(order, [low_cutoff, high_cutoff] / (f/2), 'bandpass');

%% Application du filtre

voltage_filtered = filtfilt(b, a, v);
%voltage_filtered = v;

FFT_signal = fft(v);

FFT_signal_filtered = fft(voltage_filtered);

%% Affichage des résultats
figure;
subplot(4,1,1)
plot(t, v, 'b');
title('Signal brut');
xlabel('Temps (s)');
ylabel('Tension (V)');
grid on;

subplot(4,1,2)
plot(t, voltage_filtered, 'r');
title('Signal filtré');
xlabel('Temps (s)');
ylabel('Tension (V)');
grid on;

subplot(4,1,3)
plot(f, abs(FFT_signal));
title('Spectre du signal mesuré');
xlabel('Fréquence (Hz)');
ylabel('Amplitude');
grid on;

subplot(4,1,4)
plot(f, abs(FFT_signal_filtered));
title('Spectre du signal filtré');
xlabel('Fréquence (Hz)');
ylabel('Amplitude');
grid on;

audiowrite("test_440.wav", v, round(f));
