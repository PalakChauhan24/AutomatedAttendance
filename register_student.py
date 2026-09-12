import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import subprocess
import sys


# ==================================================
# PROJECT PATHS
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CSV_FILE = os.path.join(DATA_DIR, "students.csv")

os.makedirs(DATA_DIR, exist_ok=True)


# ==================================================
# CSV HELPERS
# ==================================================

NEW_HEADERS = [
    "ID",
    "Name",
    "Enrollment No",
    "Email",
    "Year",
    "Semester",
    "Section"
]


def prepare_students_csv():
    """
    Keeps old student records safe while upgrading students.csv
    to include Year, Semester and Section.
    """
    if not os.path.exists(CSV_FILE):
        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            csv.writer(file).writerow(NEW_HEADERS)
        return

    try:
        with open(
            CSV_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)
            old_headers = reader.fieldnames or []
            rows = list(reader)

        if all(header in old_headers for header in NEW_HEADERS):
            return

        upgraded_rows = []

        for row in rows:
            upgraded_rows.append([
                row.get("ID", ""),
                row.get("Name", ""),
                row.get("Enrollment No", ""),
                row.get("Email", ""),
                row.get("Year", "Not Specified"),
                row.get("Semester", "Not Specified"),
                row.get("Section", "Not Specified")
            ])

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow(NEW_HEADERS)
            writer.writerows(upgraded_rows)

    except Exception as error:
        messagebox.showerror(
            "CSV Error",
            f"Could not prepare students.csv.\n\n{error}"
        )


prepare_students_csv()


# ==================================================
# REGISTER STUDENT
# ==================================================

def register_student():

    student_id_text = id_entry.get().strip()
    name = name_entry.get().strip()
    enrollment = enrollment_entry.get().strip()
    email = email_entry.get().strip()
    year = year_var.get().strip()
    semester = semester_var.get().strip()
    section = section_var.get().strip()

    # ---------------- CHECK EMPTY FIELDS ----------------

    if not all([
        student_id_text,
        name,
        enrollment,
        email,
        year,
        semester,
        section
    ]):
        messagebox.showwarning(
            "Missing Details",
            "Please fill all student details."
        )
        return

    # ---------------- CHECK STUDENT ID ----------------

    try:
        student_id = int(student_id_text)
    except ValueError:
        messagebox.showerror(
            "Invalid ID",
            "Student ID must be a number."
        )
        return

    # ---------------- CHECK DUPLICATE ID ----------------

    try:
        with open(
            CSV_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                try:
                    if int(row.get("ID", "")) == student_id:
                        messagebox.showerror(
                            "Duplicate ID",
                            "This Student ID is already registered."
                        )
                        return
                except (ValueError, TypeError):
                    continue

    except Exception as error:
        messagebox.showerror(
            "CSV Error",
            f"Could not check student records.\n\n{error}"
        )
        return

    # ---------------- SAVE STUDENT ----------------

    try:
        with open(
            CSV_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                student_id,
                name,
                enrollment,
                email,
                year,
                semester,
                section
            ])

    except Exception as error:
        messagebox.showerror(
            "Save Error",
            f"Could not save student record.\n\n{error}"
        )
        return

    # ---------------- CONFIRM REGISTRATION ----------------

    messagebox.showinfo(
        "Student Registered",
        f"{name} has been registered successfully!\n\n"
        f"Year: {year}\n"
        f"Semester: {semester}\n"
        f"Section: {section}\n\n"
        "The camera will start now."
    )

    # ==================================================
    # FACE CAPTURE
    # ==================================================

    try:
        result = subprocess.run(
            [
                sys.executable,
                os.path.join(BASE_DIR, "capture_faces.py"),
                str(student_id)
            ],
            cwd=BASE_DIR
        )

    except Exception as error:
        messagebox.showerror(
            "Camera Error",
            f"Could not start face capture.\n\n{error}"
        )
        return

    # ==================================================
    # CHECK CAPTURE RESULT
    # ==================================================

    student_folder = os.path.join(
        BASE_DIR,
        "dataset",
        str(student_id)
    )

    image_count = 0

    if os.path.exists(student_folder):
        image_count = len([
            filename
            for filename in os.listdir(student_folder)
            if filename.lower().endswith(
                (".jpg", ".jpeg", ".png")
            )
        ])

    if image_count < 30:
        messagebox.showwarning(
            "Capture Incomplete",
            f"Only {image_count} face images were captured.\n\n"
            "At least 30 images are required."
        )
        return

    # ==================================================
    # AUTOMATIC TRAINING
    # ==================================================

    messagebox.showinfo(
        "Training",
        "Face capture completed successfully!\n\n"
        "Training the face recognition model now..."
    )

    try:
        training_result = subprocess.run(
            [
                sys.executable,
                os.path.join(BASE_DIR, "train.py")
            ],
            cwd=BASE_DIR
        )

        if training_result.returncode == 0:
            messagebox.showinfo(
                "Registration Complete",
                f"{name} has been registered successfully!\n\n"
                "30 face images captured.\n"
                "Face model trained successfully.\n\n"
                "The student is now ready for attendance."
            )
        else:
            messagebox.showerror(
                "Training Failed",
                "Student details were saved, but face model "
                "training failed.\n\n"
                "Please run train.py manually."
            )

    except Exception as error:
        messagebox.showerror(
            "Training Error",
            f"Could not start training.\n\n{error}"
        )

    clear_form()


