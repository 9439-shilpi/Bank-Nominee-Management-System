# Bank-Nominee-Management-System

A Flask-based web application for managing bank nominees.

## Features

- Add Nominee
- View Nominees
- Edit Nominee
- Delete Nominee
- JSON Data Storage
- Flask Backend
- HTML Frontend

## Technologies Used

- Python
- Flask
- HTML
- CSS
- JSON

## Project Structure

Bank-Nominee-Management-System/

├── app.py

├── data.json

├── requirements.txt

├── README.md

├── .gitignore

└── templates/

    ├── index.html
    
    ├── view.html
    
    └── edit.html

## Routes

- `/` → Home Page
- `/add` → Add Nominee
- `/view` → View Nominees
- `/edit/<index>` → Edit Nominee
- `/update/<index>` → Update Nominee
- `/delete/<index>` → Delete Nominee
- `/api/nominees` → JSON API

## How to Run

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python3 app.py
```

### Open Browser

```text
http://127.0.0.1:5004
```

## Author

Sunandana Sahoo
Jatin Bhangotra
