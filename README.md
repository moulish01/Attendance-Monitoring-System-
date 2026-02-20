
---

# 📸 OCR-Based Attendance Management System

A **Camera-Based Automated Attendance System** built using **Python, OpenCV, EasyOCR, Tkinter, and MySQL**.
This system captures roll numbers using a webcam and automatically marks attendance in a database.

---

## 🚀 Features

* 🔐 Admin Login Authentication
* ➕ Add New Students
* 📷 Real-Time Camera Attendance Marking
* 🧠 OCR-Based Roll Number Detection (EasyOCR)
* 🗃️ MySQL Database Integration
* 📊 View Attendance Records in GUI
* ⏱️ Automatic Duplicate Prevention (1-hour restriction)

---

## 🛠️ Technologies Used

* **Python**
* **OpenCV** – Camera & Image Processing
* **EasyOCR** – Text Recognition
* **Tkinter** – GUI Interface
* **MySQL** – Database
* **dotenv** – Environment Variable Management

---

## 📂 Project Structure

```
attendance-system/
│
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## 🗄️ Database Setup

Create the following tables in MySQL:

### 1️⃣ Students Table

```sql
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(50) UNIQUE,
    name VARCHAR(100)
);
```

### 2️⃣ Attendance Table

```sql
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    date DATE,
    status VARCHAR(20),
    roll_number VARCHAR(50),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
```

---

## ⚙️ Environment Variables Setup

Create a `.env` file in the project root:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=attendance_db
```

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/attendance-system.git
cd attendance-system
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install opencv-python easyocr mysql-connector-python python-dotenv pandas
```

---

## ▶️ Run the Application

```bash
python main.py
```

---

## 🔑 Default Login Credentials

```
Username: ADMIN
Password: Admin@123
```

⚠️ Change credentials in production for security.

---

## 📸 How It Works

1. Admin logs in.
2. Add student details (Roll Number & Name).
3. Start Camera.
4. System scans roll number using OCR.
5. If student exists → Attendance marked.
6. Prevents duplicate marking within 1 hour.
7. Attendance records can be viewed in GUI.

---

## ⏱️ Time Complexity

* OCR Processing: Depends on frame complexity.
* Database Lookup: O(1) (Indexed search).
* Overall Attendance Marking: Real-time.

---

## 🔒 Security Notes

* Uses environment variables for DB credentials.
* GUI-based restricted admin access.
* Duplicate attendance prevention mechanism implemented.

---

## 📌 Future Enhancements

* Face Recognition Integration
* Excel Export Feature
* Cloud Database Support
* Mobile App Integration
* Role-based Login System
* Attendance Analytics Dashboard

---

## 📄 License

This project is developed for educational and research purposes.

---

## 👨‍💻 Author

Developed by **[Moulishwaran V]**
Feel free to contribute and improve the project!

---