# ==================================================
# CLEAR FORM
# ==================================================

def clear_form():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    enrollment_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

    year_var.set("")
    semester_var.set("")
    section_var.set("")


# ==================================================
# GUI
# ==================================================

root = tk.Tk()

root.title("Register Student")
root.geometry("560x680")
root.resizable(False, False)
root.configure(bg="#0F172A")


# ==================================================
# TITLE
# ==================================================

tk.Label(
    root,
    text="REGISTER STUDENT",
    font=("Segoe UI", 22, "bold"),
    bg="#0F172A",
    fg="#F8FAFC"
).pack(pady=(25, 5))


tk.Label(
    root,
    text="Add student details and capture face data",
    font=("Segoe UI", 10),
    bg="#0F172A",
    fg="#94A3B8"
).pack(pady=(0, 18))


# ==================================================
# FORM CARD
# ==================================================

card = tk.Frame(
    root,
    bg="#1E293B",
    padx=30,
    pady=22
)

card.pack(
    padx=35,
    fill="x"
)


def add_entry(label_text, row):

    tk.Label(
        card,
        text=label_text,
        font=("Segoe UI", 10, "bold"),
        bg="#1E293B",
        fg="#F8FAFC"
    ).grid(
        row=row,
        column=0,
        sticky="w",
        padx=(0, 15),
        pady=7
    )

    entry = tk.Entry(
        card,
        font=("Segoe UI", 10),
        width=32,
        bg="#334155",
        fg="#F8FAFC",
        insertbackground="#F8FAFC",
        relief="flat"
    )

    entry.grid(
        row=row,
        column=1,
        pady=7,
        ipady=6
    )

    return entry


id_entry = add_entry("Student ID", 0)
name_entry = add_entry("Name", 1)
enrollment_entry = add_entry("Enrollment No", 2)
email_entry = add_entry("Email", 3)


# ==================================================
# ACADEMIC DETAILS
# ==================================================

tk.Label(
    card,
    text="Year",
    font=("Segoe UI", 10, "bold"),
    bg="#1E293B",
    fg="#F8FAFC"
).grid(
    row=4,
    column=0,
    sticky="w",
    padx=(0, 15),
    pady=7
)

year_var = tk.StringVar()

year_box = ttk.Combobox(
    card,
    textvariable=year_var,
    values=("1", "2", "3", "4"),
    state="readonly",
    width=30
)

year_box.grid(
    row=4,
    column=1,
    pady=7,
    ipady=5
)


tk.Label(
    card,
    text="Semester",
    font=("Segoe UI", 10, "bold"),
    bg="#1E293B",
    fg="#F8FAFC"
).grid(
    row=5,
    column=0,
    sticky="w",
    padx=(0, 15),
    pady=7
)

semester_var = tk.StringVar()

semester_box = ttk.Combobox(
    card,
    textvariable=semester_var,
    values=("1", "2", "3", "4", "5", "6", "7", "8"),
    state="readonly",
    width=30
)

semester_box.grid(
    row=5,
    column=1,
    pady=7,
    ipady=5
)


tk.Label(
    card,
    text="Section",
    font=("Segoe UI", 10, "bold"),
    bg="#1E293B",
    fg="#F8FAFC"
).grid(
    row=6,
    column=0,
    sticky="w",
    padx=(0, 15),
    pady=7
)

section_var = tk.StringVar()

section_box = ttk.Combobox(
    card,
    textvariable=section_var,
    values=("A", "B", "C", "D", "E"),
    state="readonly",
    width=30
)

section_box.grid(
    row=6,
    column=1,
    pady=7,
    ipady=5
)


# ==================================================
# BUTTONS
# ==================================================

button_frame = tk.Frame(
    root,
    bg="#0F172A"
)

button_frame.pack(pady=22)


register_button = tk.Button(
    button_frame,
    text="📷  REGISTER & CAPTURE FACE",
    command=register_student,
    font=("Segoe UI", 11, "bold"),
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=12,
    cursor="hand2"
)

register_button.pack(
    side="left",
    padx=7
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_form,
    font=("Segoe UI", 10, "bold"),
    bg="#334155",
    fg="#F8FAFC",
    activebackground="#475569",
    activeforeground="#F8FAFC",
    relief="flat",
    padx=25,
    pady=12,
    cursor="hand2"
)

clear_button.pack(
    side="left",
    padx=7
)


# ==================================================
# INFO
# ==================================================

tk.Label(
    root,
    text="Year • Semester • Section are stored with every student record",
    font=("Segoe UI", 9),
    bg="#0F172A",
    fg="#94A3B8"
).pack()


# ==================================================
# START
# ==================================================

root.mainloop()
