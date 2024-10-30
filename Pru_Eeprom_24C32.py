#File: Pru_Eeprom_24C32.py

# from machine import Pin, I2C
from machine import Pin, I2C
#importar modulo eeprom_24C32
#Colocar fichero: 'Eeprom_24C32.py'
#En memoria flash RP2040 device, carpeta '/lib' o raiz '/'
import Eeprom_24C32
import time

# Definir parámetros del bus i2c0
i2c0 = I2C(0,scl=Pin(1), sda=Pin(0), freq=100000)

#Escanear Dispositivos del Bus i2c0
print("i2c0 scan: ", i2c0.scan())
print()
#Crear un ojeto de la Clase RTC_DS1307 definido en el modulo rtc_ds1307
eeprom = Eeprom_24C32.EEPROM_24C32(i2c0, 0x50, debug=False)

#Imprimir capacidad de la memoria eeprom en bytes
print('Capacidad Memoria:',eeprom.capacidad(),'bytes')
print()
time.sleep(1)

print("Escribir buf en eeprom, a partir de la Addr=8")
#bytearray para escribir en la memoria
buf = bytearray([ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,
                  40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79 ])
print('buf a escribir:', list(buf))
#Escribir buffer en memoria eeprom a partir de la dirección '8'
eeprom.write(8,buf)
print()
time.sleep(1)

#Leer 80 bytes, a partie de la dirección 0
#los convertirmos en una lista para facilitar la lectura decimal de los valores leidos
print("Leer 80 bytes en la eeprom a partir de la Addr=8")
print('leido eeprom:  ', list(eeprom.read(8,80)))

print()
time.sleep(1)

#Leer una pagina de memoria (0 .., 127) de 32bytes
print("Leer paginas de 32 bytes de la memoria eeprom, page = 0,1,2")
eeprom.read_page(0)
eeprom.read_page(1)
eeprom.read_page(2)
print()
time.sleep(1)

#Introducir 'S' si queremos borrar la memoria completa
sel = input("Borrado Completo Memoria Eeprom S/N:")
if sel == 'S':
    eeprom.erase_mem()