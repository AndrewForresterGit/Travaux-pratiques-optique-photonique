t = moku.data(:,1);
v = moku.data(:, 2);

plot(t, v);
Fs = 40000; % Fréquence d'échantillonnage
audiowrite("sweep.wav", v, Fs);