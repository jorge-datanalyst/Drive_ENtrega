import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import datetime
from apiclient import errors
import list_member_group_service

"""
Este script permite enlistar todos las carpetas que tienen un nombre definido,
si hay varias carpetas con nombres igual tambien seran idenfiticados.

Luego utiliza esta lista para administrar/eliminar los usuarios que no deben tener permisos
para acceder.

Se utiliza puntualmente para buscar las carpetas internas de los proyectos, 
luego de acuerdo a permisos de los grupos emilina los usuarios que no deben tener acceso
"""


#Credenciales y parametros para autenticación con API DRIVE 
# Lo cambie de ruta, no se ha provado

Path_Secret_File = "/home/jorgeda/Downloads/Quantil/private/drive_aut.json"
CLIENT_SECRET_FILE = Path_Secret_File
SCOPES=["https://www.googleapis.com/auth/drive"]

flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials=flow.run_console()
drive=build("drive", "v3", credentials=credentials)

print('Autenticado valida con Api Drive V3')

# Función para eliminar permisos de carpetas
def delete_permissions(ID_PERMISSIONS, ID_DRIVE):
    """
    ID_PERMISSIONS: Permiso que se eliminara 
                (ID del permiso, este se obtiene por medio del metodo GET del Api Drive)
    ID_DRIVE: ID del Drieve al que se elimina algun permsiso
    """
    try:
        drive.permissions().delete(fileId=ID_DRIVE, permissionId=ID_PERMISSIONS).execute()
        return # print('Permission Delete!!!')
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None
    # Función para listar permisos de carpetas
def list_permissions(ID_DRIVE):
    """
    ID_DRIVE: ID del Drieve que se consultara
    """
    try:
        listper = drive.permissions().list(fileId=ID_DRIVE).execute()
        return listper.get('permissions',[])
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

# Función para obtener permisos de carpetas
def get_permissions(ID_DRIVE, ID_PERMISSIONS):
    """
    ID_PERMISSIONS: Permisos que se consultara 
                (normalmente es un usuario por medio de un email 
                o un grupo de usuarios)
    ID_DRIVE: ID del Drieve que se consultara
    """
    try:
        gt = drive.permissions().get(fileId=ID_DRIVE, permissionId=ID_PERMISSIONS, fields='emailAddress, role').execute()
        #print(gt)
        return gt
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None


