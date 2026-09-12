# AutomatedAttendance
A desktop-based **Automated Attendance System** built with Python, OpenCV and Tkinter.  
The system uses **Haar Cascade face detection** and **LBPH (Local Binary Patterns Histograms) face recognition** to identify registered students and automatically record their attendance.

---

## ✨ Features

- 👤 Student registration
- 📸 Automatic face-image capture
- 🧠 LBPH face-recognition model training
- 👁️ Real-time face recognition using webcam
- ✅ Automatic attendance marking
- 🚫 Duplicate attendance prevention
- 🎓 Year, Semester and Section management
- 👩‍🏫 Faculty management
- 📊 Attendance analytics
- 📋 Attendance summary and daily records
- 📗 Excel attendance records and report export
- 📧 Automated attendance email notifications
- 🗓️ Working-day calculation excluding weekends and Indian public holidays
- 🌙 Modern dark-themed desktop GUI

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Face detection and recognition |
| Haar Cascade | Face detection |
| LBPH | Face recognition |
| Tkinter | Desktop GUI |
| Pandas | Data handling |
| NumPy | Numerical processing |
| OpenPyXL | Excel workbook management |
| CSV | Student/faculty data storage and compatibility |
| Holidays | Working-day and holiday handling |
| Resend | Email notifications |

---

## 📂 Project Structure

```text
AutomatedAttendance/
│
├── data/
│   ├── students.csv
│   └── faculty.csv
│
├── dataset/
│   ├── 1/
│   ├── 2/
│   └── ...
│
├── trainer/
│   └── trainingData.yml
│
├── attendance/
│   ├── attendance_YYYY-MM-DD.csv
│   ├── attendance_records.xlsx
│   └── attendance_report.xlsx
│
├── haarcascade_frontalface_default.xml
│
├── main.py
├── register_student.py
├── capture_faces.py
├── train.py
├── recognize.py
├── attendance.py
├── view_attendance.py
├── analytics.py
├── faculty_management.py
└── email_notification.py
```

---

## 🧠 How Face Recognition Works

The system follows these main stages:

```text
Webcam
   ↓
Grayscale Conversion
   ↓
Histogram Equalization
   ↓
Median Blur
   ↓
Haar Cascade Face Detection
   ↓
Face Region Extraction
   ↓
Face Resizing (100 × 100)
   ↓
LBPH Recognition
   ↓
Student Identification
   ↓
Multi-frame Confirmation
   ↓
Attendance Marked
```

The LBPH model is trained using grayscale face images resized to **100 × 100 pixels**.

---

## 📸 Student Registration

A student is registered through the desktop interface using:

- Student ID
- Name
- Enrollment Number
- Email
- Year
- Semester
- Section

The system checks for duplicate Student IDs before registration.

After registration, the webcam automatically starts and captures **30 face images** for the student.

The captured images are stored inside:

```text
dataset/<student_id>/
```

---

## 🧠 Training the Face Recognition Model

After capturing the student's face images, the system trains an LBPH face-recognition model.

The trained model is stored as:

```text
trainer/trainingData.yml
```

To manually retrain the model:

```bash
python train.py
```

---

## 👁️ Face Recognition

The recognition module uses the webcam to detect and identify registered students.

The system uses:

- Haar Cascade for face detection
- Histogram equalization for improved contrast
- Median blur for noise reduction
- LBPH for face recognition
- A recognition threshold
- Consecutive-frame confirmation to reduce incorrect recognition

Start recognition with:

```bash
python recognize.py
```

---

## ✅ Attendance Tracking

When a registered student is successfully recognized, the system records:

- Student ID
- Name
- Enrollment Number
- Year
- Semester
- Section
- Date
- Time
- Attendance Status

The system also prevents the same student from being marked multiple times on the same day.

Run attendance tracking using:

```bash
python attendance.py
```

---

## 📗 Attendance Records

The main Excel attendance workbook is:

```text
attendance/attendance_records.xlsx
```

It contains:

### Attendance Records

```text
ID
Name
Enrollment No
Year
Semester
Section
Date
Time
Status
```

### Student Records

```text
ID
Name
Enrollment No
Email
Year
Semester
Section
```

Daily CSV attendance files are also maintained for compatibility and historical records.

---

## 📊 Attendance Analytics

The analytics module provides information such as:

