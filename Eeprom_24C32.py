# Licencia: None
'''
MODULO para 24C32 EEPROM 32Kbits (4 Kbytes)
============================================

MicroPython Modulo con una Clase para Chip 24C32 EEPROM.

*  Author: Germán de la Cruz
*  Build: V0.1
*  Ver repositorio: https://github.com/...
** Hardware: EEPROM 24C32 in RTCTiny Modules
** Software and Dependencies: micropython --> https://micropython.org/
** Notes:
    EEPROM 24C32: 128 paginas de 32 bytes por pagina = 4Kbytes = 4096 bytes
    Las operaciones de Escritura solo se pueden hacer dentro de una misma pagina
    Dirección Bus I2C = 0x50 (80 en decimal)
'''
import time

class EEPROM_24C32(object):
    #Class para el chip 24C32 32Kbits/4Kbytes EEPROM.

    def __init__(self, i2c:I2C, i2c_addr:int=0x50, pages:int=128, bpp:int=32, debug:bool=False) -> None:
        self.i2c = i2c           #Objeto I2C
        self.i2c_addr = i2c_addr #Direccion een el bus i2c
        self.pages = pages       #Paginas de la memoria
        self.bpp   = bpp         #Bytes por pagina
        self.debug = debug       #true si debug. Imprime ciertos mensajes en el REPL

    def capacidad(self)-> int:
        #Capacidad de la memoria en bytes
        return self.pages * self.bpp

    def read(self, addr:int, nbytes:int) -> bytes:
        #Las operaciones de lectura pueden abarcar varias páginas
        #Leer un byte o un grupo de 'nbytes' desde la direccion especificada por 'addr'
        time.sleep_ms(15)
        return self.i2c.readfrom_mem(self.i2c_addr, addr, nbytes, addrsize=16)
    
    def read_page(self, npage:int) -> None:
        astr = rstr = ''
        if npage >= self.pages:
            npage = 127
            print("Solo Hay 18 paginas: 0 ... 127") if self.debug else None
        addr = npage * self.bpp
        cadd = addr
        nbytes = self.bpp
        time.sleep_ms(15)
        lstBytes =list(self.i2c.readfrom_mem(self.i2c_addr, addr, nbytes, addrsize=16))
        c_lineas = 2
        for ilin in range(0, c_lineas):
            astr = '[ 0x'+ cadd.to_bytes(2,"big").hex() + ' ]'
            print(astr, end=' ') 
            for ibyte in range(0,16):
                rstr += '0x'+ lstBytes[ibyte+ilin*16].to_bytes(1, "big").hex() + ' '
                cadd+=1
            print(rstr)
            astr = rstr = ''
           
    def write_pages_mem(self, Add:int, buf:bytearray) -> None:
        #Usada por la función self.write(Add, buf)
        #Segun la dirección 'Add' y la 'len(buf)'
        #La escritura puede tener que hacerse en más de una página de la memoria
        nbytes = len(buf)
        NMAXBYTES = self.pages * self.bpp 
        Page_add = Page_i = Add // self.bpp
        Page_f = (Add+nbytes-1) // self.bpp
        NkPages = 0 
        k0 = Add
        nbytes0 = nbytes
        
        if Add+nbytes0 > NMAXBYTES:
            print("Error solo hay", NMAXBYTES ,"bytes") if self.debug else None
            nbytes0 = NMAXBYTES - Add
            
        print("Page_i:", Page_i, "Page_f:", Page_f) if self.debug else None
        #Escritura completa en solo una página de la eeprom
        if Page_i == Page_f:
            print("Adress:", Add, "nbytes:", nbytes0) if self.debug else None
            print("[",0,",",nbytes0,"]") if self.debug else None
            time.sleep_ms(15)
            self.i2c.writeto_mem(self.i2c_addr, Add, buf[0:nbytes0], addrsize=16)
        else:
            #Escritura en sucesivas paginas completas
            for k in range(Add, Add+nbytes0):
                Page_k = k // self.bpp
                if Page_k != Page_i:
                    print("Adress:", k0, "nbytes:", k-k0) if self.debug else None
                    print("[",k0-Add,",",k-Add,"]") if self.debug else None
                    time.sleep_ms(15)
                    self.i2c.writeto_mem(self.i2c_addr, k0, buf[k0-Add:k-Add], addrsize=16)
                    Page_i = Page_k
                    k0 = k
                    NkPages += 1
            #Escritura de la ultima parte en la siguiente pagina
            if NkPages <= (Page_f - Page_add):
                print("Adress:", k0, "nbytes:", Add+nbytes0-k0) if self.debug else None
                print("[",k0-Add,",",nbytes0,"]") if self.debug else None
                time.sleep_ms(15)
                self.i2c.writeto_mem(self.i2c_addr, k0, buf[k0-Add:nbytes0], addrsize=16)

    def write(self, addr:int, buf:bytearray) -> None:
        #Escribr uno o más bytes en EEPROM, a partir de una dirección 'addr' especificada
        #'buf' contine los datos a escribit.
        #Para escribir en la memoria EEPROM cada transferencia write_to_mem debe estar dentro de una misma pagina de 32 bytes.
        self.write_pages_mem(addr, buf)
        
    def erase_mem(self) -> None:
        #Borrado de todos los bits de la memoria con un valor de cero
        #Va borrando en bloques de 256 bytes (8 paginas de 32 bytes)
        #Define un 'buf0' con 256 bytes
        buf0=bytearray(256)
        for i in range(0, 16):
            self.write_pages_mem(i*256, buf0)
            time.sleep_ms(10)
            print("Erase Pagina:", i) if self.debug else None
