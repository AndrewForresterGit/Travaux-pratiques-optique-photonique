load('phone_sur_table.mat');
t = moku.data(:,1);
v = moku.data(:,2);

% 1) Paramètres d'échantillonnage
fs = 1 / (t(2) - t(1));
fprintf('Fréquence d''échantillonnage: %.2f Hz\n', fs);
N  = length(v);

% 2) Suppression du DC / detrend
v = v - mean(v);
% v = detrend(v);

% 3) Conception du filtre passe-bande
low_cutoff  = 100;
high_cutoff = 4000;
order       = 4;
[b, a]      = butter(order, [low_cutoff, high_cutoff]/(fs/2), 'bandpass');

% 4) Application du filtre
voltage_filtered = filtfilt(b, a, v);

% 5) FFT et normalisation
FFT_signal          = fft(v)/N;
FFT_signal_filtered = fft(voltage_filtered)/N;

% Axe fréquentiel complet
f = (0:N-1)*(fs/N);

% 6) Affichage
figure;

subplot(2,2,1)
plot(t, v);
title('Signal brut (DC enlevé)');
xlabel('Temps (s)');
ylabel('Tension (V)');
grid on;

subplot(2,2,2)
plot(t, voltage_filtered);
title('Signal filtré 200–300 Hz');
xlabel('Temps (s)');
ylabel('Tension (V)');
grid on;

half = floor(N/2);
subplot(2,2,3)
plot(f(1:half), abs(FFT_signal(1:half)));
title('Spectre du signal mesuré');
xlabel('Fréquence (Hz)');
ylabel('Amplitude (V)');
grid on;
xlim([0 20000]); 
set(gca, 'XScale', 'log');  
set(gca, 'YScale', 'log');


subplot(2,2,4)
set(gca, 'XScale', 'log'); 
set(gca, 'YScale', 'log');
plot(f(1:half), abs(FFT_signal_filtered(1:half)));
title('Spectre du signal filtré');
xlabel('Fréquence (Hz)');
ylabel('Amplitude (V)');
xlim([low_cutoff high_cutoff]);  
grid on;
set(gca, 'XScale', 'log');  
set(gca, 'YScale', 'log');

% 7) Sauvegarde audio (normalisation si besoin)
v_norm = v / max(abs(v));
v_filt = voltage_filtered / max(abs(voltage_filtered));
audiowrite("phone_sur_table.wav", v_norm, round(fs));
audiowrite("phone_sur_table_filt.wav", v_filt, round(fs));
