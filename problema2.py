
import pandas as pd
data = pd.read_csv('/workspaces/PC5/data/winemag-data-130k-v2.csv')

print(data.head())  
print(data.columns)

data.rename(columns={
    'country': 'pais',
    'points': 'puntuacion',
    'price': 'precio',
    'variety': 'variedad'
}, inplace=True)

def continente(pais):
    if pais in ['Argentina', 'Chile', 'Uruguay']:
        return 'América del Sur'
    elif pais in ['France', 'Italy', 'Spain']:
        return 'Europa'
    else:
        return 'Otros'

data['continente'] = data['pais'].apply(continente)

# Clasificar vinos según puntuación
data['clasificacion'] = pd.cut(data['puntuacion'], bins=[0, 80, 90, 100], labels=['Bajo', 'Medio', 'Alto'])

### Generar reportes
mejores_vinos = data.groupby('continente').apply(lambda x: x[x['puntuacion'] == x['puntuacion'].max()])
print(mejores_vinos)

promedio_precio = data.groupby('pais').agg({'precio': 'mean'}).reset_index()
print(promedio_precio)

vinos_caros = data.nlargest(10, 'precio')
print(vinos_caros)

conteo_variedad = data['variedad'].value_counts()
print(conteo_variedad)

### Exportar reportes

# Exportar a CSV
mejores_vinos.to_csv('mejores_vinos.csv', index=False)

# Exportar a Excel
promedio_precio.to_excel('promedio_precio.xlsx', index=False)

# Exportar a SQLite
import sqlite3

conn = sqlite3.connect('vinos.db')
data.to_sql('vinos', conn, if_exists='replace', index=False)

# Exportar a MongoDB (requiere pymongo)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://handradenato:<db_password>@clustermongodb.bzv3s.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMongoDb')
db = client['sample_mflix']
collection = db['vinos']
db.vinos.insert_many(data.to_dict('records'))


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


