import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import datetime
from apiclient import errors
from datetime import datetime
import list_member_group_service

"""
Este ascript asigna todo los usuarios/permisos del grupo empleados@quantil.com.co 
a la carpeta que se asigne en la variable "id_folder"
"""

#Credenciales y parametros para autenticación con API DRIVE 
# Lo cambie de ruta, no se ha provado

Path_Secret_File = "/home/jorgeda/Downloads/Quantil/private/drive_aut.json"
CLIENT_SECRET_FILE = Path_Secret_File
SCOPES=["https://www.googleapis.com/auth/drive"]

flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials=flow.run_console()
drive=build("drive", "v3", credentials=credentials)

print('Autenticación valida con Api Drive V3')

# Función para dar permisos a carpetas
def create_permissions(EMAIL_ADDRESS, ID_DRIVE):
    try:
        permission = {'role': 'writer', 
                    'type' : 'group',
                    'sendNotificationEmail' : 'false',
                    'emailAddress': EMAIL_ADDRESS}
        drive.permissions().create(fileId=ID_DRIVE, body=permission, sendNotificationEmail=False).execute()
        return 
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

# Hace lista con todo los usuarios del grupo empleados@quantil.com.co
# list_mem_group = list_member_group_service.members_groups(GROUP = '03cqmetx3x4zz9p') # ID grupo de empleados@quantil.com.co
list_mem_group = list_member_group_service.members_groups(GROUP = '01qoc8b127t2hl9') # ID grupo de tic@quantil.com.co
# Se debe colocar el ID del drive al que se le quiere asignar los permisos
id_folder = '10iCGeLsqx4IKULt_lLmNpTCqIdTyQAtC' 

# Asignar acceso de todos los usuarios a un Proyecto (folder)
def assign_permissions_folder(LIST_PERMISSIONS, ID_FOLDER):
    for j in LIST_PERMISSIONS:
        create_permissions(EMAIL_ADDRESS=j, ID_DRIVE=ID_FOLDER)



assign_permissions_folder(LIST_PERMISSIONS=list_mem_group, ID_FOLDER=id_folder)
