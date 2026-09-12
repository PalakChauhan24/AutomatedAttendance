import tkinter as tk
from tkinter import messagebox
import os
import csv
import subprocess
import sys
from datetime import datetime


# ============================================================
# PATH SETUP
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STUDENT_FILE = os.path.join(BASE_DIR, "data", "students.csv")
ATTENDANCE_FOLDER = os.path.join(BASE_DIR, "attendance")


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#0f172a"
SIDEBAR_COLOR = "#111827"
CARD_COLOR = "#1e293b"
BUTTON_COLOR = "#2563eb"
BUTTON_HOVER = "#1d4ed8"
TEXT_COLOR = "#f8fafc"
MUTED_COLOR = "#94a3b8"
SUCCESS_COLOR = "#22c55e"
DANGER_COLOR = "#dc2626"
BORDER_COLOR = "#334155"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Automated Attendance System")
root.geometry("1200x720")
root.configure(bg=BG_COLOR)
root.resizable(False, False)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def run_file(filename):
    """
    Opens another Python module from the project folder.
    """

    file_path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(file_path):
        messagebox.showerror(
            "File Not Found",
            f"{filename} was not found in the project folder."
        )
        return

    try:
        subprocess.Popen([sys.executable, file_path])
    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Could not open {filename}.\n\n{error}"
        )


def get_student_count():
    """
    Returns the number of registered students.
    """

    if not os.path.exists(STUDENT_FILE):
        return 0

    try:
        with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return sum(1 for row in reader if row.get("ID", "").strip())

    except Exception:
        return 0


def get_attendance_days():
    """
    Returns the number of attendance files/days.
    """

    if not os.path.exists(ATTENDANCE_FOLDER):
        return 0

    try:
        files = [
            file for file in os.listdir(ATTENDANCE_FOLDER)
            if file.startswith("attendance_") and file.endswith(".csv")
        ]

        return len(files)

    except Exception:
        return 0


def update_statistics():
    """
    Updates dashboard statistics.
    """

    student_count = get_student_count()
    attendance_days = get_attendance_days()

    student_value.config(text=str(student_count))
    days_value.config(text=str(attendance_days))

    root.after(3000, update_statistics)


def exit_application():
    """
    Closes the dashboard.
    """

    confirm = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit the application?"
    )

    if confirm:
        root.destroy()


# ============================================================
# HOVER EFFECT
# ============================================================

def add_hover(button, normal_color, hover_color):
    def on_enter(event):
        button.config(bg=hover_color)

    def on_leave(event):
        button.config(bg=normal_color)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)


# ============================================================
# SIDEBAR BUTTON
# ============================================================

def create_sidebar_button(parent, text, command):

    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=SIDEBAR_COLOR,
        fg=TEXT_COLOR,
        activebackground=BUTTON_COLOR,
        activeforeground=TEXT_COLOR,
        relief="flat",
        anchor="w",
        padx=25,
        cursor="hand2",
        bd=0
    )

    button.pack(fill="x", pady=2)

    add_hover(button, SIDEBAR_COLOR, "#1e293b")

    return button


# ============================================================
# SIDEBAR
# ============================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR_COLOR,
    width=240
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# Logo / title

logo_frame = tk.Frame(
    sidebar,
    bg=SIDEBAR_COLOR
)

logo_frame.pack(
    fill="x",
    pady=(30, 35)
)


logo = tk.Label(
    logo_frame,
    text="AUTOMATED",
    font=("Segoe UI", 18, "bold"),
    bg=SIDEBAR_COLOR,
    fg=TEXT_COLOR
)

logo.pack()


logo2 = tk.Label(
    logo_frame,
    text="ATTENDANCE",
    font=("Segoe UI", 18, "bold"),
    bg=SIDEBAR_COLOR,
    fg=BUTTON_COLOR
)

logo2.pack()


# Sidebar heading

menu_label = tk.Label(
    sidebar,
    text="MAIN MENU",
    font=("Segoe UI", 9, "bold"),
    bg=SIDEBAR_COLOR,
    fg=MUTED_COLOR,
    anchor="w",
    padx=25
)

menu_label.pack(
    fill="x",
    pady=(0, 10)
)


# Sidebar buttons

create_sidebar_button(
    sidebar,
    "Face Recognition",
    lambda: run_file("recognize.py")
)

create_sidebar_button(
    sidebar,
    "Student Management",
    lambda: run_file("register_student.py")
)

