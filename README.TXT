# Sistema IoT de Automação Residencial com ESP32

## Descrição

Este projeto implementa um sistema de automação residencial utilizando ESP32, com os seguintes recursos:

* Monitoramento de temperatura e umidade (DHT22)
* Detecção de movimento (PIR)
* Monitoramento de luminosidade (LDR)
* Detecção de gás
* Controle de porta automática por servo motor
* Display OLED para visualização local
* Comunicação MQTT para monitoramento remoto
* Controle remoto de LED, buzzer e porta

---

## Instalação

Antes de executar o projeto, é necessário instalar automaticamente o arquivo principal do sistema e a biblioteca do display OLED.

Abra o terminal do MicroPython e execute os comandos abaixo **na ordem apresentada**.

### 1. Instalar o arquivo main.py

```python
exec("import network, urequests, time\nsta=network.WLAN(network.STA_IF);sta.active(True);sta.connect('Wokwi-GUEST','')\nwhile not sta.isconnected(): time.sleep(0.1)\nr=urequests.get('https://pastebin.com/raw/PqRVnYiy')\nf=open('main.py','w');f.write(r.text);f.close();r.close()\nprint('main.py gravado permanentemente com sucesso!')")
```

---

### 2. Instalar a biblioteca SSD1306

```python
exec("import network, urequests, time\nsta=network.WLAN(network.STA_IF);sta.active(True);sta.connect('Wokwi-GUEST','')\nwhile not sta.isconnected(): time.sleep(0.1)\nr=urequests.get('https://raw.githubusercontent.com/stlehmann/micropython-ssd1306/master/ssd1306.py')\nf=open('ssd1306.py','w');f.write(r.text);f.close();r.close()\nprint('Biblioteca ssd1306 instalada com sucesso!')")
```

---

## Execução

Após executar os dois comandos acima com sucesso, execute:

```python
import main
```

ou reinicie a ESP32.

O sistema iniciará automaticamente e começará a:

* Conectar ao Wi-Fi
* Conectar ao broker MQTT
* Ler os sensores
* Atualizar o display OLED
* Publicar os dados MQTT
* Controlar automaticamente a porta através do sensor de movimento

---

## Tópicos MQTT

### Publicação

* casa/temperatura
* casa/umidade
* casa/luminosidade
* casa/gas
* casa/movimento
* casa/porta
* casa/alerta_gas

### Comandos

* casa/comando/led
* casa/comando/buzzer
* casa/comando/porta

#### Comandos disponíveis

LED:

```text
ON
OFF
```

Buzzer:

```text
ON
OFF
```

Porta:

```text
OPEN
CLOSE
```

---

## Hardware Utilizado

* ESP32
* Sensor DHT22
* Sensor PIR
* Sensor LDR
* Sensor de Gás
* Servo Motor SG90
* Display OLED SSD1306
* LED
* Buzzer

---

## Autor

Leonardo Giampaglia Gomes

Projeto desenvolvido para fins acadêmicos e demonstração de conceitos de Internet das Coisas (IoT), automação residencial e comunicação MQTT.
