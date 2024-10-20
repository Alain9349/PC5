
import pandas as pd


data = pd.read_csv("/workspaces/PC5/data/youtube.csv", sep='\t')  


print(data.head())

filtered_data = data[['VideoID', 'age', 'category', 'views', 'rate']]

print(filtered_data.head())

categorias_interes = ['Music', 'Comedy'] 
filtered_data = filtered_data[filtered_data['category'].isin(categorias_interes)]

print(filtered_data.head())


### Exportar a MongoDB

from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient('mongodb+srv://handradenato:<db_password>@clustermongodb.bzv3s.mongodb.net/?retryWrites=true&w=majority&appName=ClusterMongoDb')
db = client['sample_mflix']
collection = db['youtube'] 

# Convertir el DataFrame a un diccionario y exportar
data_dict = filtered_data.to_dict("records")
collection.insert_many(data_dict)

print("Datos exportados a MongoDB.")




