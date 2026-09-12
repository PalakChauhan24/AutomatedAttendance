import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os


# ============================================================
# FILE PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
FACULTY_FILE = os.path.join(DATA_FOLDER, "faculty.csv")

os.makedirs(DATA_FOLDER, exist_ok=True)


# ============================================================
# CREATE FACULTY FILE IF IT DOES NOT EXIST
# ============================================================

if not os.path.exists(FACULTY_FILE):
    with open(
        FACULTY_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Faculty ID",
            "Name",
            "Email",
            "Department"
        ])


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
ENTRY_COLOR = "#334155"
TEXT_COLOR = "#f8fafc"
MUTED_COLOR = "#94a3b8"
BUTTON_COLOR = "#2563eb"
DELETE_COLOR = "#dc2626"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title("Faculty Management")
root.geometry("900x650")
root.configure(bg=BG_COLOR)
root.resizable(False, False)


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="Faculty Management",
    font=("Segoe UI", 26, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

title.pack(pady=(25, 5))


subtitle = tk.Label(
    root,
    text="Add, update and manage faculty records",
    font=("Segoe UI", 11),
    bg=BG_COLOR,
    fg=MUTED_COLOR
)

subtitle.pack(pady=(0, 20))


# ============================================================
# FORM CARD
# ============================================================

form_card = tk.Frame(
    root,
    bg=CARD_COLOR,
    padx=25,
    pady=20
)

form_card.pack(
    padx=40,
    fill="x"
)


# ============================================================
# VARIABLES
# ============================================================

faculty_id_var = tk.StringVar()
name_var = tk.StringVar()
email_var = tk.StringVar()
department_var = tk.StringVar()


# ============================================================
# FORM LABELS AND ENTRIES
# ============================================================

def create_field(parent, label_text, variable, row):

    label = tk.Label(
        parent,
        text=label_text,
        font=("Segoe UI", 10, "bold"),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )

    label.grid(
        row=row,
        column=0,
        sticky="w",
        padx=(0, 15),
        pady=8
    )

    entry = tk.Entry(
        parent,
        textvariable=variable,
        font=("Segoe UI", 10),
        bg=ENTRY_COLOR,
        fg=TEXT_COLOR,
        insertbackground=TEXT_COLOR,
        relief="flat",
        width=45
    )

    entry.grid(
        row=row,
        column=1,
        sticky="ew",
        pady=8,
        ipady=7
    )

    return entry


create_field(
    form_card,
    "Faculty ID",
    faculty_id_var,
    0
)

create_field(
    form_card,
    "Name",
    name_var,
    1
)

create_field(
    form_card,
    "Email",
    email_var,
    2
)

create_field(
    form_card,
    "Department",
    department_var,
    3
)


# ============================================================
# CLEAR FORM
# ============================================================

def clear_form():

    faculty_id_var.set("")
    name_var.set("")
    email_var.set("")
    department_var.set("")


# ============================================================
# LOAD FACULTY RECORDS
# ============================================================

def load_faculty():

    for item in faculty_table.get_children():
        faculty_table.delete(item)

    if not os.path.exists(FACULTY_FILE):
        return

    try:

        with open(
            FACULTY_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                faculty_table.insert(
                    "",
                    "end",
                    values=(
                        row.get("Faculty ID", ""),
                        row.get("Name", ""),
                        row.get("Email", ""),
                        row.get("Department", "")
                    )
                )

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Could not load faculty records.\n\n{error}"
        )


# ============================================================
# ADD FACULTY
# ============================================================

def add_faculty():

    faculty_id = faculty_id_var.get().strip()
    name = name_var.get().strip()
    email = email_var.get().strip()
    department = department_var.get().strip()

    if not faculty_id:
        messagebox.showwarning(
            "Missing Information",
            "Please enter Faculty ID."
        )
        return

    if not name:
        messagebox.showwarning(
            "Missing Information",
            "Please enter Faculty Name."
        )
        return

    if not email:
        messagebox.showwarning(
            "Missing Information",
            "Please enter Faculty Email."
        )
        return

    if not department:
        messagebox.showwarning(
            "Missing Information",
            "Please enter Department."
        )
        return

    # Check duplicate Faculty ID
    try:

        with open(
            FACULTY_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row.get("Faculty ID") == faculty_id:

                    messagebox.showerror(
                        "Duplicate Faculty ID",
                        "This Faculty ID already exists."
                    )

                    return

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Could not check faculty records.\n\n{error}"
        )

        return

    # Save faculty
    try:

        with open(
            FACULTY_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                faculty_id,
                name,
                email,
                department
            ])

        messagebox.showinfo(
            "Success",
            f"Faculty member {name} added successfully."
        )

        clear_form()
        load_faculty()

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Could not save faculty record.\n\n{error}"
        )


