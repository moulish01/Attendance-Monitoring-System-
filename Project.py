import cv2
import easyocr
import mysql.connector as mc
from datetime import date, datetime, timedelta
from tkinter import *
from tkinter import messagebox, ttk
from dotenv import load_dotenv
import os

# ------------------ Load environment variables ------------------
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# ------------------ Connect to MySQL ------------------
db = mc.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = db.cursor(dictionary=True)

# ------------------ Initialize EasyOCR ------------------
reader = easyocr.Reader(['en'])

# ------------------ GUI ------------------
root = Tk()
root.title("Attendance Marker")
root.geometry("900x600")

# ------------------ Login ------------------
def login():
    user = username_entry.get()
    pwd = password_entry.get()
    if user == "ADMIN" and pwd == "Admin@123":
        login_frame.pack_forget()
        main_frame.pack(fill="both", expand=True)
    else:
        messagebox.showerror("Error", "Invalid Credentials")

login_frame = Frame(root)
login_frame.pack(fill="both", expand=True)

Label(login_frame, text="Username").pack(pady=10)
username_entry = Entry(login_frame)
username_entry.pack(pady=5)

Label(login_frame, text="Password").pack(pady=10)
password_entry = Entry(login_frame, show="*")
password_entry.pack(pady=5)

Button(login_frame, text="Login", command=login).pack(pady=20)

# ------------------ Main Frame ------------------
main_frame = Frame(root)

# ------------------ Add Student ------------------
def add_student():
    def save_student():
        roll = roll_entry.get().strip().upper()
        name = name_entry.get().strip()
        if roll == "" or name == "":
            messagebox.showerror("Error", "All fields required")
            return
        cursor.execute("SELECT * FROM students WHERE roll_number=%s", (roll,))
        if cursor.fetchone():
            messagebox.showerror("Error", "Student already exists")
            return
        cursor.execute("INSERT INTO students (roll_number, name) VALUES (%s,%s)", (roll, name))
        db.commit()
        messagebox.showinfo("Success", f"Student {name} added")
        add_win.destroy()
        
    add_win = Toplevel(root)
    add_win.title("Add Student")
    add_win.geometry("300x200")
    Label(add_win, text="Roll Number").pack(pady=5)
    roll_entry = Entry(add_win)
    roll_entry.pack(pady=5)
    Label(add_win, text="Name").pack(pady=5)
    name_entry = Entry(add_win)
    name_entry.pack(pady=5)
    Button(add_win, text="Save", command=save_student).pack(pady=10)

# ------------------ Attendance Tracking ------------------
last_marked = {}  # Track last marking time for each roll number

def start_camera():
    cap = cv2.VideoCapture(0)
    messagebox.showinfo("Info", "Camera started. Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = reader.readtext(frame)
        for (bbox, text, prob) in results:
            roll_number = text.strip().upper()
            if roll_number.isalnum() and prob > 0.5:
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = tuple(map(int, top_left))
                bottom_right = tuple(map(int, bottom_right))
                cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
                cv2.putText(frame, f"Roll No: {roll_number}", 
                            (top_left[0], top_left[1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

                # Mark attendance every hour
                now = datetime.now()
                if roll_number not in last_marked or (now - last_marked[roll_number]) > timedelta(hours=1):
                    cursor.execute("SELECT student_id FROM students WHERE roll_number=%s", (roll_number,))
                    student = cursor.fetchone()
                    if student:
                        today = date.today()
                        cursor.execute("INSERT INTO attendance (student_id, date, status, roll_number) VALUES (%s, %s, %s, %s)",
                                       (student['student_id'], today, 'Present', roll_number))
                        db.commit()
                        last_marked[roll_number] = now

        cv2.putText(frame, "Press 'q' to exit", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.imshow("Attendance Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# ------------------ View Attendance ------------------
def view_attendance():
    for widget in main_frame.winfo_children():
        widget.destroy()
    Label(main_frame, text="Attendance Records", font=("Arial", 16)).pack(pady=10)

    tree = ttk.Treeview(main_frame)
    tree["columns"] = ("id", "student_id", "roll_number", "name", "date", "status")
    tree.heading("id", text="ID")
    tree.heading("student_id", text="Student ID")
    tree.heading("roll_number", text="Roll No")
    tree.heading("name", text="Name")
    tree.heading("date", text="Date")
    tree.heading("status", text="Status")
    tree.pack(fill="both", expand=True)

    cursor.execute("""
        SELECT a.id, a.student_id, a.roll_number, s.name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        ORDER BY a.date DESC
    """)
    records = cursor.fetchall()
    for r in records:
        tree.insert("", "end", values=(r['id'], r['student_id'], r['roll_number'], r['name'], str(r['date']), r['status']))

# ------------------ Buttons ------------------
Button(main_frame, text="Add Student", command=add_student, width=20, height=2).pack(pady=10)
Button(main_frame, text="Start Camera", command=start_camera, width=20, height=2).pack(pady=10)
Button(main_frame, text="View Attendance", command=view_attendance, width=20, height=2).pack(pady=10)

root.mainloop()

# ------------------ Close DB ------------------
cursor.close()
db.close()
