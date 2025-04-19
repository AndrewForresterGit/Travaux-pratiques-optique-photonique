% Ne marche pas très bien
% Code qui filtre les audio; méthode filtre de Wienner
load('vitre_steph_phone.mat');
t = moku.data(:,1);
x = moku.data(:,2);

data = x - mean(x);

% 2) filtre passe-haut 8e ordre, coupure 20 Hz
hpFilt = designfilt('bandpassiir', ...
    'FilterOrder',6, ...
    'HalfPowerFrequency1',100, ...
    'HalfPowerFrequency2',8000, ...
    'SampleRate',Fs);
x = filtfilt(hpFilt, x);


% Récupère les données de l'audio
%[x, Fs] = audioread('copy_phone_stephanie.wav');
Fs = 1 / (t(2) - t(1));
% On prende la permière seconde, qui est supposé être du bruit.
noise_seg = x(1:round(0.9*Fs));

N = length(noise_seg);

% On définit une fenêtre de hamming pour mieux gérer les bords qu'une
% fenêtre carré
window = hamming(N);

% spectre du bruit
noise_specter = fft(noise_seg .* window);
% Densité de puissance normalisé du bruit
Pn = abs(noise_specter).^2 / N;

% paramètres
frameLen = 1024;
hop = frameLen/2;
w = hamming(frameLen);

% trames et reconstruction
[x_frames, ~] = buffer(x, frameLen, frameLen-hop, 'nodelay');
numFrames = size(x_frames,2);
y = zeros(size(x));
filter_1 = true;
wienner = true;

if filter_1
for k = 1:numFrames
    frame = x_frames(:,k) .* w;
    Xf = fft(frame);
    % puissance et modulo
    P_frame = abs(Xf).^2;
    % soustraction
    P_clean = max(P_frame - Pn(1:frameLen), eps);
    % conservation de la phase
    Yf = sqrt(P_clean) .* exp(1i*angle(Xf));
    % trame nettoyée
    frame_clean = real(ifft(Yf));
    % remise dans y (Overlap-Add)
    idx = (k-1)*hop + (1:frameLen);
    y(idx) = y(idx) + frame_clean .* w;
end

audiowrite('nettoye_soustraction.wav', y, Fs);
end

if wienner
    for k = 1:numFrames
        frame = x_frames(:,k) .* w;
        Xf = fft(frame);
        P_x = abs(Xf).^2;
        % Estimation de SNR spectral
        H = max((P_x - Pn(1:frameLen)) ./ (P_x), 0);
        Yf = H .* Xf;
        frame_clean = real(ifft(Yf));
        idx = (k-1)*hop + (1:frameLen);
        y(idx) = y(idx) + frame_clean .* w;
    end
    audiowrite('nettoye_wiener.wav', y, Fs);
end