from machine import Pin, ADC, PWM, SoftI2C
from time import sleep
import network
import dht
import ssd1306
from umqtt.simple import MQTTClient

# WIFI
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print("Conectando WiFi...")
wifi.connect("Wokwi-GUEST", "")

while not wifi.isconnected():
    print("Conectando...")
    sleep(1)

print("WiFi conectado!")
print(wifi.ifconfig())

# ATUADORES
led = Pin(2, Pin.OUT)
buzzer = Pin(18, Pin.OUT)
servo = PWM(Pin(19), freq=50)

# SENSORES
pir = Pin(13, Pin.IN)
sensor = dht.DHT22(Pin(15))

ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)

gas = ADC(Pin(35))
gas.atten(ADC.ATTN_11DB)

# OLED
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

status_porta = "FECHADA"
alerta_gas = "GAS NORMAL"

def mover_servo(angulo):
    duty = int((angulo / 180) * 102 + 26)
    servo.duty(duty)

def receber_mensagem(topic, msg):
    global status_porta

    print("Comando recebido:")
    print(topic, msg)

    if topic == b"casa/comando/led":
        if msg == b"ON":
            led.on()
        elif msg == b"OFF":
            led.off()

    elif topic == b"casa/comando/buzzer":
        if msg == b"ON":
            buzzer.on()
        elif msg == b"OFF":
            buzzer.off()

    elif topic == b"casa/comando/porta":
        if msg == b"OPEN":
            status_porta = "ABERTA"
            mover_servo(90)
        elif msg == b"CLOSE":
            status_porta = "FECHADA"
            mover_servo(0)

# MQTT
client = MQTTClient("esp32_casa_carlos", "broker.hivemq.com")
client.set_callback(receber_mensagem)
client.connect()

client.subscribe(b"casa/comando/led")
client.subscribe(b"casa/comando/buzzer")
client.subscribe(b"casa/comando/porta")

print("MQTT conectado e inscrito nos comandos!")

while True:
    client.check_msg()

    sensor.measure()

    temperatura = sensor.temperature()
    umidade = sensor.humidity()
    movimento = pir.value()
    luminosidade = ldr.read()
    nivel_gas = gas.read()

    if movimento == 1:
        status_movimento = "DETECTADO"
    else:
        status_movimento = "SEM MOV."

    if nivel_gas > 2500:
        alerta_gas = "ALERTA GAS"
        buzzer.on()
    else:
        alerta_gas = "GAS NORMAL"

    client.publish(b"casa/temperatura", str(temperatura))
    client.publish(b"casa/umidade", str(umidade))
    client.publish(b"casa/luminosidade", str(luminosidade))
    client.publish(b"casa/gas", str(nivel_gas))
    client.publish(b"casa/movimento", status_movimento)
    client.publish(b"casa/porta", status_porta)
    client.publish(b"casa/alerta_gas", alerta_gas)

    oled.fill(0)
    oled.text("Temp: {}C".format(temperatura), 0, 0)
    oled.text("Umid: {}%".format(umidade), 0, 10)
    oled.text("Luz: {}".format(luminosidade), 0, 20)
    oled.text("Gas: {}".format(nivel_gas), 0, 30)
    oled.text("Porta: {}".format(status_porta), 0, 40)
    oled.text(alerta_gas, 0, 50)
    oled.show()

    print("Temp:", temperatura)
    print("Umid:", umidade)
    print("Movimento:", status_movimento)
    print("Luz:", luminosidade)
    print("Gas:", nivel_gas)
    print("Porta:", status_porta)
    print(alerta_gas)
    print("MQTT atualizado")
    print("--------------------")

    sleep(2)