import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_token(email, token):
    sender = "noriegaarturonoriega2@gmail.com"
    recipient = email
    subject = "Autenticación - Cloud Resource Controller"

    # Cuerpo del correo en HTML
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                padding: 20px;
                background-color: #ffffff;
                border: 1px solid #eaeaea;
                max-width: 600px;
                margin: 0 auto;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
                text-align: center;
                font-size: 16px;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #777777;
                text-align: center;
            }}
            .token {{
                font-size: 24px;
                font-weight: bold;
                margin: 20px 0;
                background-color: #f1f1f1;
                padding: 10px;
                border-radius: 5px;
                display: inline-block;
                letter-spacing: 2px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Cloud Resource Controller</h1>
            </div>
            <div class="content">
                <p>Hola <strong>Arturo Noriega</strong>,</p>
                <p>Has solicitado autenticación para acceder al sistema de gestión de recursos de la nube.</p>
                <p>Tu token de acceso es el siguiente:</p>
                <div class="token">{token}</div>
                <p>Por favor, introduce este token en el sistema para completar el acceso.</p>
            </div>
            <div class="footer">
                <p>Cloud Resource Controller &copy; 2024</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Crear mensaje multipart
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Añadir cuerpo HTML al mensaje
    part = MIMEText(html, "html")
    msg.attach(part)

    try:
        # Configurar el servidor SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, "edks wbje agoo svwx")  # Reemplaza con la contraseña del remitente
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Token enviado a {email}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
