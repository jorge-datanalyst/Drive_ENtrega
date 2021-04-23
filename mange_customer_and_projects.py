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



def main():
    #Credenciales y parametros para autenticación con API DRIVE 
    Path_Secret_File = "/home/jorgeda/Downloads/Quantil/private/drive_aut.json"
    CLIENT_SECRET_FILE = Path_Secret_File
    SCOPES=["https://www.googleapis.com/auth/drive"]

    flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials=flow.run_console()
    drive=build("drive", "v3", credentials=credentials)

    print('Autenticación valida con Api Drive V3')

    # Encontrar carpeta de proyectos
    def search_drive_id_by_name(name_folder):
        """
        Esta función busca el ID de un Drive o Folder ingresando su nombre,
        Se espera que haya un solo folder con ese nombre, si hay mas de un folder 
        con el mismo nombre se debere ajustar el script
        """

        page_token = None
        flag_while = True
        flag_for = False
        id_project = None

        try:
            while flag_while:
                response = drive.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                    spaces='drive',
                                                    fields='nextPageToken, files(id, name)',
                                                    pageToken=page_token).execute()
                for file in response.get('files', []):
                    # Process change
                    if file.get('name') == name_folder:
                        print('Encontrado')
                        # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                        id_project = file.get('id')

                        flag_while = False
                        flag_for = True
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

            if flag_for == False:
                print('No se encontro Carpeta con ese nombre')
            #print('ID de la carpeta: ',id_project)
            return id_project
        except errors.HttpError as error:
            print('An error occurred:', error)
            return None

    # Se llama la función search_drive_id_by_name para obtener el ID de la carpeta "Proyectos y Trabajos"
    Id_Customer = search_drive_id_by_name(name_folder='Proyectos y Trabajos')
    print('>>: ', Id_Customer)


    # Encontrar hijos de primer grado en un folder
    def find_children_from_parent_drive_id(Id_Customer):
        """
        Esta función recibe el ID de un folder y crea un diccionario con Nombre y ID 
        de todo los folders Hijos de la primera linea o de primer grado
        """
        page_token = None
        dict_folder_projects = {}

        try:
            while True:
                response = drive.files().list(q = "'" + Id_Customer + "' in parents and trashed = false and mimeType='application/vnd.google-apps.folder'", 
                                              pageToken=page_token, 
                                              fields="nextPageToken, files(id, name)").execute()
                #items = results.get('files', [])
                count = 0
                for file in response.get('files', []):
                    #print ('Cliente encontrado: %s' % file.get('name'))
                    dict_folder_projects[file.get('name')] = file.get('id') 
                    count +=1 
                print ('Numero folders in Drive: ',count)
                #print ('>>: ',dict_folder_projects)
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
            return dict_folder_projects
        except errors.HttpError as error:
            print('An error occurred:', error)


    
    f = find_children_from_parent_drive_id(Id_Customer=Id_Customer)
    print('Projectos de Clientes: ', f)


    # Buscar los folders hijos dentro de cada folder Padre 
    def search_project(dict_customer):
        """
        Esta función recibe un diccionario con Nombres e ID de varios folders,
        en este caso de los clientes de Quantil y 
        a cada uno de ellos le extrae los folders hijo que en este caso serian los proyectos de cada cliente. 
        Posteriormente crea un diccionario donde las claves son los diferentes nombres de cada carpeta
        y los valores son los ID de todo los folders con la misma Clave.
        las Claves que deberian estar en cada proyectos son las siguientes;
            -Administración 
            -Directores Generales y Administración 
            -Directores y Administración 
            -Directores y Dirección Administravita
            -Todo Quantil
        Esto se realizo para obtener todo los folder de cada proyecto y verificar que tengan los mismos nombres
        ya que se encontraron varios errores tipograficos como comas al revés, espacios al inicio, en medio de los nombre 
        y/o al finas de los nombres, nombres mal escritos o todo en mayuscula.
        """

        dict_drive = {}
        for key in dict_customer:
            #print(key)
            #print(dict_customer[key])
            dict_projects_customer = find_children_from_parent_drive_id(Id_Customer=dict_customer[key])
            
            for key2 in dict_projects_customer:
                #print(key2)
                #print(dict_projects_customer[key2])
                children2 = find_children_from_parent_drive_id(Id_Customer=dict_projects_customer[key2])
                for key3 in children2:
                    if key3 in dict_drive:
                        print(key3,'ya existe')
                        print('>>: ',type(dict_drive[key3]))
                        if type(dict_drive[key3]) == list:
                            dict_drive[key3].append(children2[key3])
                            
                        else:
                            dict_drive[key3] = []
                            dict_drive[key3].append(children2[key3])
                    else:
                        print(key3, 'Es una nueva clave')
                        dict_drive[key3] = children2[key3]
            print('********************************************************')
        print('Diccionario: ', dict_drive)
        # Se exporta un objeto Pickle para poder utilizar en otro proceso
        pickle.dump(dict_drive, open( "save3.4.pkl", "wb" ) )

        # Se crea un archivo .csv para poder revisar el diccionario creado 
        a_file = open("sample_cambio_nombre_1.4.csv", "w")
        #a_dict = {"a": 1, "b": 2}
        writer = csv.writer(a_file)
        for key, value in dict_drive.items():
            writer.writerow([key, value])

    search_project(dict_customer=f)

if __name__=='__main__':
    main()