import datetime
import time
import pygame
from typing import Optional
import sys

class AlarmClock:
    def __init__(self):
        """Initialize the alarm clock with pygame mixer and default values."""
        pygame.mixer.init()
        self.alarms = []
        self.is_running = True
        self.snooze_duration = 5  # Default snooze time in minutes

    def validate_time(self, hour: int, minute: int, second: int, am_pm: str) -> bool:
        """Validate the input time values."""
        if not (0 <= hour <= 12):
            print("Invalid hour. Please enter a number between 0 and 12.")
            return False
        if not (0 <= minute <= 59):
            print("Invalid minute. Please enter a number between 0 and 59.")
            return False
        if not (0 <= second <= 59):
            print("Invalid second. Please enter a number between 0 and 59.")
            return False
        if am_pm.upper() not in ['AM', 'PM']:
            print("Invalid AM/PM value. Please enter either AM or PM.")
            return False
        return True

    def convert_to_24hr(self, hour: int, am_pm: str) -> int:
        """Convert 12-hour format to 24-hour format."""
        if am_pm.upper() == 'PM' and hour != 12:
            return hour + 12
        elif am_pm.upper() == 'AM' and hour == 12:
            return 0
        return hour

    def format_time(self, hour: int, minute: int, second: int) -> str:
        """Format time in 12-hour format with AM/PM."""
        am_pm = 'AM' if hour < 12 else 'PM'
        if hour > 12:
            hour -= 12
        elif hour == 0:
            hour = 12
        return f"{hour:02}:{minute:02}:{second:02} {am_pm}"

    def time_until_alarm(self, alarm: dict) -> str:
        """Calculate and return time remaining until alarm."""
        now = datetime.datetime.now()
        alarm_time = now.replace(
            hour=alarm['hour'],
            minute=alarm['minute'],
            second=alarm['second']
        )
        
        if alarm_time <= now:
            alarm_time += datetime.timedelta(days=1)
            
        time_diff = alarm_time - now
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def set_alarm(self) -> None:
        """Set a new alarm with user input."""
        try:
            print("\n=== Set New Alarm ===")
            hour = int(input("Enter Hour (1-12): "))
            minute = int(input("Enter Minute (0-59): "))
            second = int(input("Enter Second (0-59): "))
            am_pm = input("AM/PM: ").strip()
            
            if not self.validate_time(hour, minute, second, am_pm):
                return

            print("\nChoose alarm type:")
            print("1. One-time alarm")
            print("2. Daily alarm")
            alarm_type = input("Enter choice (1-2): ")
            
            sound_choice = input("Choose alarm sound (1: Beep, 2: Music): ")
            
            hour_24 = self.convert_to_24hr(hour, am_pm)
            sound_file = "alarmsound.mp3" if sound_choice == "2" else "beep.wav"
            
            alarm_info = {
                'hour': hour_24,
                'minute': minute,
                'second': second,
                'sound': sound_file,
                'enabled': True,
                'repeat': alarm_type == "2"
            }
            
            self.alarms.append(alarm_info)
            time_str = self.format_time(hour_24, minute, second)
            print(f"\nAlarm set for {time_str}")
            print(f"Time until alarm: {self.time_until_alarm(alarm_info)}")
            print(f"Total alarms set: {len(self.alarms)}")

        except ValueError:
            print("Please enter valid numbers for hour, minute, and second.")

    def show_alarms(self) -> None:
        """Display all set alarms."""
        if not self.alarms:
            print("\nNo alarms set.")
            return

        print("\n=== Current Alarms ===")
        for i, alarm in enumerate(self.alarms, 1):
            time_str = self.format_time(alarm['hour'], alarm['minute'], alarm['second'])
            status = "Enabled" if alarm['enabled'] else "Disabled"
            repeat = "Daily" if alarm['repeat'] else "One-time"
            time_remaining = self.time_until_alarm(alarm)
            print(f"{i}. {time_str} - {status} - {repeat}")
            print(f"   Time remaining: {time_remaining}")

    def toggle_alarm(self) -> None:
        """Enable or disable an alarm."""
        self.show_alarms()
        if not self.alarms:
            return

        try:
            alarm_index = int(input("\nEnter alarm number to toggle (0 to cancel): ")) - 1
            if alarm_index == -1:
                return
            if 0 <= alarm_index < len(self.alarms):
                self.alarms[alarm_index]['enabled'] = not self.alarms[alarm_index]['enabled']
                status = "enabled" if self.alarms[alarm_index]['enabled'] else "disabled"
                print(f"\nAlarm {alarm_index + 1} {status}")
            else:
                print("Invalid alarm number.")
        except ValueError:
            print("Please enter a valid number.")

    def handle_alarm(self, alarm: dict) -> None:
        """Handle alarm when it goes off."""
        pygame.mixer.music.load(alarm['sound'])
        pygame.mixer.music.play(-1)  # Loop the sound

        while True:
            action = input("\nAlarm! Enter 'S' for snooze, 'D' for dismiss: ").upper()
            if action == 'D':
                pygame.mixer.music.stop()
                if not alarm['repeat']:
                    alarm['enabled'] = False
                break
            elif action == 'S':
                pygame.mixer.music.stop()
                print(f"Snoozed for {self.snooze_duration} minutes...")
                time.sleep(self.snooze_duration * 60)
                pygame.mixer.music.play(-1)

    def check_alarms(self) -> None:
        """Check if any alarms should go off."""
        now = datetime.datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        current_second = now.second

        for alarm in self.alarms:
            if (alarm['enabled'] and 
                alarm['hour'] == current_hour and 
                alarm['minute'] == current_minute and 
                alarm['second'] == current_second):
                print(f"\nTime to wake up! It's {self.format_time(current_hour, current_minute, current_second)}")
                self.handle_alarm(alarm)

    def delete_alarm(self) -> None:
        """Delete an existing alarm."""
        self.show_alarms()
        if not self.alarms:
            return

        try:
            alarm_index = int(input("\nEnter alarm number to delete (0 to cancel): ")) - 1
            if alarm_index == -1:
                return
            if 0 <= alarm_index < len(self.alarms):
                deleted_alarm = self.alarms.pop(alarm_index)
                time_str = self.format_time(deleted_alarm['hour'], deleted_alarm['minute'], deleted_alarm['second'])
                print(f"\nAlarm at {time_str} has been deleted")
            else:
                print("Invalid alarm number.")
        except ValueError:
            print("Please enter a valid number.")

    def run(self) -> None:
        """Main loop of the alarm clock program."""
        print("\nWelcome to Enhanced Alarm Clock!")
        
        while self.is_running:
            print("\n=== Menu ===")
            print("1. Set New Alarm")
            print("2. Show Alarms")
            print("3. Toggle Alarm")
            print("4. Delete Alarm")
            print("5. Set Snooze Duration")
            print("6. Exit")
            
            try:
                choice = input("\nEnter your choice (1-6): ")
                
                if choice == '1':
                    self.set_alarm()
                elif choice == '2':
                    self.show_alarms()
                elif choice == '3':
                    self.toggle_alarm()
                elif choice == '4':
                    self.delete_alarm()
                elif choice == '5':
                    minutes = int(input("Enter snooze duration in minutes: "))
                    if minutes > 0:
                        self.snooze_duration = minutes
                        print(f"Snooze duration set to {minutes} minutes")
                    else:
                        print("Please enter a positive number of minutes")
                elif choice == '6':
                    print("Goodbye!")
                    self.is_running = False
                else:
                    print("Invalid choice. Please try again.")

            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")

            self.check_alarms()
            time.sleep(1)  # Check time every second

if __name__ == "__main__":
    alarm_clock = AlarmClock()
    alarm_clock.run()