# ============================================================
# DELETE FACULTY
# ============================================================

def delete_faculty():

    selected = faculty_table.selection()

    if not selected:

        messagebox.showwarning(
            "Select Faculty",
            "Please select a faculty record first."
        )

        return

    item = faculty_table.item(
        selected[0]
    )

    faculty_id = item["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete Faculty ID {faculty_id}?"
    )

    if not confirm:
        return

    records = []

    try:

        with open(
            FACULTY_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row.get("Faculty ID") != str(faculty_id):
                    records.append(row)

        with open(
            FACULTY_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "Faculty ID",
                    "Name",
                    "Email",
                    "Department"
                ]
            )

            writer.writeheader()
            writer.writerows(records)

        messagebox.showinfo(
            "Deleted",
            "Faculty record deleted successfully."
        )

        load_faculty()

    except Exception as error:

        messagebox.showerror(
            "Error",
            f"Could not delete faculty record.\n\n{error}"
        )


# ============================================================
# BUTTON FRAME
# ============================================================

button_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

button_frame.pack(
    pady=20
)


add_button = tk.Button(
    button_frame,
    text="ADD FACULTY",
    command=add_faculty,
    font=("Segoe UI", 10, "bold"),
    bg=BUTTON_COLOR,
    fg="white",
    activebackground=BUTTON_COLOR,
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2"
)

add_button.grid(
    row=0,
    column=0,
    padx=8
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_form,
    font=("Segoe UI", 10, "bold"),
    bg=ENTRY_COLOR,
    fg=TEXT_COLOR,
    activebackground=ENTRY_COLOR,
    activeforeground=TEXT_COLOR,
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2"
)

clear_button.grid(
    row=0,
    column=1,
    padx=8
)


delete_button = tk.Button(
    button_frame,
    text="DELETE SELECTED",
    command=delete_faculty,
    font=("Segoe UI", 10, "bold"),
    bg=DELETE_COLOR,
    fg="white",
    activebackground=DELETE_COLOR,
    activeforeground="white",
    relief="flat",
    padx=25,
    pady=10,
    cursor="hand2"
)

delete_button.grid(
    row=0,
    column=2,
    padx=8
)


# ============================================================
# TABLE FRAME
# ============================================================

table_frame = tk.Frame(
    root,
    bg=CARD_COLOR
)

table_frame.pack(
    padx=40,
    pady=(0, 30),
    fill="both",
    expand=True
)


# ============================================================
# TABLE
# ============================================================

columns = (
    "Faculty ID",
    "Name",
    "Email",
    "Department"
)

faculty_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)


for column in columns:

    faculty_table.heading(
        column,
        text=column
    )

    faculty_table.column(
        column,
        anchor="center",
        width=180
    )


faculty_table.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# ============================================================
# TABLE STYLE
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except tk.TclError:
    pass


style.configure(
    "Treeview",
    background=ENTRY_COLOR,
    foreground=TEXT_COLOR,
    fieldbackground=ENTRY_COLOR,
    rowheight=32,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#475569",
    foreground=TEXT_COLOR,
    font=("Segoe UI", 10, "bold")
)

style.map(
    "Treeview",
    background=[
        ("selected", BUTTON_COLOR)
    ],
    foreground=[
        ("selected", "white")
    ]
)


# ============================================================
# LOAD EXISTING RECORDS
# ============================================================

load_faculty()


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()