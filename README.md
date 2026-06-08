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
USE defaultdb;

CREATE TABLE IF NOT EXISTS nominees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        gender VARCHAR(20),
        relation VARCHAR(100),
        account VARCHAR(100) UNIQUE,
        share_percentage VARCHAR(10),
        nominee_type VARCHAR(50)
    )


Select * From nominees;

mysql> DESCRIBE nominees;
+------------------+--------------+------+-----+---------+----------------+
| Field            | Type         | Null | Key | Default | Extra          |
+------------------+--------------+------+-----+---------+----------------+
| id               | int          | NO   | PRI | NULL    | auto_increment |
| name             | varchar(100) | YES  |     | NULL    |                |
| gender           | varchar(20)  | YES  |     | NULL    |                |
| relation         | varchar(100) | YES  |     | NULL    |                |
| account          | varchar(100) | YES  |     | NULL    |                |
| share_percentage | int          | YES  |     | NULL    |                |
| nominee_type     | varchar(50)  | YES  |     | NULL    |                |
+------------------+------

ALTER TABLE nominees
ADD CONSTRAINT unique_account UNIQUE (account);

DELIMITER $$

CREATE TRIGGER limit_primary
BEFORE INSERT ON nominees
FOR EACH ROW
BEGIN
    IF NEW.nominee_type = 'Primary' THEN
        IF (SELECT COUNT(*) FROM nominees WHERE nominee_type='Primary') >= 1 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Only ONE Primary nominee allowed';
        END IF;
    END IF;
END$$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER limit_secondary
BEFORE INSERT ON nominees
FOR EACH ROW
BEGIN
    IF NEW.nominee_type = 'Secondary' THEN
        IF (SELECT COUNT(*) FROM nominees WHERE nominee_type='Secondary') >= 2 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Only TWO Secondary nominees allowed';
        END IF;
    END IF;
END$$

DELIMITER ;

## Editing table nominee for unique account no.

DROP TABLE IF EXISTS nominees;

CREATE TABLE nominees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    gender VARCHAR(20),
    relation VARCHAR(50),
    account BIGINT UNIQUE,
    share_percentage VARCHAR(10),
    nominee_type VARCHAR(20)
);

## Author

Sunandana Sahoo and 
Jatin Bhangotra.
