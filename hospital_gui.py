import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import datetime

# ================== DATABASE ==================
conn = sqlite3.connect('hospital_gui.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    disease TEXT,
    admission_date TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXTt
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    date TEXT,
    time TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
)
''')

conn.commit()

# ================== MAIN APP ==================
root = tk.Tk()
root.title("🏥 Hospital Management System")
root.geometry("800x500")
root.config(bg="#f0f4f7")

# ================== HELPER FUNCTIONS ==================
def clear_entries():
    for entry in entries.values():
        entry.delete(0, tk.END)

def refresh_tree(tree, query, cols):
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

# ================== PATIENT FUNCTIONS ==================
def add_patient():
    name = entries['name'].get()
    age = entries['age'].get()
    gender = entries['gender'].get()
    disease = entries['disease'].get()
    date = datetime.date.today()
    if name and age and gender and disease:
        cursor.execute('INSERT INTO patients (name, age, gender, disease, admission_date) VALUES (?, ?, ?, ?, ?)',
                       (name, age, gender, disease, date))
        conn.commit()
        messagebox.showinfo("Success", "Patient added successfully!")
        clear_entries()
        refresh_tree(patient_tree, "SELECT * FROM patients", patient_cols)
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

def delete_patient():
    selected = patient_tree.focus()
    if not selected:
        messagebox.showwarning("Error", "Please select a record to delete.")
        return
    patient_id = patient_tree.item(selected)['values'][0]
    cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
    conn.commit()
    refresh_tree(patient_tree, "SELECT * FROM patients", patient_cols)
    messagebox.showinfo("Deleted", "Patient record deleted successfully!") 

# ================== DOCTOR FUNCTIONS ==================
def add_doctor():
    name = entries['doctor_name'].get()
    specialization = entries['specialization'].get()
    if name and specialization:
        cursor.execute('INSERT INTO doctors (name, specialization) VALUES (?, ?)', (name, specialization))
        conn.commit()
        messagebox.showinfo("Success", "Doctor added successfully!")
        clear_entries()
        refresh_tree(doctor_tree, "SELECT * FROM doctors", doctor_cols)
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

# ================== APPOINTMENT FUNCTIONS ==================
def schedule_appointment():
    pid = entries['patient_id'].get()
    did = entries['doctor_id'].get()
    date = entries['date'].get()
    time = entries['time'].get()
    if pid and did and date and time:
        cursor.execute('INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (?, ?, ?, ?)',
                       (pid, did, date, time))
        conn.commit()
        messagebox.showinfo("Success", "Appointment scheduled successfully!")
        clear_entries()
        refresh_tree(appointment_tree, "SELECT * FROM appointments", appointment_cols)
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

# ================== TABS ==================
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", pady=10)

# ---------- PATIENT TAB ----------
patient_tab = ttk.Frame(notebook)
notebook.add(patient_tab, text="Patients")

entries = {}

tk.Label(patient_tab, text="Name:").grid(row=0, column=0, padx=5, pady=5)
entries['name'] = tk.Entry(patient_tab)
entries['name'].grid(row=0, column=1, padx=5, pady=5)

tk.Label(patient_tab, text="Age:").grid(row=1, column=0)
entries['age'] = tk.Entry(patient_tab)
entries['age'].grid(row=1, column=1)

tk.Label(patient_tab, text="Gender:").grid(row=2, column=0)
entries['gender'] = tk.Entry(patient_tab)
entries['gender'].grid(row=2, column=1)

tk.Label(patient_tab, text="Disease:").grid(row=3, column=0)
entries['disease'] = tk.Entry(patient_tab)
entries['disease'].grid(row=3, column=1)

tk.Button(patient_tab, text="Add Patient", bg="#28a745", fg="white", command=add_patient).grid(row=4, column=0, pady=5)
tk.Button(patient_tab, text="Delete Patient", bg="#dc3545", fg="white", command=delete_patient).grid(row=4, column=1)

patient_cols = ("ID", "Name", "Age", "Gender", "Disease", "Admission Date")
patient_tree = ttk.Treeview(patient_tab, columns=patient_cols, show="headings", height=10)
for col in patient_cols:
    patient_tree.heading(col, text=col)
    patient_tree.column(col, width=100)
patient_tree.grid(row=5, column=0, columnspan=3, pady=10)
refresh_tree(patient_tree, "SELECT * FROM patients", patient_cols)

# ---------- DOCTOR TAB ----------
doctor_tab = ttk.Frame(notebook)
notebook.add(doctor_tab, text="Doctors")

tk.Label(doctor_tab, text="Doctor Name:").grid(row=0, column=0, padx=5, pady=5)
entries['doctor_name'] = tk.Entry(doctor_tab)
entries['doctor_name'].grid(row=0, column=1)

tk.Label(doctor_tab, text="Specialization:").grid(row=1, column=0)
entries['specialization'] = tk.Entry(doctor_tab)
entries['specialization'].grid(row=1, column=1)

tk.Button(doctor_tab, text="Add Doctor", bg="#007bff", fg="white", command=add_doctor).grid(row=2, column=0, pady=5)

doctor_cols = ("ID", "Name", "Specialization")
doctor_tree = ttk.Treeview(doctor_tab, columns=doctor_cols, show="headings", height=10)
for col in doctor_cols:
    doctor_tree.heading(col, text=col)
    doctor_tree.column(col, width=150)
doctor_tree.grid(row=3, column=0, columnspan=3, pady=10)
refresh_tree(doctor_tree, "SELECT * FROM doctors", doctor_cols)

# ---------- APPOINTMENT TAB ----------
appointment_tab = ttk.Frame(notebook)
notebook.add(appointment_tab, text="Appointments")

tk.Label(appointment_tab, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5)
entries['patient_id'] = tk.Entry(appointment_tab)
entries['patient_id'].grid(row=0, column=1)

tk.Label(appointment_tab, text="Doctor ID:").grid(row=1, column=0)
entries['doctor_id'] = tk.Entry(appointment_tab)
entries['doctor_id'].grid(row=1, column=1)

tk.Label(appointment_tab, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
entries['date'] = tk.Entry(appointment_tab)
entries['date'].grid(row=2, column=1)

tk.Label(appointment_tab, text="Time (HH:MM):").grid(row=3, column=0)
entries['time'] = tk.Entry(appointment_tab)
entries['time'].grid(row=3, column=1)

tk.Button(appointment_tab, text="Schedule Appointment", bg="#17a2b8", fg="white", command=schedule_appointment).grid(row=4, column=0, pady=5)

appointment_cols = ("ID", "Patient ID", "Doctor ID", "Date", "Time")
appointment_tree = ttk.Treeview(appointment_tab, columns=appointment_cols, show="headings", height=10)
for col in appointment_cols:
    appointment_tree.heading(col, text=col)
    appointment_tree.column(col, width=100)
appointment_tree.grid(row=5, column=0, columnspan=3, pady=10)
refresh_tree(appointment_tree, "SELECT * FROM appointments", appointment_cols)

# ================== RUN APP ==================
root.mainloop()
