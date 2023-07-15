from machine import Pin, SoftI2C
from time import sleep
import network, socket
import random
import ssd1306
import neopixel
import retea


i2c=SoftI2C(sda=Pin(4), scl=Pin(5), freq=100000)
oled=ssd1306.SSD1306_I2C(128,64,i2c)
led_neopixel=Pin(14, Pin.OUT)
np=neopixel.NeoPixel(led_neopixel, 8)


lista_raspunsuri=['Da','Nu','Ma mai gandesc']

def aflam_raspuns():
    return lista_raspunsuri[random.getrandbits(len(lista_raspunsuri)-1)-1]

def clear_all():
    for i in range(0,8):
        np[i]=(0,0,0)
    np.write()
    
def fill_neopixel(nr):
    if nr==0:
        clear_all()
    else:
        if nr>8:
            nr=8
        else:
            for i in range(0,nr):
                c1=random.getrandbits(8)
                c2=random.getrandbits(8)
                c3=random.getrandbits(8)
                np[i]=(c1,c2,c3)
            np.write()
        
def conectare(nume, parola):
    sta_if=network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        nr_conectari=10
        sta_if.connect(nume, parola)
        while nr_conectari!=0 and not sta_if.isconnected():
            nr_conectari-=1
            sleep(1)
            print('Conectare in derulare ')
        if nr_conectari>0:
            ip=sta_if.ifconfig()[0]
        else:
            ip=None
    else:
        ip=sta_if.ifconfig()[0]
    return ip
    

def main():
    ip=conectare(retea.nume_retea, retea.parola)
    if ip==None:
        print("Conectarea nu s-a putut efectua cu succes !")
    else:
        print(" IP-ul clientului este = "+str(ip))
        while True:
            try:
                clear_all()
                s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('192.168.0.100',80))
                oled.text('* IP-client * ',1,1)
                oled.text(str(ip),1,15)   
                
                nr_leduri=s.recv(512).decode()
               
                if int(nr_leduri)==1:
                    print('Aprindem '+str(nr_leduri)," led ")
                    oled.text('   Aprindem ',1,35)
                    oled.text("  "+str(nr_leduri)+' led ',10,50)                
                else:    
                    print('Aprindem '+str(nr_leduri)," leduri ")
                    oled.text('   Aprindem ',1,35)
                    oled.text("  "+str(nr_leduri)+' leduri ',10,50)                
                oled.show()
                sleep(1)
                oled.fill(0)
                print()
                fill_neopixel(int(nr_leduri))
               
                raspuns=aflam_raspuns()
                print('Continuam? (Da/Nu/Ma mai gandesc ... ) ')
                print('Raspuns  =====> '+raspuns)
                sleep(3)
                s.send(raspuns.encode())
                s.close()
                if raspuns=='Nu' and int(nr_leduri)==0:
                    clear_all()
                    break
                print()
            
            except OSError as err:
              s.close()
              break
        print('Bye bye ')
                
main()
