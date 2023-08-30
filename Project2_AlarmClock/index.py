import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import wave
import pyaudio

alarms = []  # Global list to store alarms

def play_alarm():
    # Load the alarm sound using wave
    alarm_sound = "alarm.wav"  # Assuming the alarm sound is in the same directory as the script

    try:
        wf = wave.open(alarm_sound, 'rb')
        p = pyaudio.PyAudio()

        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        data = wf.readframes(1024)

        while data:
            stream.write(data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()
        p.terminate()
    except FileNotFoundError:
        print(f"Error: Could not find {alarm_sound} file.")
        messagebox.showerror("Error", f"Could not find {alarm_sound} file.")
    except Exception as e:
        print(f"Error: Unable to play the alarm sound - {e}")
        messagebox.showerror("Error", "Unable to play the alarm sound.")

def check_alarms(root):
    global alarms  # Declare 'alarms' as a global variable so it can be accessed within the function
    
    current_time = time.strftime("%I:%M %p")  # Get current time in 12-hour format
    for alarm in alarms:
        if alarm[0] == current_time and not alarm[1]:
            alarm[1] = True  # Set alarm as ringing
            play_alarm()

    root.after(1000, check_alarms, root)  # Schedule the check_alarms() function to run after 1 second

    root.after(1000, check_alarms, root)  # Schedule the check_alarms() function to run after 1 second

def stop_alarm(alarm_index):
    alarms[alarm_index][1] = False  # Turn off the alarm
    alarms_list.itemconfig(alarm_index, {'bg': 'white'})  # Change the background color to indicate it's off

def delete_alarm(alarm_index):
    alarms.pop(alarm_index)  # Remove the alarm from the list
    alarms_list.delete(alarm_index)  # Delete the alarm from the listbox

def set_alarm():
    global hour_var, minute_var, am_pm_var, alarms_frame, alarms  # Add 'alarms' to global variables

    hour = hour_var.get()
    minute = minute_var.get()
    am_pm = am_pm_var.get()
    alarm_time = f"{hour:02d}:{minute:02d} {am_pm}"
    messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")

    # Add the alarm to the list with a flag indicating if it is ringing
    alarms.append([alarm_time, False])

    # Create a frame for the new alarm entry
    alarm_entry_frame = ttk.Frame(alarms_frame)
    alarm_entry_frame.pack(pady=5, fill=tk.X)

    # Insert the alarm time label in the alarm entry frame
    alarm_time_label = ttk.Label(alarm_entry_frame, text=alarm_time)
    alarm_time_label.pack(side=tk.LEFT, padx=5)

    # Create "Turn Off" and "Delete" buttons for the newly added alarm
    off_button = ttk.Button(alarm_entry_frame, text="Turn Off", command=lambda index=len(alarms) - 1: stop_alarm(index))
    delete_button = ttk.Button(alarm_entry_frame, text="Delete", command=lambda index=len(alarms) - 1: delete_alarm(index))

    # Pack the buttons in the alarm entry frame
    off_button.pack(side=tk.LEFT, padx=5)
    delete_button.pack(side=tk.LEFT, padx=5)



def main():
    global hour_var, minute_var, am_pm_var, alarms_frame, root  # Declare them as global variables

    root = tk.Tk()
    root.title("Alarm Clock")
    root.geometry("400x400")

    frame = ttk.Frame(root)
    frame.pack(pady=20)

    hour_var = tk.IntVar()
    minute_var = tk.IntVar()
    am_pm_var = tk.StringVar(value="AM")

    hour_label = ttk.Label(frame, text="Hour:")
    hour_label.grid(row=0, column=0, padx=5)

    hour_combobox = ttk.Combobox(frame, values=list(range(1, 13)), textvariable=hour_var, width=2)
    hour_combobox.grid(row=0, column=1)

    minute_label = ttk.Label(frame, text="Minute:")
    minute_label.grid(row=0, column=2, padx=5)

    minute_combobox = ttk.Combobox(frame, values=list(range(60)), textvariable=minute_var, width=2)
    minute_combobox.grid(row=0, column=3)

    am_pm_combobox = ttk.Combobox(frame, values=["AM", "PM"], textvariable=am_pm_var, width=3)
    am_pm_combobox.grid(row=0, column=4)

    set_button = ttk.Button(frame, text="Set Alarm", command=set_alarm)
    set_button.grid(row=0, column=5, padx=10)

    alarms_frame = ttk.Frame(root)
    alarms_frame.pack(pady=20)

    # Schedule the check_alarms() function to run after 1 second
    root.after(1000, check_alarms, root)

    root.mainloop()

if __name__ == "__main__":
    main()