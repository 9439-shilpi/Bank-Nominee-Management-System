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

### SQL Procedure
CREATE DATABASE IF NOT EXISTS bank_nominee_db;
USE bank_nominee_db;

DROP TABLE IF EXISTS nominees;

CREATE TABLE nominees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(20),
    relation VARCHAR(50),
    account BIGINT,
    share_percentage VARCHAR(10),
    nominee_type VARCHAR(20)
);

DELIMITER $$

CREATE TRIGGER block_multiple_primary
BEFORE INSERT ON nominees
FOR EACH ROW
BEGIN
    IF NEW.nominee_type = 'Primary' THEN
        IF (SELECT COUNT(*) FROM nominees WHERE nominee_type = 'Primary') >= 1 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Only one Primary nominee allowed';
        END IF;
    END IF;
END$$

DELIMITER ;


## Author

Sunandana Sahoo
Jatin Bhangotra
