// Paramètres de timing et broches
const unsigned long BIT_DURATION = 20; // en microsecondes (50 kHz), modifiable
const int LED_TX_PIN = 9;     // Broche de sortie pour la LED
const int RX_PIN = 8;         // Broche de réception (pour le signal digital, soit via comparateur ou filtré)

// Constantes du protocole
const byte PREAMBULE = 0x55;  // Valeur à envoyer pour le préambule
const int NB_PREAMBULE = 4;   // Nombre d'octets de préambule
const byte START_MARKER = 0x7E; // Marqueur de début de paquet

// Fonctions de base pour la transmission

// Envoi d'un bit (1 ou 0)
void sendBit(bool bitVal) {
  digitalWrite(LED_TX_PIN, bitVal ? HIGH : LOW);
  delayMicroseconds(BIT_DURATION);
}

// Envoi d'un octet, MSB en premier
void sendByte(byte data) {
  for (int i = 7; i >= 0; i--) {
    bool bitVal = (data >> i) & 0x01;
    sendBit(bitVal);
  }
}

// Calcul du checksum : somme modulo 256 sur le type, la longueur et les données
byte calcChecksum(byte type, byte length, const byte* data) {
  unsigned int sum = type + length;
  for (int i = 0; i < length; i++) {
    sum += data[i];
  }
  return sum & 0xFF;
}

// Envoi d'un paquet complet
void sendPacket(byte packetType, const byte* payload, byte payloadLength) {
  // 1. Envoi du préambule
  for (int i = 0; i < NB_PREAMBULE; i++) {
    sendByte(PREAMBULE);
  }
  
  // 2. Envoi du start marker
  sendByte(START_MARKER);
  
  // 3. Envoi du type de paquet et de la longueur
  sendByte(packetType);
  sendByte(payloadLength);
  
  // 4. Envoi de la charge utile
  for (int i = 0; i < payloadLength; i++) {
    sendByte(payload[i]);
  }
  
  // 5. Calcul et envoi du checksum
  byte checksum = calcChecksum(packetType, payloadLength, payload);
  sendByte(checksum);
}

// Exemple d'une fonction de réception (squelette)
// Remarque : Une implémentation robuste nécessiterait une machine à états pour détecter le préambule,
// le start marker, puis échantilloner précisément chaque bit.
// Ici, on propose un cadre simplifié.
bool receivePacket(byte &packetType, byte* payload, byte &payloadLength) {
  // Pour une implémentation simple :
  // - Attendre et détecter NB_PREAMBULE octets de 0x55 consécutifs
  // - Puis détecter le start marker (0x7E)
  // - Lire le packetType et la longueur
  // - Lire le payload et enfin le checksum
  // - Vérifier le checksum et retourner true si le paquet est valide, false sinon.
  
  // [CODE DE SYNCHRONISATION & LECTURE DES BITS À ÉCHANTILLONNER PRÉCISÉMENT À COMPLETER]
  
  // Cette partie peut être réalisée en utilisant un timer ou des interruptions sur la broche RX.
  return false; // Indiquer que rien n'a encore été reçu
}

void setup() {
  pinMode(LED_TX_PIN, OUTPUT);
  pinMode(RX_PIN, INPUT);
  Serial.begin(115200);
  // Pour debug : indication de démarrage
  Serial.println("Initialisation du protocole LED...");
}

void loop() {
  // Exemple d'envoi périodique d'un paquet de données (bidirectionnel)
  byte dataToSend[3] = {0x12, 0x34, 0x56};  // Charge utile exemple
  byte packetType = 0x01; // Type "donnée"
  sendPacket(packetType, dataToSend, 3);
  
  Serial.println("Paquet envoyé !");
  
  // Attendre un certain temps avant d'envoyer un nouveau paquet (exemple)
  delay(1000);
  
  // Ici, vous ajouterez la gestion de la réception
  // if(receivePacket(...)) { ... }
}