- Total registered students
- Attendance days
- Average attendance
- Students below the attendance threshold
- Highest attendance
- Students requiring attention
- Attendance visualization

The system considers weekends and Indian public holidays while calculating working days.

Run analytics with:

```bash
python analytics.py
```

---

## 📋 Attendance Reports

The attendance-report module provides:

- Attendance Summary
- Daily Attendance Records
- Attendance percentage
- Student academic details
- Excel report export

Run:

```bash
python view_attendance.py
```

The exported report is saved as:

```text
attendance/attendance_report.xlsx
```

---

## 👩‍🏫 Faculty Management

The system includes a dedicated Faculty Management module.

Faculty records include:

- Faculty ID
- Name
- Email
- Department

Run:

```bash
python faculty_management.py
```

---

## 📧 Email Notifications

The system can send automated attendance updates using the **Resend email service**.

The email module uses environment variables for configuration:

```text
RESEND_API_KEY
ATTENDANCE_SENDER_EMAIL
```

### Windows PowerShell

```powershell
$env:RESEND_API_KEY="your_api_key"
$env:ATTENDANCE_SENDER_EMAIL="your_sender_email"
```

> **Security:** Never upload your API key to GitHub. Store credentials in environment variables or another secure configuration method.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/PalakChauhan24/AutomatedAttendance.git
cd AutomatedAttendance
```

> Replace the repository URL if your GitHub repository uses a different name.

### 2. Install Required Libraries

```bash
pip install opencv-python opencv-contrib-python pandas numpy openpyxl pillow holidays resend
```

### 3. Verify the Haar Cascade

Make sure this file exists in the project root:

```text
haarcascade_frontalface_default.xml
```

### 4. Start the Application

```bash
python main.py
```

---

## ▶️ Running the System

The recommended workflow is:

```text
1. Run main.py
       ↓
2. Register a student
       ↓
3. Capture 30 face images
       ↓
4. Train the LBPH model
       ↓
5. Start Attendance
       ↓
6. Student faces the webcam
       ↓
7. Face is recognized
       ↓
8. Attendance is recorded
       ↓
9. View Reports / Analytics
```

---

## 🖥️ Main Dashboard

The desktop dashboard provides access to:

- Face Recognition
- Student Management
- Faculty Management
- Attendance Tracking
- Attendance Reports
- Analytics
- Exit

---

## 📸 Screenshots

Add your project screenshots here after uploading them to GitHub.

### Main Dashboard

```text
![Main Dashboard](screenshots/dashboard.png)
```

### Student Registration

```text
![Student Registration](screenshots/register_student.png)
```

### Face Recognition

```text
![Face Recognition](screenshots/face_recognition.png)
```

### Attendance Report

```text
![Attendance Report](screenshots/attendance_report.png)
```

### Analytics

```text
![Analytics](screenshots/analytics.png)
```

---

## 🔐 Data & Security Notes

- Student and faculty information is stored locally.
- Email credentials/API keys should be kept outside the repository.
- Do not commit private credentials to GitHub.
- Consider adding sensitive/local data files to `.gitignore` before publishing the repository.

Example:

```gitignore
__pycache__/
*.pyc
.env
attendance/*.xlsx
attendance/*.csv
```

If you want to keep sample data in your repository, use anonymized sample records instead of real student information.

---

## 🚀 Future Enhancements

Possible future improvements include:

- 🔐 Faculty/admin login
- ✏️ Student record editing
- 🔎 Search and filtering in attendance reports
- 📅 Custom academic-year selection
- 📈 More detailed attendance charts
- 🗄️ Database-based storage
- ☁️ Cloud backup
- 🖥️ Improved multi-camera support
- 📱 Mobile companion application
- 📄 PDF report generation

---

## 🎯 Project Objective

The objective of this project is to automate the traditional attendance process using facial recognition technology, reduce manual work, minimize duplicate attendance entries, and provide useful attendance reports and analytics through an easy-to-use desktop application.

---

## 👩‍💻 Author

**Palak Chauhan**

B.Tech Computer Science

---

## ⭐ Acknowledgement

This project was developed as an academic project to explore:

- Computer Vision
- Face Recognition
- Python Desktop Application Development
- Data Management
- Automated Reporting
- Email Automation

If you find this project useful, consider giving the repository a ⭐ on GitHub!