# Adimistra  los permisos de las carpetas dependiendo el nombre y los grupos que pertenezcan
# Elimina los usuarios que no deben estar en esas carpetas.
def manage_permissions(LIST_METADATA):
    
    email_group_director_area = 'director.area@quantil.com.co'
    id_email_group_director_area = '02szc72q2xxvuu8'
    member_director_area = list_member_group_service.members_groups(GROUP = id_email_group_director_area)
    # print('member_director_area',member_director_area)

    email_group_administrativo = 'administrativo@quantil.com.co'
    id_email_group_administrativo = '0279ka654kypbv4'
    member_administrativo = list_member_group_service.members_groups(GROUP = id_email_group_administrativo)
    # print('member_administrativo',member_administrativo)            

    email_group_direccion_administrativa = 'direccion.administrativa@quantil.com.co'
    id_email_group_direccion_administrativa = '01tuee744dz97pl'
    member_direccion_administrativa = list_member_group_service.members_groups(GROUP = id_email_group_direccion_administrativa)
    # print('member_direccion_administrativa',member_direccion_administrativa) 
    
    email_group_director_general = 'direccion.administrativa@quantil.com.co'
    id_email_group_director_general = '01baon6m35is19e'
    member_director_general = list_member_group_service.members_groups(GROUP = id_email_group_director_general)
    # print('member_director_general',member_director_general) 

    email_group_empleados = 'empleados@quantil.com.co' 
    id_email_group_empleados = '03cqmetx3x4zz9p'
    member_empleados = list_member_group_service.members_groups(GROUP = id_email_group_empleados)
    # print('member_empleados',member_empleados) 

    for l in LIST_METADATA:
        
        if l['name'] == 'Directores y Administrativos' or l['name'] == 'Directores y Administración':
            # print('Directores y Administrativos')
            iddriv = l['id']
            lp = list_permissions(ID_DRIVE=iddriv)
            for i in lp:
                gp = get_permissions(ID_DRIVE=iddriv, ID_PERMISSIONS=i['id'])
                # print('>>',gp['emailAddress'], gp['role'])
                if gp['emailAddress'] in member_director_area or gp['emailAddress'] in member_administrativo or  gp['role'] == 'owner':
                    continue
                    # print(gp['emailAddress'], 'Si debe tener permisos en esta carpeta')
                else:
                    # print(gp['emailAddress'], 'No debe tener permisos en esta carpeta')
                    delete_permissions(ID_PERMISSIONS=i['id'], ID_DRIVE=iddriv)

        elif l['name'] == 'Directores y Dirección Administrativa':
            # print('Directores y Dirección Administrativa')
            iddriv = l['id']
            lp = list_permissions(ID_DRIVE=iddriv)
            for i in lp:
                gp = get_permissions(ID_DRIVE=iddriv, ID_PERMISSIONS=i['id'])
                # print('>>',gp['emailAddress'], gp['role'])
                if gp['emailAddress'] in member_director_area or gp['emailAddress'] in member_direccion_administrativa or  gp['role'] == 'owner':
                    continue
                    # print(gp['emailAddress'], 'Si debe tener permisos en esta carpeta')
                else:
                    # print(gp['emailAddress'], 'No debe tener permisos en esta carpeta')
                    delete_permissions(ID_PERMISSIONS=i['id'], ID_DRIVE=iddriv)
            

        if l['name'] == 'Directores Generales y Administrativos' or l['name'] == 'Directores Generales y Administración':
            # print('Directores Generales y Administrativos')
            iddriv = l['id']
            lp = list_permissions(ID_DRIVE=iddriv)
            for i in lp:
                gp = get_permissions(ID_DRIVE=iddriv, ID_PERMISSIONS=i['id'])
                # print('>>',gp['emailAddress'], gp['role'])
                if gp['emailAddress'] in member_director_general or gp['emailAddress'] in member_administrativo or  gp['role'] == 'owner':
                    continue
                    # print(gp['emailAddress'], 'Si debe tener permisos en esta carpeta')
                else:
                    # print(gp['emailAddress'], 'No debe tener permisos en esta carpeta')
                    delete_permissions(ID_PERMISSIONS=i['id'], ID_DRIVE=iddriv)

        if l['name'] == 'Administrativos' or l['name'] == 'Administración':
            # print('Administrativos')
            iddriv = l['id']
            lp = list_permissions(ID_DRIVE=iddriv)
            for i in lp:
                gp = get_permissions(ID_DRIVE=iddriv, ID_PERMISSIONS=i['id'])
                # print('>>',gp['emailAddress'], gp['role'])
                if gp['emailAddress'] in member_administrativo or  gp['role'] == 'owner':
                    continue
                    # print(gp['emailAddress'], 'Si debe tener permisos en esta carpeta')
                else:
                    # print(gp['emailAddress'], 'No debe tener permisos en esta carpeta')
                    delete_permissions(ID_PERMISSIONS=i['id'], ID_DRIVE=iddriv)

        if l['name'] == 'Todo Quantil':
            # print('Todo Quantil')
            iddriv = l['id']
            lp = list_permissions(ID_DRIVE=iddriv)
            for i in lp:
                gp = get_permissions(ID_DRIVE=iddriv, ID_PERMISSIONS=i['id'])
                # print('>>',gp['emailAddress'], gp['role'])
                if gp['emailAddress'] in member_empleados or  gp['role'] == 'owner':
                    continue
                    # print(gp['emailAddress'], 'Si debe tener permisos en esta carpeta')
                else:
                    # print(gp['emailAddress'], 'No debe tener permisos en esta carpeta')
                    delete_permissions(ID_PERMISSIONS=i['id'], ID_DRIVE=iddriv)

def search_drive():

    page_token = None
    flag_while = True
    flag_for = False
    list_metadata = []

    try:
        while flag_while:
            response = drive.files().list(q="mimeType='application/vnd.google-apps.folder' and trashed = false and 'me' in owners",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                if file.get('name') == 'Directores y Administrativos' or file.get('name') == 'Directores y Administración':
                    # print('Encontrado')
                    # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                    list_metadata.append(file)

                    #flag_while = False
                    #flag_for = True
                elif file.get('name') == 'Directores y Dirección Administrativa':
                    # print('Encontrado')
                    # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                    list_metadata.append(file)

                elif file.get('name') == 'Directores Generales y Administrativos' or file.get('name') == 'Directores Generales y Administración':
                    # print('Encontrado')
                    # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                    list_metadata.append(file)

                elif file.get('name') == 'Administrativos' or file.get('name') == 'Administración':
                    # print('Encontrado')
                    # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                    list_metadata.append(file)

                elif file.get('name') == 'Todo Quantil':
                    # print('Encontrado')
                    # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                    list_metadata.append(file)

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        return list_metadata
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None



if __name__=='__main__':
    # Enlista las carpetas predefinida de los proyectos para un usuario, 
    # por ejemplo para "gestion.conocimiento@quantil.com.co"
    list_folder_project = search_drive()
    #print('ID de carpetas: ', list_folder_project)

    # Aplica para cada carpeta de la lista enterios los filtros para eliminar permisos a los usuarios que no deban estar.
    manage_permissions(LIST_METADATA=list_folder_project)
    print('Finalizo!!!')




## Referencias 
# https://developers.google.com/drive/api/v2/reference/files/list
# https://developers.google.com/drive/api/v2/search-files
# https://stackoverflow.com/questions/56857760/list-of-files-in-a-google-drive-folder-with-python