
# 📝 Flask Registration Form

A simple user registration system built using **Flask**, **WTForms**, and **SQLite**. This project demonstrates form validation, password hashing, and database integration in a clean, beginner-friendly Flask app.

---

## 🔧 Features

- User registration form with validation
- Password hashing using Flask-Bcrypt
- SQLite database with SQLAlchemy ORM
- Flash messages for feedback
- Bootstrap 5 for clean UI styling

---

## 📂 Project Structure

```markdown

Assignment 11/
├── app/
│   ├── **init**.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   └── templates/
│       ├── base.html
│       ├── register.html
│       └── success.html
├── run.py
├── requirements.txt
└── README.md

````

---

## 🚀 Getting Started

### 1. Clone the Repository


### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python run.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧪 Tech Stack

* Python 3.x
* Flask
* Flask-WTF
* Flask-Bcrypt
* Flask-SQLAlchemy
* SQLite
* Bootstrap 5

---

## 🔐 Security Notes

* Passwords are securely hashed before storing in the database.
* CSRF protection is enabled via `Flask-WTF`.

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Your Name**
GitHub: Ranit Saha([Coderooz])(https://github.com/coderooz)
