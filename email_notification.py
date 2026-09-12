import csv
import os
from datetime import datetime, timedelta

import holidays
import resend


# ============================================================
# RESEND EMAIL CONFIGURATION
# ============================================================

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
SENDER_EMAIL = os.getenv("ATTENDANCE_SENDER_EMAIL", "")


# ============================================================
# FILE PATHS
# ============================================================

STUDENTS_FILE = "data/students.csv"
ATTENDANCE_FOLDER = "attendance"


# ============================================================
# CONFIGURE RESEND
# ============================================================

if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY


# ============================================================
# LOAD STUDENT DATA
# ============================================================

def load_students():
    students = {}

    if not os.path.exists(STUDENTS_FILE):
        return students

    try:
        with open(
            STUDENTS_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                try:
                    student_id = int(row["ID"])
                except (ValueError, KeyError):
                    continue

                students[student_id] = {
                    "name": row.get("Name", ""),
                    "enrollment": row.get("Enrollment No", ""),
                    "email": row.get("Email", "")
                }

    except (FileNotFoundError, OSError):
        pass

    return students


# ============================================================
# GET ATTENDANCE FILES
# ============================================================

def get_attendance_files():

    if not os.path.exists(ATTENDANCE_FOLDER):
        return []

    files = []

    for filename in os.listdir(ATTENDANCE_FOLDER):

        if (
            filename.startswith("attendance_")
            and filename.endswith(".csv")
        ):
            files.append(filename)

    return sorted(files)


# ============================================================
# GET ATTENDANCE DATES
# ============================================================

def get_attendance_dates():

    dates = []

    for filename in get_attendance_files():

        try:

            date_text = filename.replace(
                "attendance_", ""
            ).replace(
                ".csv", ""
            )

            date_value = datetime.strptime(
                date_text,
                "%Y-%m-%d"
            ).date()

            dates.append(date_value)

        except ValueError:
            continue

    return sorted(dates)


# ============================================================
# CALCULATE WORKING DAYS
# EXCLUDES WEEKENDS + INDIAN HOLIDAYS
# ============================================================

def calculate_working_days(start_date, end_date):

    if start_date is None or end_date is None:
        return 0

    india_holidays = holidays.India()

    current_date = start_date
    working_days = 0

    while current_date <= end_date:

        is_weekend = current_date.weekday() >= 5
        is_holiday = current_date in india_holidays

        if not is_weekend and not is_holiday:
            working_days += 1

        current_date += timedelta(days=1)

    return working_days


# ============================================================
# GET STUDENT ATTENDANCE STATISTICS
# ============================================================

def get_student_attendance_stats(student_id):

    attendance_dates = get_attendance_dates()

    if not attendance_dates:

        return {
            "present_days": 0,
            "working_days": 0,
            "attendance_percentage": 0
        }

    start_date = min(attendance_dates)
    end_date = max(attendance_dates)

    working_days = calculate_working_days(
        start_date,
        end_date
    )

    india_holidays = holidays.India()

    present_days = 0

    for filename in get_attendance_files():

        try:

            date_text = filename.replace(
                "attendance_",
                ""
            ).replace(
                ".csv",
                ""
            )

            attendance_date = datetime.strptime(
                date_text,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            continue

        # Ignore weekends
        if attendance_date.weekday() >= 5:
            continue

        # Ignore Indian public holidays
        if attendance_date in india_holidays:
            continue

        filepath = os.path.join(
            ATTENDANCE_FOLDER,
            filename
        )

        try:

            with open(
                filepath,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    try:
                        row_id = int(row["ID"])
                    except (ValueError, KeyError):
                        continue

                    if row_id == student_id:

                        status = row.get(
                            "Status",
                            ""
                        ).strip().lower()

                        if status == "present":
                            present_days += 1

                        break

        except (FileNotFoundError, OSError):
            continue

    if working_days > 0:

        percentage = (
            present_days / working_days
        ) * 100

    else:
        percentage = 0

    return {
        "present_days": present_days,
        "working_days": working_days,
        "attendance_percentage": percentage
    }


# ============================================================
# CREATE ATTENDANCE EMAIL
# ============================================================

def create_attendance_email(student_id):

    students = load_students()

    if student_id not in students:
        return None

    student = students[student_id]

    stats = get_student_attendance_stats(
        student_id
    )

    name = student["name"]
    enrollment = student["enrollment"]
    email = student["email"]

    percentage = stats["attendance_percentage"]

    subject = "Automated Attendance Update"

    body = f"""
Hello {name},

Your attendance record has been updated successfully.

Student Details
---------------
Name: {name}
Enrollment No: {enrollment}

Attendance Summary
------------------
Present Days: {stats["present_days"]}
Working Days: {stats["working_days"]}
Attendance Percentage: {percentage:.2f}%

This is an automated message from the
Automated Attendance System.

Regards,
Automated Attendance System
"""

    return {
        "email": email,
        "subject": subject,
        "body": body
    }


# ============================================================
# SEND EMAIL USING RESEND
# ============================================================

def send_email(receiver_email, subject, body):

    if not RESEND_API_KEY:

        print(
            "⚠ RESEND_API_KEY is not configured."
        )

        return False

    if not SENDER_EMAIL:

        print(
            "⚠ ATTENDANCE_SENDER_EMAIL is not configured."
        )

        return False

    if not receiver_email:

        print(
            "⚠ Student email address is missing."
        )

        return False

    try:

        params = {
            "from": SENDER_EMAIL,
            "to": [receiver_email],
            "subject": subject,
            "text": body
        }

        response = resend.Emails.send(
            params
        )

        print(
            f"📧 Email sent successfully to "
            f"{receiver_email}"
        )

        print(
            f"Email ID: {response}"
        )

        return True

    except Exception as error:

        print(
            "❌ Email sending failed:"
        )

        print(error)

        return False


# ============================================================
# SEND ATTENDANCE EMAIL TO ONE STUDENT
# ============================================================

def send_student_attendance_email(student_id):

    email_data = create_attendance_email(
        student_id
    )

    if email_data is None:

        print(
            f"⚠ Student ID {student_id} not found."
        )

        return False

    receiver_email = email_data["email"]

    if not receiver_email:

        print(
            f"⚠ No email address found for "
            f"student ID {student_id}."
        )

        return False

    return send_email(
        receiver_email,
        email_data["subject"],
        email_data["body"]
    )


# ============================================================
# SEND EMAILS TO ALL PRESENT STUDENTS
# ============================================================

def send_emails_to_present_students():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    attendance_file = os.path.join(
        ATTENDANCE_FOLDER,
        f"attendance_{today}.csv"
    )

    if not os.path.exists(attendance_file):

        print(
            "⚠ Today's attendance file does "
            "not exist."
        )

        return

    present_students = set()

    try:

        with open(
            attendance_file,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                try:
                    student_id = int(row["ID"])
                except (ValueError, KeyError):
                    continue

                status = row.get(
                    "Status",
                    ""
                ).strip().lower()

                if status == "present":
                    present_students.add(
                        student_id
                    )

    except (FileNotFoundError, OSError):

        print(
            "❌ Could not read today's "
            "attendance file."
        )

        return

    print(
        f"📧 Sending emails to "
        f"{len(present_students)} "
        f"present student(s)..."
    )

    for student_id in present_students:

        send_student_attendance_email(
            student_id
        )


# ============================================================
# SEND TEST EMAIL
# ============================================================

def send_test_email(receiver_email):

    subject = (
        "Automated Attendance System - "
        "Test Email"
    )

    body = """
Hello,

This is a test email from the
Automated Attendance System.

The email notification module is
working correctly.

Regards,
Automated Attendance System
"""

    return send_email(
        receiver_email,
        subject,
        body
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("========================================")
    print("📧 Email Notification Module")
    print("========================================")

    if not RESEND_API_KEY:

        print(
            "⚠ RESEND_API_KEY is not configured."
        )

    else:

        print(
            "✅ Resend API key detected."
        )

    if not SENDER_EMAIL:

        print(
            "⚠ ATTENDANCE_SENDER_EMAIL "
            "is not configured."
        )

    else:

        print(
            "✅ Sender email detected."
        )

    students = load_students()

    print(
        f"Registered students: "
        f"{len(students)}"
    )

    print(
        "Email notification module loaded."
    )

    print("========================================")