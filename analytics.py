import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from datetime import datetime, timedelta
import holidays


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "students.csv"
)

ATTENDANCE_DIR = os.path.join(
    BASE_DIR,
    "attendance"
)


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
TEXT_COLOR = "#f8fafc"
SECONDARY_TEXT = "#94a3b8"
ACCENT_COLOR = "#38bdf8"
SUCCESS_COLOR = "#22c55e"
DANGER_COLOR = "#ef4444"
BORDER_COLOR = "#334155"


# ============================================================
# LOAD STUDENTS
# ============================================================

def load_students():

    if not os.path.exists(DATA_FILE):

        return pd.DataFrame(
            columns=[
                "ID",
                "Name",
                "Enrollment No",
                "Email"
            ]
        )

    try:

        df = pd.read_csv(
            DATA_FILE
        )

        required_columns = [
            "ID",
            "Name",
            "Enrollment No",
            "Email"
        ]

        for column in required_columns:

            if column not in df.columns:

                df[column] = ""

        return df

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"Could not load students.csv\n\n{e}"
        )

        return pd.DataFrame(
            columns=[
                "ID",
                "Name",
                "Enrollment No",
                "Email"
            ]
        )


# ============================================================
# GET ATTENDANCE FILES
# ============================================================

def get_attendance_files():

    if not os.path.exists(
        ATTENDANCE_DIR
    ):

        return []

    files = []

    for filename in os.listdir(
        ATTENDANCE_DIR
    ):

        if (
            filename.startswith("attendance_")
            and filename.endswith(".csv")
        ):

            files.append(
                os.path.join(
                    ATTENDANCE_DIR,
                    filename
                )
            )

    files.sort()

    return files


# ============================================================
# GET DATE FROM FILE NAME
# ============================================================

def get_date_from_filename(
    filepath
):

    filename = os.path.basename(
        filepath
    )

    try:

        date_text = (
            filename
            .replace(
                "attendance_",
                ""
            )
            .replace(
                ".csv",
                ""
            )
        )

        return datetime.strptime(
            date_text,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        return None


# ============================================================
# CHECK WORKING DAY
# ============================================================

def is_working_day(
    date
):

    # Saturday and Sunday
    if date.weekday() >= 5:

        return False

    try:

        indian_holidays = (
            holidays.country_holidays(
                "IN",
                years=[date.year]
            )
        )

    except AttributeError:

        # Compatibility with older holidays versions
        indian_holidays = holidays.India(
            years=[date.year]
        )

    if date in indian_holidays:

        return False

    return True


# ============================================================
# CALCULATE WORKING DAYS
# ============================================================

def calculate_working_days(
    attendance_files
):

    dates = []

    for filepath in attendance_files:

        date = get_date_from_filename(
            filepath
        )

        if date is not None:

            dates.append(date)

    if not dates:

        return 0

    start_date = min(
        dates
    )

    end_date = max(
        dates
    )

    working_days = 0

    current_date = start_date

    while current_date <= end_date:

        if is_working_day(
            current_date
        ):

            working_days += 1

        current_date += timedelta(
            days=1
        )

    return working_days


# ============================================================
# GET WORKING ATTENDANCE FILES
# ============================================================

def get_working_attendance_files(
    attendance_files
):

    working_files = []

    for filepath in attendance_files:

        date = get_date_from_filename(
            filepath
        )

        if (
            date is not None
            and is_working_day(date)
        ):

            working_files.append(
                filepath
            )

    return working_files


# ============================================================
# GET ATTENDANCE DATA
# ============================================================

def get_attendance_data():

    students_df = load_students()

    attendance_files = (
        get_attendance_files()
    )

    working_days = (
        calculate_working_days(
            attendance_files
        )
    )

    working_files = (
        get_working_attendance_files(
            attendance_files
        )
    )

    present_count = {}

    for _, student in students_df.iterrows():

        student_id = str(
            student["ID"]
        )

        present_count[
            student_id
        ] = 0

    # --------------------------------------------------------
    # COUNT PRESENT DAYS
    # --------------------------------------------------------

    for filepath in working_files:

        try:

            df = pd.read_csv(
                filepath
            )

            if "ID" not in df.columns:

                continue

            for _, row in df.iterrows():

                student_id = str(
                    row["ID"]
                )

                status = str(
                    row.get(
                        "Status",
                        ""
                    )
                ).strip().lower()

                if (
                    status == "present"
                    and student_id in present_count
                ):

                    present_count[
                        student_id
                    ] += 1

        except Exception:

            continue

    return (
        students_df,
        attendance_files,
        working_days,
        present_count
    )


# ============================================================
# CREATE MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Attendance Analytics"
)

root.geometry(
    "1200x760"
)

root.configure(
    bg=BG_COLOR
)

root.minsize(
    1000,
    650
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=BG_COLOR
)

header.pack(
    fill="x",
    padx=30,
    pady=(25, 10)
)


