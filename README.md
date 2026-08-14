# Smart Attendance System

A professional web-based **Smart Attendance System** built with **Django and Face Recognition** to simplify student attendance management.

## 🚀 Features

* 👤 Student registration and management
* 📷 Face image capture using a camera
* 🧠 Face recognition-based attendance
* ✅ Automatic attendance marking
* 📊 Attendance dashboard
* 📋 Student attendance records
* 📈 Attendance percentage calculation
* 🗓️ Date and time-based attendance records
* 🔐 Login system
* ⚙️ Django Admin panel
* 📱 Responsive web interface for mobile and desktop browsers

## 🛠️ Technologies Used

* **Python**
* **Django**
* **OpenCV**
* **HTML5**
* **Bootstrap 5**
* **SQLite**
* **Git & GitHub**

## 📁 Project Structure

```text
smart_attendance/
│
├── attendance/
│   ├── migrations/
│   ├── haarcascade/
│   ├── dataset/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── capture_faces.py
│   ├── recognize_faces.py
│   └── train_faces.py
│
├── smart_attendance/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── student_list.html
│   ├── edit_student.html
│   ├── attendance_list.html
│   ├── student_attendance.html
│   └── attendance_report.html
│
├── manage.py
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sdongare432-dotcom/smart-attendance-system.git
cd smart-attendance-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install required packages

```bash
pip install django opencv-python
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

Follow the instructions in the terminal.

### 6. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## 📷 Face Recognition Workflow

1. Register a student.
2. Capture face images using the camera.
3. Store the captured face dataset.
4. Train the face recognition model.
5. Start face recognition.
6. Recognized students are marked as present.
7. Attendance is stored in the Django database.
8. Attendance can be viewed through the dashboard and reports.

## 📊 Dashboard

The dashboard provides an overview of:

* Total students
* Students present today
* Students absent today
* Attendance percentage
* Daily attendance information

## 🌐 Mobile & Network Access

The Django development server can be accessed from another device on the same local network by running:

```bash
python manage.py runserver 0.0.0.0:8000
```

Then open the computer's local IP address from a mobile device connected to the same network.

> Note: Local-network access is intended for development/testing. Production deployment requires proper hosting, security configuration, and HTTPS.

## 🔒 Security

For security:

* Do not upload passwords or API keys.
* Do not expose Django `SECRET_KEY` in a public production repository.
* Keep private student/face data out of public repositories.
* Use environment variables for production secrets.
* Configure `DEBUG = False` for production deployment.

## 🔮 Future Enhancements

* Cloud database integration
* Cloud deployment
* Teacher/admin role management
* Email notifications
* Advanced attendance analytics
* PDF/Excel attendance reports
* Improved face recognition accuracy
* Multi-class and multi-department support
* Student profile management
* Production-ready authentication and security

## 👩‍💻 Developer

**Shubhangi Dongare**

B.Sc. Computer Science

## 📄 License

This project is intended for educational, portfolio, and demonstration purposes. Add an appropriate open-source or commercial license before distributing the software to customers.

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
