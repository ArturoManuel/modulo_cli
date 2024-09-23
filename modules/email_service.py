import smtplib
from email.mime.text import MIMEText

def send_token(email, token):
    sender = "noriegaarturonoriega2@gmail.com"
    msg = MIMEText(f"Tu token de acceso es: {token}")
    msg['Subject'] = "Token de acceso"
    msg['From'] = sender
    msg['To'] = email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, "edks wbje agoo svwx")  # Reemplaza con la contraseña del remitente
            server.sendmail(sender, email, msg.as_string())
        print(f"Token enviado a {email}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