title = tk.Label(
    header,
    text="Attendance Analytics",
    font=(
        "Segoe UI",
        26,
        "bold"
    ),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

title.pack(
    anchor="w"
)


subtitle = tk.Label(
    header,
    text=(
        "Performance overview based on "
        "working days"
    ),
    font=(
        "Segoe UI",
        10
    ),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

subtitle.pack(
    anchor="w",
    pady=(5, 0)
)


# ============================================================
# GET DATA
# ============================================================

students_df, attendance_files, working_days, present_count = (
    get_attendance_data()
)


total_students = len(
    students_df
)


# ============================================================
# CALCULATE PERCENTAGES
# ============================================================

student_percentages = []

for _, student in students_df.iterrows():

    student_id = str(
        student["ID"]
    )

    present = present_count.get(
        student_id,
        0
    )

    if working_days > 0:

        percentage = (
            present / working_days
        ) * 100

    else:

        percentage = 0

    percentage = min(
        percentage,
        100
    )

    student_percentages.append(
        {
            "ID": student_id,
            "Name": str(
                student["Name"]
            ),
            "Present": present,
            "Percentage": percentage
        }
    )


# ============================================================
# OVERALL STATISTICS
# ============================================================

if student_percentages:

    average_attendance = sum(
        student["Percentage"]
        for student in student_percentages
    ) / len(
        student_percentages
    )

else:

    average_attendance = 0


below_75 = sum(
    1
    for student in student_percentages
    if student["Percentage"] < 75
)


# ============================================================
# STAT CARDS
# ============================================================

cards_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

cards_frame.pack(
    fill="x",
    padx=30,
    pady=20
)


def create_stat_card(
    parent,
    title_text,
    value_text
):

    card = tk.Frame(
        parent,
        bg=CARD_COLOR,
        highlightbackground=BORDER_COLOR,
        highlightthickness=1
    )

    card.pack_propagate(
        False
    )

    title_label = tk.Label(
        card,
        text=title_text,
        font=(
            "Segoe UI",
            10
        ),
        bg=CARD_COLOR,
        fg=SECONDARY_TEXT
    )

    title_label.pack(
        anchor="w",
        padx=18,
        pady=(15, 4)
    )

    value_label = tk.Label(
        card,
        text=value_text,
        font=(
            "Segoe UI",
            22,
            "bold"
        ),
        bg=CARD_COLOR,
        fg=TEXT_COLOR
    )

    value_label.pack(
        anchor="w",
        padx=18
    )

    return card


card1 = create_stat_card(
    cards_frame,
    "Students",
    str(total_students)
)

card1.config(
    width=230,
    height=100
)

card1.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 8)
)


card2 = create_stat_card(
    cards_frame,
    "Working Days",
    str(working_days)
)

card2.config(
    width=230,
    height=100
)

card2.pack(
    side="left",
    fill="x",
    expand=True,
    padx=8
)


card3 = create_stat_card(
    cards_frame,
    "Average Attendance",
    f"{average_attendance:.2f}%"
)

card3.config(
    width=230,
    height=100
)

card3.pack(
    side="left",
    fill="x",
    expand=True,
    padx=8
)


card4 = create_stat_card(
    cards_frame,
    "Below 75%",
    str(below_75)
)

card4.config(
    width=230,
    height=100
)

card4.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(8, 0)
)


# ============================================================
# MAIN CONTENT
# ============================================================

content = tk.Frame(
    root,
    bg=BG_COLOR
)

content.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(5, 20)
)


# ============================================================
# LEFT PANEL - BAR CHART
# ============================================================

chart_card = tk.Frame(
    content,
    bg=CARD_COLOR,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

chart_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10)
)


chart_title = tk.Label(
    chart_card,
    text="Attendance Percentage",
    font=(
        "Segoe UI",
        14,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

chart_title.pack(
    anchor="w",
    padx=20,
    pady=(15, 5)
)


chart_subtitle = tk.Label(
    chart_card,
    text=(
        "Percentage of present days "
        "out of working days"
    ),
    font=(
        "Segoe UI",
        9
    ),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT
)

chart_subtitle.pack(
    anchor="w",
    padx=20
)


# ============================================================
# CANVAS
# ============================================================

canvas = tk.Canvas(
    chart_card,
    bg=CARD_COLOR,
    highlightthickness=0
)

canvas.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)


def draw_chart():

    canvas.delete(
        "all"
    )

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    if width <= 1 or height <= 1:

        return

    if not student_percentages:

        canvas.create_text(
            width // 2,
            height // 2,
            text="No attendance data available",
            fill=SECONDARY_TEXT,
            font=(
                "Segoe UI",
                12
            )
        )

        return

    max_students = min(
        len(student_percentages),
        8
    )

    data = student_percentages[
        :max_students
    ]

    left_margin = 130
    right_margin = 40
    top_margin = 30
    bottom_margin = 30

    chart_width = (
        width
        - left_margin
        - right_margin
    )

    chart_height = (
        height
        - top_margin
        - bottom_margin
    )

    # --------------------------------------------------------
    # GRID LINES
    # --------------------------------------------------------

    for percentage in range(
        0,
        101,
        20
    ):

        y = (
            top_margin
            + chart_height
            - (
                percentage / 100
                * chart_height
            )
        )

        canvas.create_line(
            left_margin,
            y,
            width - right_margin,
            y,
            fill=BORDER_COLOR
        )

        canvas.create_text(
            left_margin - 15,
            y,
            text=f"{percentage}%",
            fill=SECONDARY_TEXT,
            font=(
                "Segoe UI",
                8
            ),
            anchor="e"
        )

    # --------------------------------------------------------
    # BARS
    # --------------------------------------------------------

    bar_height = min(
        30,
        max(
            20,
            chart_height
            / max(
                len(data) * 1.5,
                1
            )
        )
    )

    spacing = (
        chart_height
        / max(
            len(data),
            1
        )
    )

    for index, student in enumerate(
        data
    ):

        percentage = student[
            "Percentage"
        ]

        name = student[
            "Name"
        ]

        y_center = (
            top_margin
            + spacing * index
            + spacing / 2
        )

        y1 = (
            y_center
            - bar_height / 2
        )

        y2 = (
            y_center
            + bar_height / 2
        )

        x1 = left_margin

        x2 = (
            left_margin
            + (
                percentage / 100
                * chart_width
            )
        )

        canvas.create_text(
            left_margin - 10,
            y_center,
            text=name,
            fill=TEXT_COLOR,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            anchor="e"
        )

        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=ACCENT_COLOR,
            outline=""
        )

        canvas.create_text(
            min(
                x2 + 8,
                width - 25
            ),
            y_center,
            text=f"{percentage:.1f}%",
            fill=TEXT_COLOR,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            anchor="w"
        )