create_sidebar_button(
    sidebar,
    "Faculty Management",
    lambda: run_file("faculty_management.py")
)

create_sidebar_button(
    sidebar,
    "Attendance Tracking",
    lambda: run_file("attendance.py")
)

create_sidebar_button(
    sidebar,
    "Attendance Reports",
    lambda: run_file("view_attendance.py")
)

create_sidebar_button(
    sidebar,
    "Analytics",
    lambda: run_file("analytics.py")
)


# Separator

separator = tk.Frame(
    sidebar,
    bg=BORDER_COLOR,
    height=1
)

separator.pack(
    fill="x",
    padx=20,
    pady=25
)


# Exit button

exit_button = tk.Button(
    sidebar,
    text="EXIT",
    command=exit_application,
    font=("Segoe UI", 10, "bold"),
    bg=SIDEBAR_COLOR,
    fg="#f87171",
    activebackground=DANGER_COLOR,
    activeforeground="white",
    relief="flat",
    anchor="w",
    padx=25,
    cursor="hand2",
    bd=0
)

exit_button.pack(
    fill="x",
    pady=2
)

add_hover(
    exit_button,
    SIDEBAR_COLOR,
    "#3f1d1d"
)


# ============================================================
# MAIN CONTENT AREA
# ============================================================

content = tk.Frame(
    root,
    bg=BG_COLOR
)

content.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# TOP HEADER
# ============================================================

header = tk.Frame(
    content,
    bg=BG_COLOR
)

header.pack(
    fill="x",
    padx=40,
    pady=(30, 10)
)


