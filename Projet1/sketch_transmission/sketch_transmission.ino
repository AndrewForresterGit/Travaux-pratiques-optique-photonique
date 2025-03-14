const int ledPin = 9;  // Pin de la LED
const int receive_pin = 54; // Pin 54 -> A0

const int frequency = 500; // Frequency in Hertz
const int sample_freq = 100*frequency;
const int period = 1000 / frequency; // period in ms
int sample_per = 1000 / sample_freq; // period in ms

const float seuil_low = 3.5; // Seuil du 5V en dessous duquel on considère le niveau logique bas
const float seuil_3V = 3.3/5.0 * 256; // Seuil analogique (pour le analogue read 3.3V avec un ADC 8 bit)

const byte syncSignal = 0b10101010;  // Signal de synchronisation en binaire
const byte endSignal = 0b11011011; // Signal de fin du packet (not used rn)
const int max_len_per_pac = 64; // Longueur de message maximale par packets
bool message_sent = false;
int packet_count, last_packet_size;

const int repeatCount = 1;  // Nombre de fois que le message sera envoyé
int mode = 1; // 1: text, 2: image

const String message = "hello world";
const byte image[] = { 0x89, 0x50, 0x4e, 0x47};
byte data_type, data_len,  packet_number,  total_number_of_packets;

void setup() {
  Serial.begin(115200);
  analogReadResolution(8);
  pinMode(ledPin, OUTPUT);
}

// Fonction pour envoyer un bit (allumer/éteindre la LED)
void sendBit(int bitValue) {
  digitalWrite(ledPin, bitValue ? HIGH : LOW);
  delay(period);
}

// Fonction pour envoyer un caractère en binaire
void sendCharacter(byte character) {
  for (int bit = 7; bit >= 0; bit--) {
    sendBit((character >> bit) & 1);
  }
}

// Fonction pour envoyer le signal de synchronisation
void sendSyncSignal() {
  sendCharacter(syncSignal);  // Envoi du byte de synchronisation en binaire
}

// Fonction pour envoyer l'entête
void sendHeader(byte data_type, byte data_len, byte packet_number, byte total_number_of_packets) {
  sendCharacter(data_type);
  sendCharacter(data_len);
  sendCharacter(packet_number);
  sendCharacter(total_number_of_packets);
}

// Fonction pour calculer le checksum (somme modulo 256)
byte calculateChecksum(String message) {
  byte checksum = 0;
  for (int i = 0; i < message.length(); i++) {
    checksum += message[i];  // Addition des valeurs ASCII
  }
  return checksum;
}

// Fonction pour envoyer un message sous forme d'un paquet binaire
void sendPacket(String message, byte data_type, byte data_len, byte packet_number, byte total_number_of_packets) {

  sendSyncSignal();  // Envoi du signal de synchronisation

  sendHeader(data_type, data_len, packet_number, total_number_of_packets); // envoit le header

  // Envoi du message
  for (int i = 0; i < message.length(); i++) {
    sendCharacter(message[i]);
  }

  // Calcul et envoi du checksum
  byte checksum = calculateChecksum(message);
  sendCharacter(checksum);

  Serial.print("\nChecksum: ");
  Serial.println(checksum, HEX);
}
void sendImage() {
  // Ici faudrait faire que ça envoie juste plusieurs paquets. faut que ça 
  // commence par envoyer un paquet qui dit que c'est une image, qui dit le nombre de paquet de l'image
  // faut que ça divise en paquet, que ça appel la fonction send paquet à chaque fois genre
  // pour l'instant ça raw dawg le truc au complet cuz why not

  sendSyncSignal();  // Envoi du signal de synchronisation
  
  // Envoi de l'image en hex
  for (int i = 0; i < sizeof(image); i++) {
    sendCharacter(image[i]);
  }

  // Calcul et envoi du checksum de l'image
  byte checksum = 0;
  for (int i = 0; i < sizeof(image); i++) {
    checksum += image[i];  // Addition des valeurs hexadécimales de l'image
  }
  sendCharacter(checksum);

  Serial.print("\nImage checksum: ");
  Serial.println(checksum, HEX);
}

void loop() {
  if (!message_sent) {

      if (mode == 1){   // mode de tranmission de texte

      String message = "hello penar, j'ai envie d'aller manger du dulce de leche";
      // On trouve le nombre de paquet et le restant.
        packet_count = message.length() / max_len_per_pac;
        last_packet_size = message.length() % max_len_per_pac;
      // Ajouter un paquet si il y a un restant
        if (last_packet_size > 0){
          packet_count++;
        }
      // On envoie chaque paquet en scindant le message
        for (int i = 0; i < packet_count-1; i++){
          String packet_message = message.substring(i*max_len_per_pac, (i+1)*max_len_per_pac);
          sendPacket(packet_message, 0b1, (byte)packet_message.length(), (byte)i, (byte)packet_count);
        }
        //JOUE

      //delay(1000);  // Pause avant le prochain envoi
      } else if (mode == 2) {
        // Si mode = 1, envoyer une image
        sendImage();
        delay(1000);  // Pause avant la prochaine boucle
      }
    message_sent = true;
  }

  // Maintenant, il vérifie si il a reçu dequoi
  while (!read_bool){
    delay(sample_per);
  }
  // Synchroniser les fréquences
  sync(sample_per); // Fonction qui modifie le sample time en détectant le sync, calculant la valeur de durrée moyenne d'un bit, et qui ajuste la fréquence de sampla
  // Par contre là, après on peut soit juste sample à la fréquence qu'on a identifié, ou on sample à un multiple de cette fréquence, puis on fait ce que ludo m'a montré
  // Aka de expect genre 10 +/- 1 bit pour chaque, de compter le nombre avant changement, et de déduire si c'est 1 ou + de bit. idk tho wtv.
  
  interp_header(data_type, data_len,  packet_number,  total_number_of_packets);
  // Blablabla continuer à capter le

}

  bool read_bool(){
    int raw_sig = analogRead(receive_pin); 
    bool logic_state = (raw_sig >= seuil_3V) ? HIGH : LOW;
    return logic_state;
  }

  void sync(int &sample_per){
    // Fait la synchronisation en adaptant la fréquence (la période enft) de réception.
    // On regarde combien de temps ça prend pour pour recevoir tout le sync, puis on modifie pour sample à la même fréquence que la réception
    bool prev_state = 1;
    int counter = 1;
    for (uint8_t  i=1; i<8; i++){
      while (prev_state == read_bool()){
        counter++;
        delay(sample_per);
      }
    }
    // On divise par 7 même si le sync est 8 de long parce qu'on ne vérifie pas la longueur du dernier 0 (parce que si c'est un 0 dans le header on vas l'inclure, ce qu'on veut pas)
    sample_per = sample_per * counter / 7;
    // On fait un délais pour que le dernier 0 du sync passe, puis on fait 0.5 sample_per plus loin pour être au centre des bits
    delay(sample_per*1.5);
  }

void interp_header(byte &data_type, byte &data_len, byte &packet_number, byte &total_number_of_packets){
  data_type = get_byte();
  data_len = get_byte();
  packet_number = get_byte();
  total_number_of_packets = get_byte();

}

uint8_t  get_byte(){
    uint8_t valeur;
    for (uint8_t i = 0; i < 8; i++){
    valeur = (valeur << 1) | read_bool();
    }
  return valeur;
}