canvas.bind(
    "<Configure>",
    lambda event: draw_chart()
)


# ============================================================
# RIGHT PANEL
# ============================================================

side_card = tk.Frame(
    content,
    bg=CARD_COLOR,
    width=330,
    highlightbackground=BORDER_COLOR,
    highlightthickness=1
)

side_card.pack(
    side="right",
    fill="y",
    padx=(10, 0)
)

side_card.pack_propagate(
    False
)


# ============================================================
# HIGHEST ATTENDANCE
# ============================================================

highest_title = tk.Label(
    side_card,
    text="Highest Attendance",
    font=(
        "Segoe UI",
        14,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

highest_title.pack(
    anchor="w",
    padx=20,
    pady=(20, 5)
)


if student_percentages:

    highest = max(
        student_percentages,
        key=lambda x: x["Percentage"]
    )

    highest_name = highest[
        "Name"
    ]

    highest_percentage = highest[
        "Percentage"
    ]

else:

    highest_name = "No data"

    highest_percentage = 0


highest_label = tk.Label(
    side_card,
    text=(
        f"{highest_name}\n"
        f"{highest_percentage:.2f}%"
    ),
    font=(
        "Segoe UI",
        18,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=SUCCESS_COLOR,
    justify="left"
)

highest_label.pack(
    anchor="w",
    padx=20,
    pady=(5, 20)
)


# ============================================================
# NEEDS ATTENTION
# ============================================================

attention_title = tk.Label(
    side_card,
    text="Needs Attention",
    font=(
        "Segoe UI",
        14,
        "bold"
    ),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

attention_title.pack(
    anchor="w",
    padx=20,
    pady=(5, 10)
)


low_students = [
    student
    for student in student_percentages
    if student["Percentage"] < 75
]


if low_students:

    for student in low_students:

        frame = tk.Frame(
            side_card,
            bg=CARD_COLOR
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        name_label = tk.Label(
            frame,
            text=student["Name"],
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )

        name_label.pack(
            side="left"
        )

        percentage_label = tk.Label(
            frame,
            text=(
                f"{student['Percentage']:.1f}%"
            ),
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            bg=CARD_COLOR,
            fg=DANGER_COLOR
        )

        percentage_label.pack(
            side="right"
        )

else:

    no_attention = tk.Label(
        side_card,
        text="All students are above 75% 🎉",
        font=(
            "Segoe UI",
            10
        ),
        bg=CARD_COLOR,
        fg=SUCCESS_COLOR
    )

    no_attention.pack(
        anchor="w",
        padx=20,
        pady=5
    )


# ============================================================
# WORKING DAYS NOTE
# ============================================================

note = tk.Label(
    root,
    text=(
        "Working days exclude Saturdays, "
        "Sundays and Indian public holidays."
    ),
    font=(
        "Segoe UI",
        9
    ),
    bg=BG_COLOR,
    fg=SECONDARY_TEXT
)

note.pack(
    anchor="w",
    padx=30,
    pady=(0, 15)
)


# ============================================================
# REFRESH BUTTON
# ============================================================

def refresh():

    root.destroy()

    os.system(
        f'python "{os.path.abspath(__file__)}"'
    )


refresh_button = tk.Button(
    root,
    text="Refresh Analytics",
    command=refresh,
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    bg=ACCENT_COLOR,
    fg="white",
    activebackground="#0ea5e9",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=20,
    pady=9,
    cursor="hand2"
)

refresh_button.pack(
    pady=(0, 15)
)


# ============================================================
# START
# ============================================================

root.after(
    100,
    draw_chart
)

root.mainloop()