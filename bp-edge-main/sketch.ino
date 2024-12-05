#include <ESP32Servo.h>
#include <WiFi.h>
#include <PubSubClient.h>

#define DATA_PIN 5   // Pino conectado ao DS do 74HC595
#define LATCH_PIN 22 // Pino conectado ao STCP do 74HC595
#define CLOCK_PIN 23 // Pino conectado ao SHCP do 74HC595
#define EXTRA_PIN 18 // Pino extra para indicar efiencia completa

const int ldr1Pin = 35;  // Pino do LDR 1 no ESP32
const int ldr2Pin = 34;  // Pino do LDR 2 no ESP32
const int servoPin = 13; // Pino do servo no ESP32

const int numLeds = 8; // Número de LEDs no LED bar graph controlado pelo 74HC595

// Criação dos objetos necessários
Servo servoMotor;
WiFiClient espClient;
PubSubClient MQTT(espClient);

int posicaoServo = 90; // Posição inicial do servo (90º)

// Inicializando o valor global de luminosidade
int totalLuminosity = 0;

// Configuração da conexão do ESP32 com Wifi
char *SSID = const_cast<char *>("Wokwi-GUEST");
char *PASSWORD = const_cast<char *>("");
char *BROKER_MQTT = const_cast<char *>("");
int BROKER_PORT = 1883;
char *TOPICO_SUBSCRIBE = const_cast<char *>("/TEF/device001/cmd"); // Tópico de escuta do MQTT
char *TOPICO_PUBLISH_E = const_cast<char *>("/TEF/device001/attrs/ea"); // Checar a coleta no lado leste
char *TOPICO_PUBLISH_W = const_cast<char *>("/TEF/device001/attrs/we"); // Checar a coleta no lado oeste
char *TOPICO_PUBLISH_EFF = const_cast<char *>("/TEF/device001/attrs/eff"); // Checar a eficiencia energética
char *ID_MQTT = const_cast<char *>("fiware_001");
const char *topicPrefix = "device001";


void setup()
{
  initWiFi();
  initMQTT();
  initPin();
  initSerial();
  servoSetup();
}

void loop()
{
  handleSolarLight();
  updateLeds();
  verifyMQTTWifiConnections();
  MQTT.loop();
  delay(2000);
}

void reconectWiFi()
{
  if (WiFi.status() == WL_CONNECTED)
    return;
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(100);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Conectado com sucesso na rede ");
  Serial.print(SSID);
  Serial.println("IP obtido: ");
  Serial.println(WiFi.localIP());
}

void verifyMQTTWifiConnections()
{
  if (!MQTT.connected())
    reconnectMQTT();
  reconectWiFi();
}

void reconnectMQTT()
{
  while (!MQTT.connected())
  {
    Serial.print("【┘】Tentando se conectar ao Broker MQTT: ");
    Serial.println(BROKER_MQTT);
    if (MQTT.connect(ID_MQTT))
    {
      Serial.println("✔ Conectado com sucesso ao broker MQTT!");
      MQTT.subscribe(TOPICO_SUBSCRIBE);
    }
    else
    {
      Serial.println("✖ Falha ao reconectar no broker");
      Serial.println("✖ Haverá nova tentativa de conexão em 2s");
      delay(1000);
    }
  }
}

void initWiFi()
{
  delay(10);
  Serial.println("Conexao WI-FI");
  Serial.print("Conectando-se na rede: ");
  Serial.println(SSID);
  Serial.println("Aguarde");
  reconectWiFi();
}

void initMQTT()
{
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
}

void initPin()
{
  pinMode(DATA_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(EXTRA_PIN, OUTPUT);   // Pino para indicar efiencia energetica maxima
  digitalWrite(EXTRA_PIN, LOW); // Inicializa a indicação de efiencia energetica maxima como desligada
}

void initSerial()
{
  Serial.begin(115200);
  delay(1000);
}

void servoSetup()
{
  servoMotor.attach(servoPin, 500, 2400); // Configuração dos pulsos para ESP32
  servoMotor.write(posicaoServo);         // Define posição inicial do servo
}

void handleSolarLight()
{
  // Lê a intensidade de luz dos LDRs e utiliza a função map
  int luminosity1 = map(analogRead(ldr1Pin), 0, 4095, 100, 0);
  int luminosity2 = map(analogRead(ldr2Pin), 0, 4095, 100, 0);

  // Exibe os valores dos LDRs no monitor serial
  Serial.println("----=()=----");
  Serial.print("Luz LDR 1: ");
  Serial.println(luminosity1);
  Serial.print("Luz LDR 2: ");
  Serial.println(luminosity2);

  // Movimenta o servo para o lado que recebe mais luz solar
  if (luminosity1 > luminosity2 + 5) // Ajuste de 5% para evitar pequenas variacões
  {
    posicaoServo = min(posicaoServo + 6, 180); // Move para a direita
    servoMotor.write(posicaoServo);
    Serial.println("Correção para a direita");
  }
  else if (luminosity2 > luminosity1 + 5)
  {
    posicaoServo = max(posicaoServo - 6, 0); // Move para a esquerda
    servoMotor.write(posicaoServo);
    Serial.println("Correção para a esquerda");
  }
  else
  {
    Serial.println("Nenhuma mudança de correção");
  }

  // Atualiza o nível de carga com a média das leituras
  totalLuminosity = (luminosity1 + luminosity2) / 2;
  Serial.print("Eficiência: ");
  Serial.print(totalLuminosity);
  Serial.println("%");

  // Publicação dos dados via MQTT
  String mensagemOeste = String(luminosity1);
  String mensagemLeste = String(luminosity2);
  String mensagemEff = String(totalLuminosity);

  // Publica os dados de umidade e temperatura via MQTT como texto simples
  MQTT.publish(TOPICO_PUBLISH_W, mensagemOeste.c_str());
  MQTT.publish(TOPICO_PUBLISH_E, mensagemLeste.c_str());
  MQTT.publish(TOPICO_PUBLISH_EFF, mensagemEff.c_str());
}

// Função para atualizar os LEDs conforme o nível de efiencia energetica
void updateLeds()
{
  // Mapeia o nível de carga para o número de LEDs a serem acesos
  int ledsToLight = map(totalLuminosity, 0, 100, 0, numLeds);

  // Variável para armazenar o padrão dos LEDs
  byte ledPattern = 0;

  // Define os bits de `ledPattern` para acender os LEDs necessários
  for (int i = 0; i < ledsToLight; i++)
  {
    ledPattern |= (1 << i); // Liga os LEDs até o índice `ledsToLight`
  }

  // Envia o padrão para o shift register
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, ledPattern); // Envia o padrão de bits
  digitalWrite(LATCH_PIN, HIGH);

  // Se todos os LEDs estiverem acesos, indica que aeficiencia energética está no máximo
  if (ledsToLight == numLeds)
  {
    digitalWrite(EXTRA_PIN, HIGH); // Liga a indicação de eficiencia energética máxima
  }
  else
  {
    digitalWrite(EXTRA_PIN, LOW); // Desliga a indicação de eficiencia energética máxima
  }
}
