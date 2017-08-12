#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20170811
# Version:   1.0
# Homepage:   http://custom-build-robots.com

# Dieses Programm wurde fuer die Ansteuerung der Motoren des 
# SunFounder Video Car entwickelt. Es folgt dabei der Belegung
# der GPIO Pins am Raspberry Pi sowie der am PCA9685 Servo
# Kontroller wie von SunFounder beschreiben.

# Hinweis:
# Es muss noch die Adafruit PCA9685 Bibliothek für dieses Programm
# unter Raspbian installiert werden.
# Eine Installationsanleitung findet Ihr auf meinem Blog hier:
# https://custom-build-robots.com/raspberry-pi-elektronik/16-kanal-pca9685-servo-kontroller-teil-3-ansteuerung-einer-l298n-h-bruecke/8821

# Dieses Programm muss von einem uebergeordneten Programm aufgerufen 
# werden, dass die Steuerung des SunFounderMotorController.py
# Programmes übernimmt.
# Dazu kann das Programm SunFounderRobotControl.py verwendet werden.

# Es wird die Klasse RPi.GPIO importiert, die die Ansteuerung
# der GPIO Pins des Raspberry Pi ermoeglicht.
from __future__ import division
import RPi.GPIO as io
io.setmode(io.BCM)

import time

# Importiere die Adafruit PCA9685 Bibliothek
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
PCA9685_pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Set frequency to 100hz, good for l298n h-bridge.
PCA9685_pwm.set_pwm_freq(60)

# Die Variable duty_cycle gibt die maximale Einschaltdauer der 
# Motoren pro 100 Herts vor. Dier liegt zwischen 0 bis 4095.
# Für die Geschwindigkeit der Motoren beginnt die Einschaltdauer
# immer bei 0 und endet bei einem Wert ]0, 4095[.
duty_cycle = 4095

# Mit dem folgenden Aufruf werden eventuelle Warnungen die die 
# Klasse RPi.GPIO ausgibt deaktiviert.
io.setwarnings(False)

# Im folgenden Programmabschnitt wird die logische Verkabelung des 
# Raspberry Pi im Programm abgebildet. Dazu werden den vom Motor 
# Treiber bekannten Pins nach BMC die GPIO Adressen zugewiesen.

# Bitte hier der Pin Belegung aus der SunFounder Anleitung folgen
# und die BCM GPIO Nummerierung verwenden und nicht die Pin Nummer.

# --- START KONFIGURATION GPIO Adressen ---
IN1 = 17
IN2 = 18
IN3 = 27
IN4 = 22
# --- ENDE KONFIGURATION GPIO Adressen ---

# Der Variable leftmotor_in1_pin wird die Varibale IN1 zugeorndet. 
# Der Variable leftmotor_in2_pin wird die Varibale IN2 zugeorndet. 
leftmotor_in1_pin = IN1
leftmotor_in2_pin = IN2
# Beide Variablen leftmotor_in1_pin und leftmotor_in2_pin werden als
# Ausgaenge "OUT" definiert. Mit den beiden Variablen wird die
# Drehrichtung der Motoren gesteuert.
io.setup(leftmotor_in1_pin, io.OUT)
io.setup(leftmotor_in2_pin, io.OUT)

# Der Variable rightmotor_in1_pin wird die Varibale IN1 zugeorndet. 
# Der Variable rightmotor_in2_pin wird die Varibale IN2 zugeorndet. 
rightmotor_in1_pin = IN3
rightmotor_in2_pin = IN4
# Beide Variablen rightmotor_in1_pin und rightmotor_in2_pin werden 
# als Ausgaenge "OUT" definiert. Mit den beiden Variablen wird die
# Drehrichtung der Motoren gesteuert.
io.setup(rightmotor_in1_pin, io.OUT)
io.setup(rightmotor_in2_pin, io.OUT)

# Die GPIO Pins des Raspberry Pi werden initial auf False gesetzt.
# So ist sichger gestellt, dass kein HIGH Signal anliegt und der 
# Motor Treiber nicht unbeabsichtigt aktiviert wird.
io.output(leftmotor_in1_pin, False)
io.output(leftmotor_in2_pin, False)
io.output(rightmotor_in1_pin, False)
io.output(rightmotor_in2_pin, False)

# Die Funktion setMotorMode(mode) legt die Drehrichtung der beiden
# Motoren fest. Die Funktion verfügt über eine Eingabevariable.
# mode      -> diese Variable legt fest welcher Modus gewaehlt ist

