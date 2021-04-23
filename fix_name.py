import pandas as pd
import csv
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import datetime
from apiclient import errors
from datetime import datetime
import list_member_group_service
import pandas as pd
import csv
import pickle


#Credenciales y parametros para autenticación con API DRIVE 
Path_Secret_File = "/home/jorgeda/Downloads/Quantil/private/drive_aut.json"
CLIENT_SECRET_FILE = Path_Secret_File
SCOPES=["https://www.googleapis.com/auth/drive"]

flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials=flow.run_console()
drive=build("drive", "v3", credentials=credentials)

print('Autenticación valida con Api Drive V3')


# Función para actualizar metadatos de un Folder
def update_file(drive, file_id, new_title):
    """Esta función la usamos para actulaicar los metadatos de un folder
       en este caso se actualiza en nombre pero se puede actualizar otros atributos
    """
    try:
        # First retrieve the file from the API.
        file = drive.files().get(fileId=file_id).execute()

        print('>>',file)
        # File's new metadata.
        #file['name'] = new_title
        file_metadata = {
            'name': new_title,
        }

        # Send the request to the API.
        updated_file = drive.files().update(
            fileId=file_id,
            body=file_metadata,
            ).execute()
        #return updated_file
        
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None


# Función para obtener los algunos metadatos de un archivo o folder
def get_metadata_file(drive, file_id):
    """

    """
    try:
        # First retrieve the file from the API.
        file = drive.files().get(fileId=file_id).execute()

        print('>>',file)


        return file
        
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None

# Se llama un diccionario dentro de un objeto
# Para este caso el dicionario tiene todo los nombres e id de los folder dentro de cada proyecto
dict_name = pickle.load( open( "save3.3.pkl", "rb" ) )

#print(dict_name)
#print(type(dict_name))


# Función utilizada para actualizar metadatos de folders
def function_drive(object_dict):
    dict_name = object_dict
    for key in dict_name:
        """
        Esta función se uso para tomar un diccionario con Nombres e Id de folders,
        luego hacer algunas actualizaciones a los metadatos de esos folder, en este caso se corrigieron los 
        nombres.
        """
        # print(key)
        # print(type(dict_name[key]))
        # print(dict_name[key])

        if key == "Directores y Dirección Administrativa":
            print(key, 'Esta bien, no se cambia atributos')

        
        elif key == "Directores y Dirección Administrativa ":
            print(key, 'Se debe cambiar porque tiene espacio de mas')
            #print('Esta es la lista a recorrer: ',dict_name[key])
            for i in dict_name[key]:
                update_file(drive=drive, file_id=i, new_title="Directores y Dirección Administrativa")
                #print(type(i))
                #print(i)
                print(i, 'Nombre Cambiado!')


        elif key == "Directores y Direción Administrativa":
            print(key, 'Se debe cambiar porque mal escrito')
            for i in dict_name[key]:
                update_file(drive=drive, file_id=i, new_title="Directores y Dirección Administrativa")
                #print(type(i))
                #print(i)
                print(i, 'Nombre Cambiado!')


# Obtener metadatos de un folder ingresando en ID
#get_metadata_file(drive=drive, file_id="1V4I2ym05SCykdfpD0zyZewfHdx19Yien")

# 
#function_drive(object_dict=dict_name)


# ACtualizar metadatos de una lista de folders pasando los ID
lista_error = ['19RiwFNdcmPMnTYnVPRBwV8M3yNTekyez', '1-IqztqqSo8uiy-iPNbRkq6o6iykSYG9U']

for j in lista_error:
    update_file(drive=drive, file_id=j, new_title="Directores y Dirección Administrativa")


# ACtualizar metadatos de un folder pasando el ID
#update_file(drive=drive, file_id= "1SKNsl30yrbfYAa9MFu9RVHTe4KW4AChA", new_title="Directores y Administración")






# Referencias

# https://developers.google.com/drive/api/v3/folder
# https://developers.google.com/drive/api/v3/reference/files/update
# https://developers.google.com/drive/api/v2/reference/files/update#examples