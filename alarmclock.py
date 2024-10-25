import datetime
import time
import pygame  # Import pygame


pygame.mixer.init()

# Set the alarm time
Alarm_hour = int(input("Enter Hour: "))
Alarm_minute = int(input("Enter Minute: "))
am_pm = input("AM/PM: ").strip().upper()

if am_pm == "PM" and Alarm_hour != 12:
    Alarm_hour += 12
elif am_pm == "AM" and Alarm_hour == 12:
    Alarm_hour = 0

print(f"Alarm set for {Alarm_hour:02}:{Alarm_minute:02}")

while True:
    now = datetime.datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    if current_hour == Alarm_hour and current_minute == Alarm_minute:
        print("Playing Sound.....")
        pygame.mixer.music.load("alarmsound.mp3")  # Load alarm sound
        pygame.mixer.music.play()  # Play the sound
        
        break
    
