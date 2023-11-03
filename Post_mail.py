from flask import Flask, render_template, request
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

def is_valid_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

@app.route('/')
def contact_form():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if not name or not email or not message:
            return 'Wypełnij wszystkie pola formularza'

        if not is_valid_email(email):
            return 'Nieprawidłowy adres e-mail'

        # Logika wysyłania wiadomości e-mail za pomocą modułu smtplib
        from_email = email
        to_email = "######"
        email_subject = "Nowa wiadomość ze strony"
        email_body = f"Imię: {name}\nE-mail: {email}\nWiadomość: {message}"

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = email_subject
        msg.attach(MIMEText(email_body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(to_email, '######') 
            server.sendmail(from_email, to_email, msg.as_string())
            server.quit()
            return 'Wiadomość e-mail została wysłana pomyślnie'
        except Exception as e:
            return f'Wystąpił błąd podczas wysyłania wiadomości e-mail: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
