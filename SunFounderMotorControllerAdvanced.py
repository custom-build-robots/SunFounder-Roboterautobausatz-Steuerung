#!/usr/bin/env python
# coding: latin-1
# Autor:   Ingmar Stapel
# Datum:   20170812
# Version:   1.1
# Homepage:   http://custom-build-robots.com
# Dieses Programm ist das sogenannte Steuerprogramm fuer das Roboter
# Auto von SunFounder ueber die Konsole und Tastatur vom PC aus.

# Hinweis: 
# Es muss noch das Modul readchar mit dem folgenden 
# Befehl installiert werden.
# Befehl: sudo pip install readchar

# Es werden verschiedene Python Klassen importiert deren Funktionen
# im Programm benoetigt werden fuer die Programmverarbeitung.
import sys, tty, termios, os, readchar

# Das Programm SunFounderMotorController.py wird als Modul geladen. 
# Es stellt die Funktionen fuer die Steuerung der H-Bruecke zur 
# Verfuegung.
import SunFounderMotorControllerAdvanced as MotorControl

# Variablen Definition der Geschwindigkeit der Motoren des Roboter
# Autos.
speed = 0

# Variablen Definition des Lenkwinkels des Lenk-Servo Motors.
# Die neutrale Stellung war bei mit 530 erreicht. 
# Diese kann aber sehr sicher abweichen und hier muss ausprobiert 
# werden was zu Deinem Auto am besten passt.
steering_value = 530

# Variablen Definition des Schwenkwinkels der Kamera.
# Die neutrale Stellung der Kamera war bei mit 530 erreicht. 
# Diese kann aber sehr sicher abweichen und hier muss ausprobiert 
# werden was zu Deinem Auto am besten passt.
pan = 440


# Variablen Definition des Neigens der Kamera.
# Die neutrale Stellung der Kamera war bei mit 530 erreicht. 
# Diese kann aber sehr sicher abweichen und hier muss ausprobiert 
# werden was zu Deinem Auto am besten passt.
tilt = 260

# Die Variable camera_mode setzt den Modus ob die Kaerma der 
# Lenkbewegung folgt oder manuell gesteuert wird.
camera_mode = "a"

# Das Menue fuer den Anwender wenn er das Programm ausfuehrt.
# Das Menue erklaert mit welchen Tasten das Auto gesteuert wird.
print("w/s: beschleunigen")
print("a/d: lenken")
print("j/l: Kamera links / rechts")
print("q: stoppt die Motoren")
print("x: Programm beenden")

# Die Funktion getch() nimmt die Tastatureingabe des Anwenders
# entgegen. Die gedrueckten Buchstaben werden eingelesen. Sie werden
# benoetigt um die Richtung und Geschwindigkeit des Roboter-Autos
# festlegen zu koennen.
def getch():
   ch = readchar.readchar()
   return ch

# Die Funktion printscreen() gibt immer das aktuelle Menue aus
# sowie die Geschwindigkeit der linken und rechten Motoren wenn
# es aufgerufen wird.
def printscreen():
   # der Befehl os.system('clear') leert den Bildschirmihalt vor
   # jeder Aktualisierung der Anzeige. So bleibt das Menue stehen
   # und die Bildschirmanzeige im Terminal Fenster steht still.
   os.system('clear')
   print("w/s: beschleunigen")
   print("a/d: lenken")
   print("j/l: Kamera links / rechts")
   print("q: stoppt die Motoren")
   print("x: Programm beenden")
   print("================= Fahrzeuganzeige ================")
   print "Geschwindigkeit der Motoren:      ", speed
   print "Lenkeinschlag des Roboter Autos: ",  steering_value
   print "Kamera Drehung des Roboter Autos: ",  pan
   print "Kamera Neigung des Roboter Autos: ",  tilt
   
