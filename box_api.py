# coding=utf-8

'''
Python API for Box.com
'''

__author__ = 'tufelkinder@yahoo.com'
__version__ = '0.0.1'

# Timezone note: This API attempts to handle dates in a timezone aware
# fashion but there are some issues with this.

from datetime import timedelta, datetime
import os
import rfc822
import sys
import tempfile
import textwrap
import time
import requests
import pytz
#utc=pytz.UTC
from django.utils.timezone import utc

try:
  # Python >= 2.6
    import json
except ImportError:
    try:
    # Python < 2.6
        import simplejson as json
    except ImportError:
        try:
        # Google App Engine
            from django.utils import simplejson as json
        except ImportError:
            raise ImportError, "Unable to load a json library"




  

class Api(object):
    '''A python interface for accessing the Box.com API
    Full method list:

    # Folders
    api.getFolderItems(folder_id,offset,limit)
    api.getFolderInfo(folder_id)
    api.createFolder(folder_name,parent_id)
    api.copyFolder(folder_id,parent_id,new_folder_name)
    api.deleteFolder(folder_id)
    # folder_dict is a dictionary or folder object of changed values
    api.updateFolderInfo(folder_dict) 
    # shared_dict contains: access[:open,company,collaborators],
    # unshared_at[timestamp], permissions, can_download, can_preview
    api.createFolderSharedLink(folder_id, shared_dict)
    api.getDiscussions(folder_id)
    # fields_dict: fields you want returned
    api.getTrashList(limit,offset, fields_dict)
    api.getTrashedFolder(folder_id)
    api.restoreTrashedFolder(folder_id,new_name,parent_id)
    api.permDeleteFolder(folder_id)

    # Files
    api.uploadFile(filename,src_file,parent_id,content_created_at,content_modified_at)
    api.uploadFileVersion(self,file_id,original_etag=None, filename, src_file, content_modified_at=None)
    api.downloadFile(file_id,local_filename,version)
    api.getFileInfo(file_id)
    api.getFileVersions(file_id)
    api.updateFileInfo(file_id, fields_dict)
    api.copyFile(file_id,new_parent_id, new_filename)
    api.deleteFile(file_id, etag)
    api.createFileSharedLink(file_id,shared_dict) # see folders, above
    api.getFileComments(file_id)
    api.getFileThumbnail(file_id,min_height,min_width,max_height,max_width)
    api.getTrashedFileInfo(file_id)
    api.restoreTrashedFile(fild_id,new_filename,parent_id)
    api.permDeleteFile(file_id)

    # Comments
    api.addComment(file_id, message)
    api.getCommentInfo(comment_id)
    api.updateComment(comment_id,message)
    api.deleteComment(commend_id)

    # Discussions
    api.createDiscussion(folder_id,name,description)
    api.addDiscussionComment(discussion_id,message)
    api.getDiscussionInfo(discussion_id)
    api.getDiscussionComments(discussion_id)
    api.updateDiscussion(discussion_id,name,description)
    
    # Users
    api.getUserInfo()
    api.getAllUsers(filter_term,limit,offset)
    api.updateUser(user_id,notify,field_dict)
    api.createUser(login,name,field_dict)
    api.moveFolder(destination_user_id,notify,destination_folder_id)
    api.deleteUser(user_id,notify,force)
    api.addUserEmail(user_id,email)
    api.removeUserEmail(user_id,email_alias_id)
    api.changeUserLogin(user_id,login)
    api.getUserEmails(user_id)
    
    # Search
    api.search(query,limit,offset)

    # Shared Items
    api.getSharedItemInfo(shared_link)

    # Events
    api.getUserEvents(stream_position,stream_type,limit)
    api.getEvents(stream_type,limit,offset,event_types,created_after,created_before)
    api.getLongPollURL()
    '''

    BOX_OAUTH = 'Bearer {0}'

    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 access_token=None,
                 refresh_token=None,
                 token_type=None,
                 token_expiration=None,
                 base_url=None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._token_type = token_type or 'bearer'
        self._token_expiration = token_expiration
        self.base_url = base_url or 'https://api.box.com/2.0'
        if not client_id or not client_secret:
