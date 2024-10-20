
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv

# Configuración del correo
from_email = 'h.andrade.nato@gmail.com'
to_email = 'alain4546@gmail.com'
subject = 'Archivo CSV adjunto'

# Crear mensaje
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = subject

# Adjuntar el archivo CSV al mensaje
filename = '/workspaces/PC5/mejores_vinos.csv'
attachment = open(filename, 'rb')

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename= {filename}')

msg.attach(part)

# Conexión al servidor SMTP de Gmail
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(from_email, 'fhvp ydgi uhax ryxw')

# Envío del correo
text = msg.as_string()
server.sendmail(from_email, to_email, text)

# Cerrar conexión
server.quit()

print('Correo enviado satisfactoriamente')