# Diese Endlosschleife wird erst dann beendet wenn der Anwender 
# die Taste X tippt. Solange das Programm laeuft wird ueber diese
# Schleife die Eingabe der Tastatur eingelesen.
while True:
   # Mit dem Aufruf der Funktion getch() wird die Tastatureingabe 
   # des Anwenders eingelesen. Die Funktion getch() liesst den 
   # gedrueckte Buchstabe ein und uebergibt diesen an die 
   # Variablechar. So kann mit der Variable char weiter 
   # gearbeitet werden.
   char = getch()
   
   # Das Roboter-Auto faehrt vorwaerts wenn der Anwender die 
   # Taste "w" drueckt.
   if(char == "w"):
      # das Roboter-Auto beschleunigt in Schritten von 10% 
      # mit jedem Tastendruck des Buchstaben "w" bis maximal 
      # 100%. Dann faehrt es maximal schnell vorwaerts.
      speed = speed + 0.1

      if speed > 1:
         speed = 1

      # Dem Programm SunFounderMotorController.py welches zu beginn  
      # importiert wurde wird die Geschwindigkeit fuer 
      # die Motoren uebergeben.
      MotorControl.setMotorPower(speed)
      printscreen()

   # Das Roboter-Auto faehrt rueckwaerts wenn die Taste "s" 
   # gedrueckt wird.
   if(char == "s"):
      # das Roboter-Auto bremst in Schritten von 10% 
      # mit jedem Tastendruck des Buchstaben "s" bis maximal 
      # -100%. Dann faehrt es maximal schnell rueckwaerts.
      speed = speed - 0.1

      if speed < -1:
         speed = -1
         
      # Dem Programm L298NMotorControl welches zu beginn  
      # importiert wurde wird die Geschwindigkeit fuer 
      # die linken und rechten Motoren uebergeben.      
      MotorControl.setMotorPower(speed)
      printscreen()

    # mit dem druecken der Taste "q" werden die Motoren angehalten
   if(char == "q"):
      speed = 0
      MotorControl.setMotorPower(speed)
      # Dreht die Servo Motoren auf einen definierten
      # Ausgangszustand.	
      steering_value = 530
      pan = 440
      tilt = 260	  
      MotorControl.setSteering(steering_value)
      MotorControl.setTiltCamera(tilt)
      MotorControl.setPanCamera(pan)
      printscreen()

   # Kamera schwenkt manuell nach links.
   if(char == "j"):
      pan = pan + 10
         
      if pan > 660:
         pan = 660      

      MotorControl.setPanCamera(pan)
      printscreen()
	  
   # Kamera schwenkt manuell nach rechts.
   if(char == "l"):
      pan = pan - 10
         
      if pan < 230:
         pan = 230
      
      MotorControl.setPanCamera(pan)
      printscreen()

   # Kamera neigen manuell nach links.
   if(char == "i"):
      tilt = tilt + 10
         
      if tilt > 660:
         tilt = 660      

      MotorControl.setTiltCamera(tilt)
      printscreen()
	  
   # Kamera neigen manuell nach rechts.
   if(char == "k"):
      tilt = tilt - 10
         
      if tilt < 230:
         tilt = 230
      
      MotorControl.setTiltCamera(tilt)
      printscreen()
	  
   # Mit der Taste "d" lenkt das Auto nach rechts. Dazu wird der
   # Servo Motor angesteuert.
   if(char == "d"):      
      steering_value = steering_value + 10
      
      if steering_value > 620:
         steering_value = 620
      
      MotorControl.setSteering(steering_value)
      printscreen()
   
   # Mit der Taste "a" lenkt das Auto nach links bis die max/min
   # Geschwindigkeit der linken und rechten Motoren erreicht ist.
   if(char == "a"):
      steering_value = steering_value - 10
         
      if steering_value < 440:
         steering_value = 440
      
      MotorControl.setSteering(steering_value)
      printscreen()
	  
   # Mit der Taste "x" wird die Endlosschleife beendet 
   # und das Programm wird ebenfalls beendet. Zum Schluss wird 
   # noch die Funktion exit() aufgerufen die die Motoren stoppt.
   if(char == "x"):
      speed = 0
      MotorControl.setMotorPower(speed)
      # Dreht die Servo Motoren auf einen definierten
      # Ausgangszustand beim Beenden des Programmes.
      steering_value = 530
      pan = 440
      tilt = 260	  
      MotorControl.setSteering(steering_value)
      MotorControl.setTiltCamera(tilt)
      MotorControl.setPanCamera(pan)	  
      MotorControl.exit()
      print("Program Ended")
      break
   
   # Die Variable char wird pro Schleifendurchlauf geleert. 
   # Das ist notwendig um weitere Eingaben sauber zu übernehmen.
   char = ""
   
# Ende des Programmes
