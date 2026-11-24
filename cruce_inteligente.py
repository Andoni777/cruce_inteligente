#!/usr/bin/env python3
import RPi.GPIO as GPIO
from gpiozero import LED
from time import sleep
import multiprocessing
import time
from queue import Queue
from threading import Event, Thread, Timer
GPIO.setmode(GPIO.BCM)
from gpiozero import Buzzer, Button, LED

#declaracion de pines
ledCocheRojo = LED(17)
ledCocheAmbar = LED(27)
ledCocheVerde = LED(22)

ledPeatonRojo = LED(23)
ledPeatonVerde = LED(24)

botonPeatonIzq = 5
botonPeatonDer = 6
# Configurar botón como entrada con pull-up
GPIO.setup(botonPeatonIzq, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(botonPeatonDer, GPIO.IN, pull_up_down=GPIO.PUD_UP)

contador = 0

buzzer = Buzzer(16)

#bool noche = False

def boton_presionado(canal):
    global contador
    if contador == 0:  
        
        contador = 1
        print("Botón presionado. Contador:", contador)
    else:
        print("Ya esta Pulsaso, Contador En CoolDown espere")

GPIO.add_event_detect(botonPeatonIzq, GPIO.FALLING, callback=boton_presionado, bouncetime=300)
GPIO.add_event_detect(botonPeatonDer, GPIO.FALLING, callback=boton_presionado, bouncetime=300)



def coche_si_persona_no():
    ledCocheVerde.on()
    ledCocheAmbar.off()
    ledCocheRojo.off()
    ledPeatonRojo.on()
    ledPeatonVerde.off()
    sleep(2)

def cocheSiPrecaucionPersonaNo():
    ledCocheVerde.off()
    for i in range(5):
        ledCocheAmbar.on()
        sleep(0.5)
        ledCocheAmbar.off()
        sleep(0.5)

def cocheNoPersonaNo():
    ledCocheAmbar.off()
    ledCocheRojo.on()
    sleep(3)

def  cocheNoPersonaSi():
    ledCocheVerde.off()
    ledCocheAmbar.off()
    ledCocheRojo.on()
    ledPeatonRojo.off()
    ledPeatonVerde.on()
    sleep(2)

def cocheNoPersonaSiPrisa():      
    for i in range(3):
        ledPeatonVerde.on()
        buzzer.on()
        sleep(0.5)
        ledPeatonVerde.off()
        buzzer.off()
        sleep(0.5)        
    
def cocheNoPersonaNoFinal():
    ledPeatonVerde.off()
    ledPeatonRojo.on()
    sleep(3)

def main():
    global contador
    try:
        while True:
           
            coche_si_persona_no()

            if (contador == 1):  # Aquí puedes agregar la condición para detectar si hay una persona esperando
                cocheSiPrecaucionPersonaNo()

                cocheNoPersonaNo()

                cocheNoPersonaSi()

                cocheNoPersonaSiPrisa()

                cocheNoPersonaNoFinal()
                coche_si_persona_no()
                print("Contador En CoolDown espere 15s")
                sleep(15)  # Pequeña pausa para evitar rebotes
                contador = 0  # Reiniciar el contador después de que la persona haya cruzado
                print("Contador Reiniciado:", contador)
            
            

            
    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario.")

    finally:
        ledCocheVerde.off()
        ledCocheAmbar.off()
        ledCocheRojo.off()
        ledPeatonRojo.off()
        ledPeatonVerde.off()
      
     

if __name__ == "__main__":
    main()
