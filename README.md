✅ README.md
# Flask + PostgreSQL Docker Project

This project is a backend application built using Flask and PostgreSQL.
PostgreSQL runs inside a Docker container, and both services are managed
using Docker Compose.

This project helps me understand backend development, Docker,
and basic DevOps concepts.

---

## 🚀 Tech Stack
- Python (Flask)
- PostgreSQL
- Docker
- Docker Compose
- Postman
- pgAdmin

---

## 📂 Project Structure



docker-project/
│
├── app/
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
│
├── postgrace-db/
│ └── Dockerfile
│
├── docker-compose.yml
├── .gitignore
└── README.md


---

## ⚙️ How to Run the Project

### Prerequisites
- Docker
- Docker Compose

### Run
```bash
docker-compose up


Open browser:

http://127.0.0.1:5000


Expected output:

Flask API is running and connected to PostgreSQL 🚀

📬 API Endpoints
Health
GET /

Students
POST /students
GET /students

Items
POST /items
GET /items
DELETE /items/{id}

🧪 Testing

APIs tested using Postman

Database verified using pgAdmin

🧠 What I Learned

Flask REST APIs

PostgreSQL integration

Dockerizing applications

Docker Compose orchestration

API testing and DB verification

👨‍💻 Author

Shubham


Save.

---

## 🧱 STEP 5 — Final Folder Check (VS Code Explorer)

You should see:


app/
postgrace-db/
docker-compose.yml
.gitignore
README.md


If yes → perfect ✅

---

# 🌐 STEP 6 — PUSH TO GITHUB (VS CODE TERMINAL)

Open **Terminal inside VS Code** and run:

```bash
git init
git add .
git commit -m "Flask PostgreSQL project using Docker Compose"



💻 HOW YOU’LL USE THIS PROJECT ON YOUR OWN LAPTOP

On your laptop, just do:

git clone https://github.com/<your-username>/flask-postgres-docker.git
cd flask-postgres-docker
docker-compose up


Project runs again. No setup headache. ✅