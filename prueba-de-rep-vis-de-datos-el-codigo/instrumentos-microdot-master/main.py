from bmp280 import *
import time

def connect_to(ssid: str, passwd: str):
    import network
    ssid = 'Red Profesores'
    passwd ='Profes_IMPA_2022'
    # Creo una instancia para interfaz tipo station
    sta_if = network.WLAN(network.STA_IF)
    # Verifico que no este conectado ya a la red
    if not sta_if.isconnected():
        # Activo la interfaz
        sta_if.active(True)
        # Intento conectar a la red
        sta_if.connect(ssid, passwd)
        # Espero a que se conecte
        while not sta_if.isconnected():
            pass
        # Retorno direccion de IP asignada
    return sta_if.ifconfig()[0]
        
# Importo lo necesario para la aplicacion de Microdot
from microdot import Microdot, send_file
# Creo una instancia de Microdot
app = Microdot()

@app.route("/")
def index(request):
    return send_file("index.html")


@app.route("/assets/<dir>/<file>")
def assets(request,dir, file):
    return send_file('/assets/'+ dir+ '/'+ file)

@app.route("/data/update")
def data_update(request):
    # Importo ADC
    from machine import Pin,I2C
    bus = I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
    bmp = BMP280(bus)

    bmp.use_case(BMP280_CASE_INDOOR)
    sensor_temp = bmp.temperature
    # Leo dato del sensor y ajusto
    lectura = sensor_temp.read_u16() * 3.3 / (1 << 16)
    # Ajusto para leer la temperatura
    temperatura_cpu = lectura * 40
    print (temperatura_cpu)
    # Retorno el diccionario
    return { "cpu_temp" : temperatura_cpu }
# Programa principal, verifico que el archivo sea el main.py
if __name__ == "__main__": 
    try:
        # Me conecto a internet
        ip = connect_to("Red Proesores", "Profes_IMPA_2022")
        # Muestro la direccion de IP
        print("Microdot corriendo en IP/Puerto: " + ip + ":5000")
        # Inicio la aplicacion
        app.run()
    except KeyboardInterrupt:
        # Termina el programa con Ctrl + C
        print("Aplicacion terminada")