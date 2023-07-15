from machine import Pin, SoftI2C
from time import sleep
import network, socket
import random
import ssd1306
import retea

i2c=SoftI2C(sda=Pin(4), scl=Pin(5), freq=100000)
oled=ssd1306.SSD1306_I2C(128,64,i2c)

def conectare(nume, parola):
    sta_if=network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.ifconfig(('192.168.0.100','192.168.0.255','192.168.0.1','8.8.8.8'))
    sta_if.connect(nume, parola)
    while not sta_if.isconnected():
        pass
        sleep(1)
    return sta_if.ifconfig()[0]


def main():
    ip=conectare(retea.nume_retea, retea.parola)
    if ip==None:
        print("Conectarea nu s-a putut efectua cu succes !")
    else:
        print(" IP-ul serverului este = "+str(ip))
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('',80))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        s.listen(5)
        while True:
            oled.text('* IP-server * ',1,1)
            oled.text(str(ip),1,15)   
            oled.show()
            conn, addr=s.accept()
            print("Conectare de la adresa "+str(addr[0]))
            nr_leduri=random.getrandbits(3)
            print()
            if nr_leduri==1:
                print('Aprinde '+str(nr_leduri)," led ")
                oled.text('    Aprinde ',1,35)
                oled.text("  "+str(nr_leduri)+' led ',10,50)                
                
            else:    
                print('Aprinde '+str(nr_leduri)," leduri ")
                oled.text('    Aprinde ',1,35)
                oled.text("  "+str(nr_leduri)+' leduri ',10,50)                
              
            oled.show()
            sleep(1)
            oled.fill(0)
            
            conn.send(str(nr_leduri).encode())
            sleep(2)      
            raspuns=conn.recv(512).decode('utf-8')
            print('Continuam ? (Da/Nu/ Ma mai gandesc... )  ----> ', end=" ")
            print(raspuns)
            if nr_leduri==0 and raspuns=='Nu':
                print('Bye bye ')
                conn.close()
                break
            sleep(3)
            print()
            
                
main()

