import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import datetime
from apiclient import errors
from datetime import datetime
import list_member_group_service



def main():    
    #Credenciales y parametros para autenticación con API DRIVE 
    # Lo cambie de ruta, no se ha provado
    Path_Secret_File = "/home/jorgeda/Downloads/Quantil/private/drive_aut.json"
    CLIENT_SECRET_FILE = Path_Secret_File
    SCOPES=["https://www.googleapis.com/auth/drive"]

    flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials=flow.run_console()
    drive=build("drive", "v3", credentials=credentials)

    print('Autenticación valida con Api Drive V3')

    # Función para encontrar fecha actual, retorna un string de la fecha
    def time_string():
        now = datetime.now()
        y = str(now.year)
        m = str(now.month)
        if int(m) < 10:
            m = '0'+m
        return str(y+m)

    ##########################--PERMISSIONS--################################

    # Asignar acceso de todos los usuarios a un Proyecto (folder)
    def assign_permissions_folder(LIST_PERMISSIONS, ID_FOLDER):
        for j in LIST_PERMISSIONS:
            create_permissions(EMAIL_ADDRESS=j, ID_DRIVE=ID_FOLDER)    

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

    ###################################--END--######################################

    # Encontrar carpeta pde proyectos
    def search_drive():

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
                    if file.get('name') == 'Proyectos y Trabajos':
                        # print('Encontrado')
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
  

    # Función para crear carpetas
    def create_folder(ID_PARENTS, LIST_FOLDER):
        try: 
            for lf in LIST_FOLDER:
                file_name = {
                    'name': lf,
                    'sendNotificationEmail' : 'false',
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents':[ID_PARENTS], # Esta sera la carpeta padre, si se comenta se crearan las carpetas en la unidad principal

                }
                obj = drive.files().create(body=file_name).execute()
                #print('ls: ', type(obj))
                list_metadata.append(obj)

            #print('Id FOlder1: ',l[0]['id'])
            #print('Folders Created!!!')
            return list_metadata
        except errors.HttpError as error:
            print('An error occurred:', error)
            return None

    # Función para dar permisos a carpetas
    def create_permissions(EMAIL_ADDRESS, ID_DRIVE):
        try:
            permission = {'role': 'writer', 
                        'type' : 'group', 
                        'emailAddress': EMAIL_ADDRESS}
            drive.permissions().create(fileId=ID_DRIVE, body=permission, sendNotificationEmail=False).execute()
            return 
        except errors.HttpError as error:
            print('An error occurred:', error)
            return None
    # Adimistra  los permisos de las carpetas dependiendo el nombre y los grupos que pertenescan
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
                

            elif l['name'] == 'Directores Generales y Administrativos' or l['name'] == 'Directores Generales y Administración':
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

            elif l['name'] == 'Administrativos' or l['name'] == 'Administración':
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

            elif l['name'] == 'Todo Quantil':
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
    
    def search_folder(Id_Customer):

        page_token = None
        # flag_while = True
        # flag_for = False
        # id_project = None

        try:
            while True:
                response = drive.files().list(q = "'" + Id_Customer + "' in parents and trashed = false and mimeType='application/vnd.google-apps.folder'", 
                                              pageToken=page_token, 
                                              fields="nextPageToken, files(id, name)").execute()
                #items = results.get('files', [])
                dict_folder = {}
                for file in response.get('files', []):
                    # print('Encontrado')
                    print ('Cliente encontrado: %s' % file.get('name'))
                    dict_folder[file.get('name')] = file.get('id') 
                Project_new = input("¿Para qué cliente quiere crear un nuevo proyecto?, escriba el nombre como aparece en la lista! \n")
                count = 0
                while count < 2:

                    if Project_new in dict_folder:
                        return dict_folder[Project_new]
                    else:
                        print ('No se encontro Cliente con ese nombre')
                        Project_new = input("Por favor escriba nuevamente el nombre como aparece en la lista! \n")
                        count += 1   
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
        except errors.HttpError as error:
            print('An error occurred:', error)
    
    #Lista de carpetas que se crearan
    # list_folder = ['Directores y Administrativos',
    #                'Directores y Dirección Administrativa',
    #                'Directores Generales y Administrativos', 
    #                'Administrativos',
    #                'Todo Quantil']
    list_folder = ["Directores y Administración",
                    "Directores y Dirección Administrativa", 
                    "Directores Generales y Administración",
                    "Administración",
                    "Todo Quantil"]

    #Lista de metadatos de cada carpeta creada
    list_metadata = []
    searchfolder = search_drive()



    if searchfolder != None:
        var_search_folder = search_folder(Id_Customer=searchfolder)
        if var_search_folder != None:
            # Pide como input el nombre del proyecto
            name_project = input("Escriba el nombre del proyecto! \n")
            # Encuentra la fecha actual
            time_string = time_string()
            # AJusta nombre del proyecto adicionandole la fecha 
            name_project = time_string+'-'+name_project
            # Crea una lista con el nombre del proyecto, dado que la funcipon de crear proyeco
            # recibe como para metro una lista
            list_name_project = [str(name_project)]
            # Crea la carpeta del proyecto asignando el nombre construido anteriormente
            var_folder_project = create_folder(ID_PARENTS=var_search_folder, LIST_FOLDER = list_name_project)
            # Crea las carpetas predeterminadas en la lista 'list_folder' dentro del proyecto
            var_folder_project_permissions = create_folder(ID_PARENTS = var_folder_project[0]['id'], LIST_FOLDER=list_folder)
            ####*** Asigna permisos a todo los mienbros del grupo "empleados@quantil.com.co" a la carpeta del proyecto recien creado***###
            # Primero obtenemos una lista de los miembros de empleados@quantil.com.co 
            # @quantil.com.co, 01qoc8b127t2hl9
            # empleados@quantil.com.co, 03cqmetx3x4zz9p 
            list_mem_group = list_member_group_service.members_groups(GROUP = '03cqmetx3x4zz9p') # ID grupo de empleados@quantil.com.co
            # Asigna a la lista anterior de usuarios acceso las carpetas predeterminadas del proyecto
            assign_permissions_folder(LIST_PERMISSIONS=list_mem_group, ID_FOLDER=var_folder_project_permissions[0]['id'])
            # Administra o elimina los permisos a las carpetas del proyecto dependiendo de los grupos de usuarios. 
            manage_permissions(LIST_METADATA=var_folder_project_permissions)
            print("Proceso Finalizado!!!")
        else:
            print('No se encontro Cliente con este Nombre!')
            
    else:
        print('No hay carpeta con el nombre: Proyectos y Trabajos')



if __name__=='__main__':
    main()


# Referencias:

# https://datatofish.com/executable-pyinstaller/