#            print >> sys.stderr, 'No can do nothing without not a client_id and a client_secret, yo.'
            raise BoxError('No can do nothing without not a client_id and a client_secret, yo.')

    def getHeaders(self):
        if self.tokenExpired():
            refresh_result = self.authRefresh()
            if refresh_result != True:
                raise BoxError('Authentication token refresh failed.\nError: {0}\nDescription: {1}'.format(refresh_result['error'], refresh_result['error_desc']))
        return { 'Authorization' : self.BOX_OAUTH.format(self._access_token) }


    def tokenExpired(self):
        try:
            return datetime.utcnow().replace(tzinfo=utc) > self._token_expiration
        except:
            return True


    def authRefresh(self):
        url = 'https://api.box.com/oauth2/token'
        data = {
            'refresh_token': self._refresh_token,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'refresh_token'
        }

        response = requests.post(url, data=data)
        auth_info = response.json()
        try:
            error = auth_info['error']
            error_desc = auth_info['error_description']
            return { "error": error, "error_desc": error_desc }
        except:
            self._access_token = auth_info['access_token']
            self._token_expiration = datetime.utcnow().replace(tzinfo=utc) + timedelta(seconds=int(auth_info['expires_in']))
            self._token_type = auth_info['token_type']
            self._refresh_token = auth_info['refresh_token']
        return True


    def getUserAuthInfo(self):
        data = {
            "access_token": self._access_token,
            "token_type": self._token_type,
            "refresh_token": self._refresh_token,
            "token_expiration": self._token_expiration
        }
        return data


    # Folders

    def getFolderItems(self,folder_id,offset=None,limit=None,debug=False):
        headers = self.getHeaders()
        data = {}
        if offset:
            data['offset'] = offset
        if limit:
            data['limit'] = limit
        url = self.base_url + '/folders/{0}/items'.format(folder_id)
        response = requests.get(url,headers=headers,params=data)
        folder_items = response.json()
        try:
            item_count = folder_items['total_count'] 
        except:
            raise BoxError('getFolderItems failed: ' + str(folder_items))
        items = list()
        # convert to a list of mini folder objects
        for item in folder_items['entries']:
            if item['type'] == 'folder':
                fi = BoxFolder(box_type='folder')
                fi.newFromJsonDict(fi,item)
            else:
                fi = BoxFile(box_type='file')
                fi.newFromJsonDict(fi,item)
            items.append(fi)
        if debug:
            return folder_items
        return items


    def getFolderInfo(self,folder_id):
        headers = self.getHeaders()
        url = self.base_url + '/folders/{0}'.format(folder_id)
        response = requests.get(url,headers=headers)
        folder_info = response.json()
        bf = BoxFolder(box_type='folder')
        bf.newFromJsonDict(bf,folder_info)
        return bf


    def createFolder(self,folder_name,parent_id):
        headers = self.getHeaders()
        url = self.base_url + '/folders'
        data = json.dumps({
            "name": folder_name,
            "parent": { "id": parent_id }
        })
        response = requests.post(url,headers=headers,data=data)
        folder_info = response.json()
        bf = BoxFolder(box_type='folder')
        bf.newFromJsonDict(bf,folder_info)
        return bf


    def copyFolder(self,folder_id,dest_parent_id,new_folder_name):
        headers = self.getHeaders()
        url = self.base_url + '/folders/{0}/copy'.format(folder_id)
        data = json.dumps({
            "name": new_folder_name,
            "parent": { "id": dest_parent_id }
        })
        response = requests.post(url,headers=headers,data=data)
        folder_info = response.json()
        bf = BoxFolder(box_type='folder')
        bf.newFromJsonDict(bf,folder_info)
        return bf


    def moveFolder(self,folder_id,dest_parent_id):
        headers = self.getHeaders()
        url = self.base_url + '/folders/{0}'.format(folder_id)
        data = json.dumps({
            "parent": { "id": dest_parent_id }
        })
        response = requests.put(url,headers=headers,data=data)
        folder_info = response.json()
        bf = BoxFolder(box_type='folder')
        bf.newFromJsonDict(bf,folder_info)
        return bf


    def deleteFolder(self,folder_id):
        pass

    # folder_dict is a dictionary or folder object of changed values
    def updateFolderInfo(self,folder_dict):
        pass

    # shared_dict contains: access[:open,company,collaborators],
    # unshared_at[timestamp], permissions, can_download, can_preview
    def createFolderSharedLink(self,folder_id, shared_dict):
        pass

    def getDiscussions(self,folder_id):
        pass

    # fields_dict: fields you want returned
    def getTrashList(self,limit,offset, fields_dict):
        pass

    def getTrashedFolder(self,folder_id):
        pass

    def restoreTrashedFolder(self,folder_id,new_name,parent_id):
        pass

    def permDeleteFolder(self,folder_id):
        pass

    # Files
    def uploadFile(self,filename,src_file,parent_id,content_created_at=None,content_modified_at=None):
        headers = self.getHeaders()
        url = self.base_url + '/files/content'
        files = {'filename': (filename, open(src_file,'rb'))}
        data = json.dumps( {"folder_id": parent_id,} )
        response = requests.post(url, data=data, files=files, headers=headers)
        file_info = response.json()
        # parse folder_info into folder object??
        return file_info


    def uploadFileVersion(self,file_id,filename,src_file,original_etag=None,content_modified_at=None):
        headers = self.getHeaders()
        if original_etag:
            headers['If-Match'] = original_etag
        url = self.base_url + '/files/{0}/content'.format(file_id)
        files = {'filename': (filename, open(src_file,'rb'))}
        data = json.dumps( {"folder_id": parent_id,} )
        response = requests.post(url, data=data, files=files, headers=headers)
        file_info = response.json()
        # parse folder_info into folder object??
        return file_info


    def downloadFile(self,file_id,local_filename,version=None):
        headers = self.getHeaders()
        url = self.base_url + '/files/{0}/content'.format(file_id)
        if version:
            data = json.dumps({ "version": version })
            response = requests.get(url,headers=headers,params=data)
        else:
            response = requests.get(url,headers=headers)

        with open(local_filename, 'wb') as fp:
            fp.write(response.content)
            fp.close()

        return local_filename


    def getFileInfo(self,file_id):
        headers = self.getHeaders()
        url = self.base_url + '/files/{0}'.format(file_id)
        response = requests.get(url,headers=headers)
        file_info = response.json()
        bf = BoxFile(box_type='file')
        bf.newFromJsonDict(bf,file_info)
        return bf


    def getFileVersions(self,file_id):
        pass

    def updateFileInfo(self,file_id, fields_dict):
        pass

    def copyFile(self,file_id,dest_parent_id,new_filename=None):
        headers = self.getHeaders()
        url = self.base_url + '/files/{0}/copy'.format(file_id)
        if new_filename:
            data = json.dumps({
                "name": new_filename,
                "parent": { "id": dest_parent_id }
            })
        else:
            data = json.dumps({
                "parent": { "id": dest_parent_id }
            })
        response = requests.post(url,headers=headers,data=data)
        file_info = response.json()
        bf = BoxFolder(box_type='file')
        bf.newFromJsonDict(bf,file_info)
        return bf


    def deleteFile(self,file_id, etag):
        headers = self.getHeaders()
        if etag:
            headers['If-Match'] = etag
        url = self.base_url + '/files/{0}'.format(file_id)
        response = requests.delete(url,headers=headers)
        # 204 successful
        # 412 Precondition failed / etag didn't match
        return response.status_code

    # see folders, above
    def createFileSharedLink(self,file_id,shared_dict):
        pass

    def getFileComments(self,file_id):
        pass

    def getFileThumbnail(self,file_id,min_height,min_width,max_height,max_width):
        pass

    def getTrashedFileInfo(self,file_id):
        pass

    def restoreTrashedFile(self,file_id,new_filename,parent_id):
        pass

    def permDeleteFile(self,file_id):
        pass


    # Comments
    def addComment(self,file_id, message):
        pass

    def getCommentInfo(self,comment_id):
        pass

    def updateComment(self,comment_id,message):
        pass

    def deleteComment(self,comment_id):
        pass


    # Discussions
    def createDiscussion(self,folder_id,name,description):
        pass

    def addDiscussionComment(self,discussion_id,message):
        pass

    def getDiscussionInfo(self,discussion_id):
        pass

    def getDiscussionComments(self,discussion_id):
        pass

    def updateDiscussion(self,discussion_id,name,description):
        pass

    
    # Users
    def getUserInfo(self):
        headers = self.getHeaders()
        url = self.base_url + '/users/me'
        response = requests.get(url,headers=headers)
        user_info = response.json()
        bu = BoxUser(box_type='user')
        bu.newFromJsonDict(bu,user_info)
        return bu


    def getAllUsers(self,filter_term=None,limit=None,offset=None):
        headers = self.getHeaders()
        url = self.base_url + '/users'
        data = {}
        if filter_term:
            data['filter_term'] = filter_term
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset
        if data:
            response = requests.get(url,headers=headers,params=data)
        else:
            response = requests.get(url,headers=headers)
        users_info = response.json()
        results = list()
        try:
            entries = users_info['entries']
        except:
            return users_info
        for entry in entries:
            bu = BoxUser(box_type='user')
            bu.newFromJsonDict(bu,entry)
            results.append(bu)
        return results


    def updateUser(self,user_id,notify,field_dict):
        pass

    def createUser(self,login,name,field_dict):
        pass

    def moveFolderToUser(self,destination_user_id,notify,destination_folder_id):
        pass

    def deleteUser(self,user_id,notify,force):
        pass

    def addUserEmail(self,user_id,email):
        pass

    def removeUserEmail(self,user_id,email_alias_id):
        pass

    def changeUserLogin(self,user_id,login):
        pass

    def getUserEmails(self,user_id):
        pass


    # Search
    def search(self,query,limit=None,offset=None):
        headers = self.getHeaders()
        url = self.base_url + '/search'
        data = {
            'query': query
        }
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset
        response = requests.get(url,headers=headers,params=data)
        search_results = response.json()
        items = list()
        try:
            entries = search_results['entries']
        except:
            return search_results
        for item in entries:
            if item['type'] == 'folder':
                fi = BoxFolder(box_type='folder')
                fi.newFromJsonDict(fi,item)
            else:
                fi = BoxFile(box_type='file')
                fi.newFromJsonDict(fi,item)
            items.append(fi)
        return items


    # Shared Items
    def getSharedItemInfo(self,shared_link):
        pass


    # Events
    def getUserEvents(self,stream_type='all',stream_position=0,limit=None):
        headers = self.getHeaders()
        url = self.base_url + '/events'
        data = {
            'stream_type': stream_type,
            'stream_position': stream_position
        }
        if limit:
            data['limit'] = limit
        response = requests.get(url,headers=headers,params=data)
        events_json = response.json()
        next_pos = False
        events = list()
        try:
            next_pos = events_json['next_stream_position']
            entries = events_json['entries']
        except:
            return events_json
        for ev in entries:
            event = Event(box_type='event')
            event.newFromJsonDict(event,ev)
            events.append(event)
        return events


    def getEvents(self,stream_type='all',event_types=None,created_after=None,created_before=None,limit=None,offset=None):
        pass


    def getLongPollURL(self):
        pass

