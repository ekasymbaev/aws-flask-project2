Project2 – AWS

Flask + SQLite web application deployed on AWS EC2 using Apache and mod_wsgi.
Users can register, log in, upload Limerick.txt, view word count, and download the file.

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

Open: http://localhost:5000

Quick Test Flow
	1.	Register a new account.
	2.	Fill in profile details.
	3.	Log out and log in again.
	4.	Upload Limerick.txt (or any .txt file).
	5.	Verify the word count appears and download works.


AWS EC2 Quick Deploy
	1.	Launch an EC2 instance (Ubuntu recommended) and open inbound port 5000 in the security group.
	2.	SSH into the instance and install Python + pip.
	3.	Upload or clone this project to the instance.
	4.	Run:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

Notes
	•	SQLite database file: users.db
	•	Uploads are stored in uploads/
	•	Change the SECRET_KEY environment variable for production use