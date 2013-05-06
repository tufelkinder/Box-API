from boxapi import api as box

CLIENT_ID = 'xxyyxxyyxxyyxxyy'
CLIENT_SECRET = 'wwwzzzwwwzzzwwwzzz'

# shortcut method to instantiate an authenticated api object
# from a user_profile object that defines at least:
#   access_token,refresh_token,token_type,access_expires

def make_api(user_profile):
    api = box.Api(client_id=CLIENT_ID,
                  client_secret=CLIENT_SECRET,
                  access_token=user_profile.access_token,
                  refresh_token=user_profile.refresh_token,
                  token_type=user_profile.token_type,
                  token_expiration=user_profile.access_expires)
    if api.tokenExpired():
        api.authRefresh()
        auth_info = api.getUserAuthInfo()
        user_profile.access_token = auth_info['access_token']
        user_profile.refresh_token = auth_info['refresh_token']
        user_profile.access_expires = auth_info['token_expiration']
        user_profile.token_type = auth_info['token_type']
        # should redirect to authentication on error
    return api


def getFolders(user_profile,parent_id=0):
    api = make_api(user_profile)
    items = api.getFolderItems(parent_id)
    return items


def getFiles(user_profile,folder_id=0):
    api = make_api(user_profile)
    items = api.getFolderItems(folder_id)
    return items


def createFolder(user_profile,parent_id=0,folder_name):
    api = make_api(user_profile)
    bf = api.createFolder(folder_name,parent_id)
    folder = { "folder_id": bf.id, "folder_name" : bf.name }
    return folder
