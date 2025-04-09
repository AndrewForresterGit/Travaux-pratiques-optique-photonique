% Load recording
load('mozzart_2.mat'); 
t = moku.data(:,1);
v = moku.data(:, 2);
% Load noise
load('noise_20s_real.mat');
t_dark = moku.data(:,1);
v_dark = moku.data(:, 2);

% Sampling freq
fs = 1 / (t(2) - t(1)); 
N = length(v); 


% FFT of signals
FFT_signal = fft(v);
FFT_dark   = fft(v_dark);

FFT_net = FFT_signal - 1.1*FFT_dark;
v_cleaned = real(ifft(FFT_net));

%% Conception d'un filtre passe-bande Butterworth
low_cutoff  = 400;    % par exemple, 20 Hz
high_cutoff = 4000; % par exemple, 20 kHz (vérifiez que cela correspond à votre système)

% Ordre du filtre
order = 4; 
% Conception du filtre
[b, a] = butter(order, [low_cutoff, high_cutoff] / (fs/2), 'bandpass');

%% Application du filtre

v_filtered = filtfilt(b, a, v_cleaned);

%% Affichage des résultats
figure;
subplot(3,1,1)
plot(t, v);
title('Signal mesuré (avec bruit)');
xlabel('Temps (s)');
ylabel('Tension (V)');
grid on;

subplot(3,1,2)
plot(t, v_dark);
title('Signal Dark (bruit)');
xlabel('Temps (s)');
ylabel('Tension (V)');
grid on;

subplot(3,1,3)
plot(t, v_filtered);
title('Signal nettoyé (après soustraction en fréquence)');
xlabel('Temps (s)');
ylabel('Tension (V)');
grid on;

%% (Optionnel) Affichage des spectres
f = (0:N-1)*(fs/N); % Vecteur de fréquences
figure;
subplot(3,1,1)
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

subplot(3,1,3)
plot(f, abs(FFT_net));
title('Spectre du signal nettoyé');
xlabel('Fréquence (Hz)');
ylabel('Amplitude');
grid on;
%audiowrite("mozzzzz6_filt.wav", v_filtered, round(fs));
