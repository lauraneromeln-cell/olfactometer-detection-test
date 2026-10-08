import tkinter as tk
from tkinter import ttk, messagebox
import serial
import time
import csv
from datetime import datetime

# ----- COM PORT CONFIGURATION -----
# Adapt to your computer (e.g. 'COM3' on Windows, '/dev/ttyUSB0' or '/dev/ttyACM0' on Linux)
ARDUINO_PORT = 'COM3'

try:
    arduino = serial.Serial(ARDUINO_PORT, 9600, timeout=1)
    time.sleep(2)
except:
    print("Error: Arduino not detected. Demo mode enabled.")
    arduino = None

# Accessible colors (Blue/Orange palette for color-blind users)
COLOR_BG = "#F5F5F7"
COLOR_PRIMARY = "#007AFF"  # Bright blue
COLOR_ACCENT = "#FF9500"   # Orange
COLOR_STOP = "#5856D6"     # Purple

ODOR_NAMES = {"1": "Peppermint", "2": "Rose", "3": "Cinnamon", "4": "Blank (Neutral)"}


def save_result(answer):
    try:
        import os
        last_name = patient_info['last_name'].get().upper()
        first_name = patient_info['first_name'].get().capitalize()
        age = patient_info['age'].get()
        dob = patient_info['dob'].get()
        history = patient_info['history'].get()

        valve_id = valve_var.get()
        odor_name = ODOR_NAMES.get(valve_id, "Unknown")
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")

        # --- ONE FILE PER PATIENT ---
        docs_folder = os.path.join(os.path.expanduser("~"), "Documents")
        file_path = os.path.join(docs_folder, f"Record_{last_name}_{first_name}.csv")

        # Check whether the file already exists to know if the header must be written
        file_exists = os.path.isfile(file_path)

        with open(file_path, mode='a', newline='', encoding='utf-8-sig') as f:
            # Semicolon (;) is used as the column separator (default for Excel with a French locale).
            # Replace with ',' if your Excel uses the English locale.
            writer = csv.writer(f, delimiter=';')

            if not file_exists:
                # IDENTITY BLOCK
                writer.writerow(['DATE AND TIME', 'LAST NAME', 'FIRST NAME', 'DATE OF BIRTH', 'MEDICAL HISTORY'])
                writer.writerow([f"{current_date} {current_time}", last_name, first_name, dob, history])
                writer.writerow([])  # Empty line for readability
                # ANSWER TABLE HEADER
                writer.writerow(['TIME', 'ODOR', 'DETECTED?'])

            # ADD THE ANSWER
            writer.writerow([current_time, odor_name, answer])

        status_label.config(text="DATA SAVED", foreground="green")

    except Exception as e:
        messagebox.showerror("Error", f"Close the patient's Excel file before clicking!\n{e}")


def deliver_with_blank():
    """Delivers the odor, then automatically switches to the blank channel"""
    valve = valve_var.get()
    t_odor = int(odor_duration.get()) * 1000
    t_blank = int(blank_duration.get()) * 1000

    def blank_step():
        if arduino: arduino.write(b"OPEN 4\n")
        status_label.config(text="CLEANING: Blank channel active...", foreground=COLOR_ACCENT)
        root.after(t_blank, stop_valves)

    if arduino: arduino.write(f"OPEN {valve}\n".encode())
    status_label.config(text=f"DELIVERING: {ODOR_NAMES[valve]}", foreground=COLOR_PRIMARY)
    root.after(t_odor, blank_step)


def stop_valves():
    if arduino: arduino.write(b"STOP\n")
    status_label.config(text="System idle", foreground="grey")


# ----- GRAPHICAL INTERFACE -----
root = tk.Tk()
root.title("Medical Olfactometer v4.0")
root.geometry("500x700")
root.configure(bg=COLOR_BG)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), background=COLOR_BG)

# --- PATIENT SECTION ---
frame_patient = ttk.LabelFrame(root, text=" Patient Information ", padding=10)
frame_patient.pack(pady=10, padx=20, fill="x")

fields = [("Last Name", "last_name"), ("First Name", "first_name"), ("Date of Birth", "dob"),
          ("Age", "age"), ("Medical History", "history")]
patient_info = {}

for i, (label, key) in enumerate(fields):
    ttk.Label(frame_patient, text=label).grid(row=i, column=0, sticky="w", pady=2)
    var = tk.StringVar()
    ttk.Entry(frame_patient, textvariable=var).grid(row=i, column=1, sticky="ew", padx=5)
    patient_info[key] = var
frame_patient.columnconfigure(1, weight=1)

# --- TIMING SETTINGS SECTION ---
frame_timing = ttk.LabelFrame(root, text=" Sequence Parameters (seconds) ", padding=10)
frame_timing.pack(pady=5, padx=20, fill="x")

ttk.Label(frame_timing, text="Odor Time:").grid(row=0, column=0)
odor_duration = ttk.Spinbox(frame_timing, from_=1, to=60, width=5); odor_duration.set(5)
odor_duration.grid(row=0, column=1, padx=5)

ttk.Label(frame_timing, text="Blank Time:").grid(row=0, column=2)
blank_duration = ttk.Spinbox(frame_timing, from_=1, to=60, width=5); blank_duration.set(10)
blank_duration.grid(row=0, column=3, padx=5)

# --- ODOR SELECTION ---
ttk.Label(root, text="ODOR SELECTION", style="Header.TLabel").pack(pady=10)
valve_var = tk.StringVar(value="1")
for k, v in ODOR_NAMES.items():
    ttk.Radiobutton(root, text=v, variable=valve_var, value=k).pack(anchor="w", padx=150)

# --- ACTION BUTTONS ---
btn_frame = tk.Frame(root, bg=COLOR_BG)
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="START SEQUENCE", command=deliver_with_blank, bg=COLOR_PRIMARY, fg="white",
          font=("Segoe UI", 10, "bold"), width=20, height=2).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="STOP", command=stop_valves, bg=COLOR_STOP, fg="white",
          font=("Segoe UI", 10, "bold"), width=10, height=2).grid(row=0, column=1, padx=5)

# --- PATIENT ANSWER ---
tk.Label(root, text="Was the odor detected?", font=("Segoe UI", 11, "italic"), bg=COLOR_BG).pack(pady=5)
answer_frame = tk.Frame(root, bg=COLOR_BG)
answer_frame.pack()

# Blue (YES) and Orange (NO): clearly distinct for color-blind users
tk.Button(answer_frame, text="YES", command=lambda: save_result("YES"), bg="#0056b3", fg="white", width=15, height=2).grid(row=0, column=0, padx=10)
tk.Button(answer_frame, text="NO", command=lambda: save_result("NO"), bg="#cc7a00", fg="white", width=15, height=2).grid(row=0, column=1, padx=10)

status_label = ttk.Label(root, text="System ready", foreground="grey")
status_label.pack(side="bottom", pady=10)

root.mainloop()
