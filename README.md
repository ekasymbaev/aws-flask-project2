# Project 2 — AWS

This project is a Flask web application built for a cloud computing assignment.
It allows users to register, store profile information in a SQLite database, log in again, upload a text file (Limerick.txt), calculate the word count, and download the file.
The same code runs locally and on an AWS EC2 instance using Apache and mod_wsgi.
## Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.

### Quick Test Flow

1. Register a new account.
2. Fill in profile details.
3. Log out and log in again.
4. Upload `Limerick.txt` (or any `.txt` file).
5. Verify the word count appears and download works.

## AWS EC2 Quick Deploy

1. Launch an EC2 instance (Ubuntu recommended) and open inbound port `5000` in the security group.
2. SSH into the instance and install Python + pip.
3. Upload or clone this project to the instance.
4. Run:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

5. Visit `http://<EC2_PUBLIC_IP>:5000`.

## Notes

- SQLite database file: `users.db`
- Uploads are stored in `uploads/`
- Change the `SECRET_KEY` environment variable for production use.
