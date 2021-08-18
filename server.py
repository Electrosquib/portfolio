from os import write
from flask import Flask, render_template, request, redirect
import csv
import smtplib, ssl
import time
app = Flask(__name__)

@app.route('/index.html')
@app.route('/')
def works():
    return render_template('/index.html')

# @app.route('/<string:page_name>')
# def html_page(page_name):
#     return render_template(page_name)

port = 465
password = 'Anaklusmos@12'
context = ssl.create_default_context()
sender = 'esquib.code@gmail.com'
receiver = 'electrosquib@gmail.com'

def email():
    with open('database.csv') as file:
        data = file.read()
    message = f"""From: Portfolio Notifications <{sender}>
    To: Levi <{receiver}>
    Subject: New Notification!

    You have a new notification from your site!
    Database Log:


    {data}
    """
    print(message)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email}, {subject}, {message}')

def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data['email']
        name = data['name']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()), email, name, message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        write_to_csv(data)
        email()
        return redirect('/index.html')

'''
Starting Web Server:
1: export FLASK_APP=server.py
2: export FLASK_ENV=development
3: flask run
'''