def setMotorMode(mode):
   if mode == "reverse":
      # Motor 1
      io.output(leftmotor_in1_pin, True)
      io.output(leftmotor_in2_pin, False)
      # Motor 2
      io.output(rightmotor_in1_pin, True)
      io.output(rightmotor_in2_pin, False) 
   elif  mode == "forward":
      # Motor 1
      io.output(leftmotor_in1_pin, False)
      io.output(leftmotor_in2_pin, True)
      # Motor 2
      io.output(rightmotor_in1_pin, False)
      io.output(rightmotor_in2_pin, True)
   # Stoppen der beiden Motoren
   else:
      io.output(leftmotor_in1_pin, False)
      io.output(leftmotor_in2_pin, False)
      io.output(rightmotor_in1_pin, False)
      io.output(rightmotor_in2_pin, False)

# Die Funktion setMotorPower(power) setzt die Geschwindigkeit der 
# beiden Motoren. Die Geschwindigkeit wird als Wert zwischen -1
# und 1 uebergeben. Bei einem negativen Wert sollen sich die Motoren 
# rueckwaerts drehen ansonsten vorwaerts. 
# Anschliessend werden aus den uebergebenen Werten die notwendigen 
# %-Werte fuer das PWM Signal berechnet.

# Beispiel:
# Die Geschwindigkeit kann mit +1 (max) und -1 (min) gesetzt werden.
# Das Beispielt erklaert wie die Geschwindigkeit berechnet wird.
# SetMotorLeft(0)     -> der linke Motor dreht mit 0% ist gestoppt
# SetMotorLeft(0.75)  -> der linke Motor dreht mit 75% vorwaerts
# SetMotorLeft(-0.5)  -> der linke Motor dreht mit 50% rueckwaerts
# SetMotorLeft(1)     -> der linke Motor dreht mit 100% vorwaerts
def setMotorPower(power):
   int(power)
   if power < 0:
      # Rueckwaertsmodus fuer die beiden Motoren
      setMotorMode("reverse")
      pwm = -int(duty_cycle * power)
      if pwm > duty_cycle:
         pwm = duty_cycle
   elif power > 0:
      # Vorwaertsmodus fuer die beiden Motoren
      setMotorMode("forward")
      pwm = int(duty_cycle * power)
      if pwm > duty_cycle:
         pwm = duty_cycle
   else:
      # Stoppmodus fuer die beiden Motoren
      setMotorMode("stopp")
      pwm = 0
   # Hier werden die beiden PWM Leitungen zu dem Motor Treiber
   # angesteuert. Hier auch bitte wieder die Pin Belegung aus der 
   # Anleitung von SunFounder beachten.
 
   PCA9685_pwm.set_pwm(4, 0, pwm)
   PCA9685_pwm.set_pwm(5, 0, pwm)

# Die Lenkung in dem SunFounder Roboter Auto ist mit einem Servo 
# Motor umgesetzt. Die folgende Funktion setSteering(value) 
# steuert den Servo Motor an und lenkt somit das Roboter Auto.
def setSteering(value):
   int(value)
   # Es wird der initiale duty_cycle durch zwei dividiert, da 
   # die neutrale Stellung des Servo Motors in der Mitte sein 
   # sollte für die geradeaus Fahrt.
   # Wenn dem so nicht ist, kann mit der variable trim eine
   # manuelle Anpassung / Korrektur vorgenommen werden.
   trim = 0
#   steering_pwm = int(duty_cycle/2 + value) + trim
   steering_pwm = int(value) + trim   
   if steering_pwm > duty_cycle:
      steering_pwm = duty_cycle
   elif steering_pwm < 0:
      steering_pwm = 0
   # Jetzt wird der Servo für die Lenkung angesprochen
   PCA9685_pwm.set_pwm(0, 0, steering_pwm) 
   
   
# Mit dieser Funktion kann die Kamera nach links / recht geschwenkt
# werden. So ist z. B. das folgen der Lenkbewegung möglich.
def setPanCamera(value):
   int(value)
   trim = 0
   pan = int(value) + trim  
   
   PCA9685_pwm.set_pwm(14, 0, pan)

def setTiltCamera(value):
   int(value)
   trim = 0
   pan = int(value) + trim  
   
   PCA9685_pwm.set_pwm(15, 0, pan) 

   
# Die Funktion exit() setzt die Ausgaenge die den Motor Treiber 
# steuern auf False. So befindet sich der Motor Treiber nach dem 
# Aufruf derFunktion in einem gesicherten Zustand und die Motoren 
# sind gestopped.
def exit():
   io.output(leftmotor_in1_pin, False)
   io.output(leftmotor_in2_pin, False)
   io.output(rightmotor_in1_pin, False)
   io.output(rightmotor_in2_pin, False)
   io.cleanup()
   
# Ende des Programmes
