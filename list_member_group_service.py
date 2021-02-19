from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

"""
Este script imprime una lista actual de los miembros del grupo empleados@quantil.com.co.
Tambien funciona para crear el token que seguira utilizando el Api Directory.
"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group.member']
# SCOPES = ['https://www.googleapis.com/auth/admin.directory.group']

def members_groups(GROUP):
    """Shows basic usage of the Admin SDK Directory API.
    Prints the names of groups.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    Path_Secre_File = ""
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                Path_Secre_File, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    # Call the Admin SDK Directory API
    # print('Getting the names of members of a groups')
    results = service.members().list(maxResults=50, groupKey = GROUP).execute()
    members = results.get('members', [])
    #El primer miembro es la cabeza del diccionario por lo que no se tiene en cuenta
    #members = members[1:]
    list_id_members = []
    if not members:
        print('No members in the domain.')
    else:
        #print('Groups:')
        for member in members:
            if member['type'] == 'CUSTOMER':
                continue
            else:
                #print(u'{0}, {1}'.format(member['email'], member['id']))
                list_id_members.append(member['email'])
        return list_id_members

if __name__ == '__main__':
    # Grupo: empleados@quantil.com.co >> '03cqmetx3x4zz9pgit'
    mg = members_groups(GROUP='03cqmetx3x4zz9p')
    print(mg)



# Referencias:

# https://developers.google.com/admin-sdk/directory/reference/rest/v1/members/list