welcome = tk.Label(
    header,
    text="Dashboard",
    font=("Segoe UI", 28, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

welcome.pack(
    anchor="w"
)


subtitle = tk.Label(
    header,
    text="Automated Face Recognition Attendance System",
    font=("Segoe UI", 11),
    bg=BG_COLOR,
    fg=MUTED_COLOR
)

subtitle.pack(
    anchor="w",
    pady=(3, 0)
)


# Current date

date_label = tk.Label(
    header,
    text=datetime.now().strftime("%d %B %Y"),
    font=("Segoe UI", 10, "bold"),
    bg=BG_COLOR,
    fg=MUTED_COLOR
)

date_label.pack(
    anchor="e",
    pady=(0, 5)
)


# ============================================================
# STATISTICS CARDS
# ============================================================

stats_frame = tk.Frame(
    content,
    bg=BG_COLOR
)

stats_frame.pack(
    fill="x",
    padx=40,
    pady=20
)


# Student card

student_card = tk.Frame(
    stats_frame,
    bg=CARD_COLOR,
    width=260,
    height=120
)

student_card.pack(
    side="left",
    padx=(0, 15)
)

student_card.pack_propagate(False)


tk.Label(
    student_card,
    text="REGISTERED STUDENTS",
    font=("Segoe UI", 9, "bold"),
    bg=CARD_COLOR,
    fg=MUTED_COLOR
).pack(
    anchor="w",
    padx=20,
    pady=(18, 3)
)


student_value = tk.Label(
    student_card,
    text=str(get_student_count()),
    font=("Segoe UI", 28, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

student_value.pack(
    anchor="w",
    padx=20
)


# Attendance days card

days_card = tk.Frame(
    stats_frame,
    bg=CARD_COLOR,
    width=260,
    height=120
)

days_card.pack(
    side="left",
    padx=15
)

days_card.pack_propagate(False)


tk.Label(
    days_card,
    text="ATTENDANCE DAYS",
    font=("Segoe UI", 9, "bold"),
    bg=CARD_COLOR,
    fg=MUTED_COLOR
).pack(
    anchor="w",
    padx=20,
    pady=(18, 3)
)


days_value = tk.Label(
    days_card,
    text=str(get_attendance_days()),
    font=("Segoe UI", 28, "bold"),
    bg=CARD_COLOR,
    fg=SUCCESS_COLOR
)

days_value.pack(
    anchor="w",
    padx=20
)


# System status card

status_card = tk.Frame(
    stats_frame,
    bg=CARD_COLOR,
    width=260,
    height=120
)

status_card.pack(
    side="left",
    padx=15
)

status_card.pack_propagate(False)


tk.Label(
    status_card,
    text="SYSTEM STATUS",
    font=("Segoe UI", 9, "bold"),
    bg=CARD_COLOR,
    fg=MUTED_COLOR
).pack(
    anchor="w",
    padx=20,
    pady=(18, 3)
)


status_value = tk.Label(
    status_card,
    text="ONLINE",
    font=("Segoe UI", 20, "bold"),
    bg=CARD_COLOR,
    fg=SUCCESS_COLOR
)

status_value.pack(
    anchor="w",
    padx=20,
    pady=(4, 0)
)


# ============================================================
# QUICK ACTIONS
# ============================================================

actions_label = tk.Label(
    content,
    text="Quick Actions",
    font=("Segoe UI", 16, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

actions_label.pack(
    anchor="w",
    padx=40,
    pady=(15, 10)
)


actions_frame = tk.Frame(
    content,
    bg=BG_COLOR
)

actions_frame.pack(
    padx=40,
    fill="x"
)


# ------------------------------------------------------------
# START ATTENDANCE
# ------------------------------------------------------------

start_button = tk.Button(
    actions_frame,
    text="START ATTENDANCE",
    command=lambda: run_file("attendance.py"),
    font=("Segoe UI", 11, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    width=25,
    height=3
)

start_button.grid(
    row=0,
    column=0,
    padx=(0, 10),
    pady=10
)

add_hover(
    start_button,
    BUTTON_COLOR,
    BUTTON_HOVER
)


# ------------------------------------------------------------
# REGISTER STUDENT
# ------------------------------------------------------------

register_button = tk.Button(
    actions_frame,
    text="REGISTER STUDENT",
    command=lambda: run_file("register_student.py"),
    font=("Segoe UI", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    activebackground="#334155",
    activeforeground=TEXT_COLOR,
    relief="flat",
    cursor="hand2",
    width=25,
    height=3
)

register_button.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)

add_hover(
    register_button,
    CARD_COLOR,
    "#334155"
)


# ------------------------------------------------------------
# FACULTY MANAGEMENT
# ------------------------------------------------------------

faculty_button = tk.Button(
    actions_frame,
    text="FACULTY MANAGEMENT",
    command=lambda: run_file("faculty_management.py"),
    font=("Segoe UI", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    activebackground="#334155",
    activeforeground=TEXT_COLOR,
    relief="flat",
    cursor="hand2",
    width=25,
    height=3
)

faculty_button.grid(
    row=1,
    column=0,
    padx=(0, 10),
    pady=10
)

add_hover(
    faculty_button,
    CARD_COLOR,
    "#334155"
)


# ------------------------------------------------------------
# TRAIN FACE MODEL
# ------------------------------------------------------------

train_button = tk.Button(
    actions_frame,
    text="TRAIN FACE MODEL",
    command=lambda: run_file("train.py"),
    font=("Segoe UI", 11, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    activebackground="#334155",
    activeforeground=TEXT_COLOR,
    relief="flat",
    cursor="hand2",
    width=25,
    height=3
)

train_button.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)

add_hover(
    train_button,
    CARD_COLOR,
    "#334155"
)


# ============================================================
# REPORTS + ANALYTICS
# ============================================================

bottom_frame = tk.Frame(
    content,
    bg=BG_COLOR
)

bottom_frame.pack(
    padx=40,
    pady=(15, 10),
    fill="x"
)


# View attendance button

view_button = tk.Button(
    bottom_frame,
    text="VIEW ATTENDANCE REPORT",
    command=lambda: run_file("view_attendance.py"),
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    activebackground="#334155",
    activeforeground=TEXT_COLOR,
    relief="flat",
    cursor="hand2",
    width=30,
    height=2
)

view_button.pack(
    side="left",
    padx=(0, 10)
)

add_hover(
    view_button,
    CARD_COLOR,
    "#334155"
)


# Analytics button

analytics_button = tk.Button(
    bottom_frame,
    text="VIEW ANALYTICS",
    command=lambda: run_file("analytics.py"),
    font=("Segoe UI", 10, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR,
    activebackground="#334155",
    activeforeground=TEXT_COLOR,
    relief="flat",
    cursor="hand2",
    width=25,
    height=2
)

analytics_button.pack(
    side="left",
    padx=10
)

add_hover(
    analytics_button,
    CARD_COLOR,
    "#334155"
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    content,
    text="Face Recognition • Attendance Tracking • Reports • Analytics • Faculty Management",
    font=("Segoe UI", 9),
    bg=BG_COLOR,
    fg=MUTED_COLOR
)

footer.pack(
    side="bottom",
    pady=15
)


# ============================================================
# LIVE STATISTICS UPDATE
# ============================================================

update_statistics()


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()