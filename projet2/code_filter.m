load('dat_440hz.mat'); 
t = moku.data(:,1);
v = moku.data(:, 2);

%% Paramètres d'échantillonnage
% Calcul de la fréquence d'échantillonnage
fs = 1 / (t(2) - t(1)); 
fprintf('Fréquence d''échantillonnage: %.2f Hz\n', fs);

%% Conception d'un filtre passe-bande Butterworth
low_cutoff  = 100;    % par exemple, 20 Hz
high_cutoff = 3000; % par exemple, 20 kHz (vérifiez que cela correspond à votre système)

% Ordre du filtre
order = 4; 

% Conception du filtre
[b, a] = butter(order, [low_cutoff, high_cutoff] / (fs/2), 'bandpass');

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

subplot(4,1,2)
plot(f, abs(FFT_signal));
title('Spectre du signal mesuré');
xlabel('Fréquence (Hz)');
ylabel('Amplitude');
grid on;

subplot(3,1,2)
plot(f, abs(FFT_dark));
title('Spectre du signal dark');
xlabel('Fréquence (Hz)');
ylabel('Amplitude');
grid on;

audiowrite("test_440.wav", v, round(fs));
