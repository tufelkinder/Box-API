# coding=utf-8

'''
Python API for Box.com
'''

__author__ = 'tufelkinder@yahoo.com'
__version__ = '0.0.1'


import calendar
from datetime import timedelta, datetime
import httplib
import os
import rfc822
import sys
import tempfile
import textwrap
import time
import urllib
import urllib2
import urlparse
import gzip
import StringIO
import requests

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



class JSONAwareObject(object):

    def __str__(self):
        '''A string representation of this object instance.

        The return value is the same as the JSON string representation.

        Returns:
          A string representation of this object instance.
        '''
        return self.asJsonString()

    def __unicode__(self):
        '''A string representation of this object instance.

        The return value is the same as the JSON string representation.

        Returns:
          A string representation of this object instance.
        '''
        return self.asJsonString()

    def asJsonString(self):
        '''A JSON string representation of this object instance.

        Returns:
          A JSON string representation of this object instance
       '''
        return json.dumps(self.asDict(), sort_keys=True)

    def asDict(self):
        vals = []
        for field in self.FIELDS:
            vals.append(getattr(self,field))
        data = dict(zip(self.FIELDS,vals))
        return data

    @staticmethod
    def newFromJsonDict(self,data):
        for key in data:
            if key == 'type':
                setattr(self,'box_type',data[key])
            else:
                setattr(self,key,data[key])



class BoxError(Exception):
    '''Base class for Box errors'''

    @property
    def message(self):
        '''Returns the first argument used to construct this error.'''
        return self.args[0]


class BoxUser(JSONAwareObject):
    '''
    type # For users is user'
    id # A unique string identifying this user
    name # The name of this user
    login # The email address this user uses to login
    created_at # The time this user was created (timestamp)
    modified_at # The time this user was last modified
    role # This user's enterprise role. Can be admin, coadmin, or user
    language # The language of this user (ISO 639-1 Language Code)
    space_amount # The user's total available space amount in bytes (integer)
    space_used # The amount of space in use by the user (integer)
    max_upload_size # The maximum individual file size in bytes this user can have (integer)
    tracking_codes # An array of key/value pairs set by the user's admin 
    can_see_managed_users # Whether this user can see other enterprise users in its contact list (Boolean)
    is_sync_enabled # Whether or not this user can use Box Sync (boolean)
    status # Can be active or inactive
    job_title # The user's job title
    phone # The user's phone number
    address # The user's address
    avatar_url # URL of this user's avatar image
    is_exempt_from_device_limits # Whether to exempt this user from Enterprise device limits
    is_exempt_from_login_verification # Whether or not this user must use two-factor authentication
    enterprise # Mini representation of this user's enterprise, including the ID of its enterprise
    '''

    FIELDS = ['box_type','user_type','user_id','name','login','created_at',
              'modified_at','role','language','space_amount','space_used',
              'max_upload_size','tracking_codes','can_see_managed_users',
              'is_sync_enabled','status','job_title','phone','address',
              'avatar_url','is_exempt_from_device_limits',
              'is_exempt_from_login_verification','enterprise']

    def __init__(self,
                 box_type=None,
                 user_type=None,
                 user_id=None,
                 name=None,
                 login=None,
                 created_at=None,
                 modified_at=None,
                 role=None,
                 language=None,
                 space_amount=None,
                 space_used=None,
                 max_upload_size=None,
                 tracking_codes=None,
                 can_see_managed_users=None,
                 is_sync_enabled=None,
                 status=None,
                 job_title=None,
                 phone=None,
                 address=None,
                 avatar_url=None,
                 is_exempt_from_device_limits=None,
                 is_exempt_from_login_verification=None,
                 enterprise=None):
        self.box_type = box_type
        self.user_type = user_type
        self.user_id = user_id
        self.name = name
        self.login = login
        self.created_at = created_at
        self.modified_at = modified_at
        self.role = role
        self.language = language
        self.space_amount = space_amount
        self.space_used = space_used
        self.max_upload_size = max_upload_size
        self.tracking_codes = tracking_codes
        self.can_see_managed_users = can_see_managed_users
        self.is_sync_enabled = is_sync_enabled
        self.status = status
        self.job_title = job_title
        self.phone = phone
        self.address = address
        self.avatar_url = avatar_url
        self.is_exempt_from_device_limits = is_exempt_from_device_limits
        self.is_exempt_from_login_verification = is_exempt_from_login_verification
        self.enterprise = enterprise


    def getBoxType(self):
        return self._box_type

    def setBoxType(self,box_type):
        self._box_type = box_type

    box_type = property(getBoxType,setBoxType,doc="")


    def getUserType(self):
        return self._user_type

    def setUserType(self,user_type):
        self._user_type = user_type

    user_type = property(getUserType,setUserType,doc="")


    def getUserId(self):
        return self._user_id

    def setUserId(self,user_id):
        self._user_id = user_id

    user_id = property(getUserId,setUserId,doc="")


    def getName(self):
        return self._name

    def setName(self,name):
        self._name = name

    name = property(getName,setName,doc="")


    def getLogin(self):
        return self._login

    def setLogin(self,login):
        self._login = login

    login = property(getLogin,setLogin,doc="")


    def getCreatedAt(self):
        return self._created_at

    def setCreatedAt(self,created_at):
        self._created_at = created_at

    created_at = property(getCreatedAt,setCreatedAt,doc="")


    def getModifiedAt(self):
        return self._modified_at

    def setModifiedAt(self,modified_at):
        self._modified_at = modified_at

    modified_at = property(getModifiedAt,setModifiedAt,doc="")


    def getRole(self):
        return self._role

    def setRole(self,role):
        self._role = role

    role = property(getRole,setRole,doc="")


    def getLanguage(self):
        return self._language

    def setLanguage(self,language):
        self._language = language

    language = property(getLanguage,setLanguage,doc="")


    def getSpaceAmount(self):
        return self._space_amount

    def setSpaceAmount(self,space_amount):
        self._space_amount = space_amount

    space_amount = property(getSpaceAmount,setSpaceAmount,doc="")


    def getSpaceUsed(self):
        return self._space_used

    def setSpaceUsed(self,space_used):
        self._space_used = space_used

    space_used = property(getSpaceUsed,setSpaceUsed,doc="")


    def getMaxUploadSize(self):
        return self._max_upload_size

    def setMaxUploadSize(self,max_upload_size):
        self._max_upload_size = max_upload_size

    max_upload_size = property(getMaxUploadSize,setMaxUploadSize,doc="")


    def getTrackingCodes(self):
        return self._tracking_codes

    def setTrackingCodes(self,tracking_codes):
        self._tracking_codes = tracking_codes

    tracking_codes = property(getTrackingCodes,setTrackingCodes,doc="")


    def getCanSeeManagedUsers(self):
        return self._can_see_managed_users

    def setCanSeeManagedUsers(self,can_see_managed_users):
        self._can_see_managed_users = can_see_managed_users

    can_see_managed_users = property(getCanSeeManagedUsers,setCanSeeManagedUsers,doc="")


    def getIsSyncEnabled(self):
        return self._is_sync_enabled

    def setIsSyncEnabled(self,is_sync_enabled):
        self._is_sync_enabled = is_sync_enabled

    is_sync_enabled = property(getIsSyncEnabled,setIsSyncEnabled,doc="")


    def getStatus(self):
        return self._status

    def setStatus(self,status):
        self._status = status

    status = property(getStatus,setStatus,doc="")


    def getJobTitle(self):
        return self._job_title

    def setJobTitle(self,job_title):
        self._job_title = job_title

    job_title = property(getJobTitle,setJobTitle,doc="")


    def getPhone(self):
        return self._phone

    def setPhone(self,phone):
        self._phone = phone

    phone = property(getPhone,setPhone,doc="")


    def getAddress(self):
        return self._address

    def setAddress(self,address):
        self._address = address

    address = property(getAddress,setAddress,doc="")


    def getAvatarUrl(self):
        return self._avatar_url

    def setAvatarUrl(self,avatar_url):
        self._avatar_url = avatar_url

    avatar_url = property(getAvatarUrl,setAvatarUrl,doc="")


    def getIsExemptFromDeviceLimits(self):
        return self._is_exempt_from_device_limits

    def setIsExemptFromDeviceLimits(self,is_exempt_from_device_limits):
        self._is_exempt_from_device_limits = is_exempt_from_device_limits

    is_exempt_from_device_limits = property(getIsExemptFromDeviceLimits,setIsExemptFromDeviceLimits,doc="")


    def getIsExemptFromLoginVerification(self):
        return self._is_exempt_from_login_verification

    def setIsExemptFromLoginVerification(self,is_exempt_from_login_verification):
        self._is_exempt_from_login_verification = is_exempt_from_login_verification

    is_exempt_from_login_verification = property(getIsExemptFromLoginVerification,setIsExemptFromLoginVerification,doc="")


    def getEnterprise(self):
        return self._enterprise

    def setEnterprise(self,enterprise):
        self._enterprise = enterprise

    enterprise = property(getEnterprise,setEnterprise,doc="")


class BoxGroup(JSONAwareObject):
    pass

class BoxFile(JSONAwareObject):
    '''
        Class representation of a Box File object with the properties:
        type # For files is 'file'
        id # Box's unique string identifying this file
        sequence_id # A unique ID for use with the /events endpoint
        etag # A unique string identifying the version of this file.
        sha1 # The sha1 hash of this file
        name # The name of this file
        description # The description of this file
        size # Size of this file in bytes
        path_collection # The path of folders to this item, starting at the root
        created_at # When this file was created on Box's servers
        modified_at # When this file was last updated on the Box servers
        trashed_at # When this file was last moved to the trash
        purged_at # When this file will be permanently deleted
        content_created_at # When the content of this file was created (more info)
        content_modified_at # When the content of this file was last modified (more info)
        created_by # The user who first created file
        modified_by # The user who last updated this file
        owned_by # The user who owns this file
        shared_link # The shared link object for this file
        parent # The folder this file is contained in
        item_status # Whether this item is deleted or not
    '''

    FIELDS = ['box_type','id','sequence_id','etag','sha1','name','description',
              'size','path_collection','created_at','modified_at',
              'trashed_at','purged_at','content_created_at',
              'content_modified_at','created_by','modified_by','owned_by',
              'shared_link','parent','item_status']

    def __init__(self,
                 box_type=None,
                 id=None,
                 sequence_id=None,
                 etag=None,
                 sha1=None,
                 name=None,
                 description=None,
                 size=None,
                 path_collection=None,
                 created_at=None,
                 modified_at=None,
                 trashed_at=None,
                 purged_at=None,
                 content_created_at=None,
                 content_modified_at=None,
                 created_by=None,
                 modified_by=None,
                 owned_by=None,
                 shared_link=None,
                 parent=None,
                 item_status=None):
        self.box_type = box_type
        self.id = id
        self.sequence_id = sequence_id
        self.etag = etag
        self.sha1 = sha1
        self.name = name
        self.description = description
        self.size = size
        self.path_collection = path_collection
        self.created_at = created_at
        self.modified_at = modified_at
        self.trashed_at = trashed_at
        self.purged_at = purged_at
        self.content_created_at = content_created_at
        self.content_modified_at = content_modified_at
        self.created_by = created_by
        self.modified_by = modified_by
        self.owned_by = owned_by
        self.shared_link = shared_link
        self.parent = parent
        self.item_status = item_status


    def getType(self):
        return self._box_type

    def setType(self,box_type):
        self._box_type = box_type

    box_type = property(getType,setType,doc="")


    def getId(self):
        return self._id

    def setId(self,id):
        self._id = id

    id = property(getId,setId,doc="")


    def getSequenceId(self):
        return self._sequence_id

    def setSequenceId(self,sequence_id):
        self._sequence_id = sequence_id

    sequence_id = property(getSequenceId,setSequenceId,doc="")


    def getEtag(self):
        return self._etag

    def setEtag(self,etag):
        self._etag = etag

    etag = property(getEtag,setEtag,doc="")


    def getSha1(self):
        return self._sha1

    def setSha1(self,sha1):
        self._sha1 = sha1

    sha1 = property(getSha1,setSha1,doc="")


    def getName(self):
        return self._name

    def setName(self,name):
        self._name = name

    name = property(getName,setName,doc="")


    def getDescription(self):
        return self._description

    def setDescription(self,description):
        self._description = description

    description = property(getDescription,setDescription,doc="")


    def getSize(self):
        return self._size

    def setSize(self,size):
        self._size = size

    size = property(getSize,setSize,doc="")


    def getPathCollection(self):
        return self._path_collection

    def setPathCollection(self,path_collection):
        self._path_collection = path_collection

    path_collection = property(getPathCollection,setPathCollection,doc="")


    def getCreatedAt(self):
        return self._created_at

    def setCreatedAt(self,created_at):
        self._created_at = created_at

    created_at = property(getCreatedAt,setCreatedAt,doc="")


    def getModifiedAt(self):
        return self._modified_at

    def setModifiedAt(self,modified_at):
        self._modified_at = modified_at

    modified_at = property(getModifiedAt,setModifiedAt,doc="")


    def getTrashedAt(self):
        return self._trashed_at

    def setTrashedAt(self,trashed_at):
        self._trashed_at = trashed_at

    trashed_at = property(getTrashedAt,setTrashedAt,doc="")


    def getPurgedAt(self):
        return self._purged_at

    def setPurgedAt(self,purged_at):
        self._purged_at = purged_at

    purged_at = property(getPurgedAt,setPurgedAt,doc="")


    def getContentCreatedAt(self):
        return self._content_created_at

    def setContentCreatedAt(self,content_created_at):
        self._content_created_at = content_created_at

    content_created_at = property(getContentCreatedAt,setContentCreatedAt,doc="")


    def getContentModifiedAt(self):
        return self._content_modified_at

    def setContentModifiedAt(self,content_modified_at):
        self._content_modified_at = content_modified_at

    content_modified_at = property(getContentModifiedAt,setContentModifiedAt,doc="")


    def getCreatedBy(self):
        return self._created_by

    def setCreatedBy(self,created_by):
        try:
            cb = BoxUser(box_type='user')
            cb.newFromJsonDict(cb,created_by)
            self._created_by = cb
        except:
            self._created_by = created_by

    created_by = property(getCreatedBy,setCreatedBy,doc="")


    def getModifiedBy(self):
        return self._modified_by

    def setModifiedBy(self,modified_by):
        try:
            mb = BoxUser(box_type='user')
            mb.newFromJsonDict(mb,modified_by)
            self._modified_by = mb
        except:
            self._modified_by = modified_by

    modified_by = property(getModifiedBy,setModifiedBy,doc="")


    def getOwnedBy(self):
        return self._owned_by

    def setOwnedBy(self,owned_by):
        try:
            ob = BoxUser(box_type='user')
            ob.newFromJsonDict(mb,owned_by)
            self._owned_by = ob
        except:
            self._owned_by = owned_by

    owned_by = property(getOwnedBy,setOwnedBy,doc="")


    def getSharedLink(self):
        return self._shared_link

    def setSharedLink(self,shared_link):
        self._shared_link = shared_link

    shared_link = property(getSharedLink,setSharedLink,doc="")


    def getParent(self):
        return self._parent

    def setParent(self,parent):
        try:
            bf = BoxFolder(box_type='folder')
            bf.newFromJsonDict(bf,parent)
            self._parent = bf
        except:
            self._parent = parent

    parent = property(getParent,setParent,doc="")


    def getItemStatus(self):
        return self._item_status

    def setItemStatus(self,item_status):
        self._item_status = item_status

    item_status = property(getItemStatus,setItemStatus,doc="")




class BoxFolder(JSONAwareObject):
    '''
        Class representation of a Box Folder with the properties:

        type # For folders is 'folder'
        id # The folder's ID
        sequence_id # A unique ID for use with the /events endpoint
        etag # A unique string identifying the version of this folder
        name # The name of the folder
        created_at # The time the folder was created
        modified_at # The time the folder or its contents were last modified
        description # The description of the folder
        size # The folder size in bytes
        path_collection # The path of folders to this item, starting at the root
        created_by # The user who created this folder
        modified_by # The user who last modified this folder
        owned_by # The user who owns this folder
        shared_link # The shared link for this folder
        folder_upload_email # The upload email address for this folder
        parent # The folder that contains this one
        item_status # Whether this item is deleted or not
        item_collection # A collection of mini file and folder objects contained in this folder
        sync_state # Whether this folder will be synced by the Box sync clients or not
    '''

    FIELDS = ['box_type','id','sequence_id','etag','name','created_at','modified_at','description',
              'size','path_collection','created_by','modified_by','owned_by','shared_link'
              'folder_upload_email','parent','item_status','item_collection','sync_state']

    def __init__(self,
                 box_type=None,
                 id=None,
                 sequence_id=None,
                 etag=None,
                 name=None,
                 created_at=None,
                 modified_at=None,
                 description=None,
                 size=None,
                 path_collection=None,
                 created_by=None,
                 modified_by=None,
                 owned_by=None,
                 shared_linkfolder_upload_email=None,
                 parent=None,
                 item_status=None,
                 item_collection=None,
                 sync_state=None):
        self.box_type = box_type
        self.id = id
        self.sequence_id = sequence_id
        self.etag = etag
        self.name = name
        self.created_at = created_at
        self.modified_at = modified_at
        self.description = description
        self.size = size
        self.path_collection = path_collection
        self.created_by = created_by
        self.modified_by = modified_by
        self.owned_by = owned_by
        self.shared_linkfolder_upload_email = shared_linkfolder_upload_email
        self.parent = parent
        self.item_status = item_status
        self.item_collection = item_collection
        self.sync_state = sync_state


    def getType(self):
        return self._box_type

    def setType(self,box_type):
        self._box_type = box_type

    box_type = property(getType,setType,doc="")


    def getId(self):
        return self._id

    def setId(self,id):
        self._id = id

    id = property(getId,setId,doc="")


    def getSequenceId(self):
        return self._sequence_id

    def setSequenceId(self,sequence_id):
        self._sequence_id = sequence_id

    sequence_id = property(getSequenceId,setSequenceId,doc="")


    def getEtag(self):
        return self._etag

    def setEtag(self,etag):
        self._etag = etag

    etag = property(getEtag,setEtag,doc="")


    def getName(self):
        return self._name

    def setName(self,name):
        self._name = name

    name = property(getName,setName,doc="")


    def getCreatedAt(self):
        return self._created_at

    def setCreatedAt(self,created_at):
        self._created_at = created_at

    created_at = property(getCreatedAt,setCreatedAt,doc="")


    def getModifiedAt(self):
        return self._modified_at

    def setModifiedAt(self,modified_at):
        self._modified_at = modified_at

    modified_at = property(getModifiedAt,setModifiedAt,doc="")


    def getDescription(self):
        return self._description

    def setDescription(self,description):
        self._description = description

    description = property(getDescription,setDescription,doc="")


    def getSize(self):
        return self._size

    def setSize(self,size):
        self._size = size

    size = property(getSize,setSize,doc="")


    def getPathCollection(self):
        return self._path_collection

    def setPathCollection(self,path_collection):
        self._path_collection = path_collection

    path_collection = property(getPathCollection,setPathCollection,doc="")


    def getCreatedBy(self):
        return self._created_by

    def setCreatedBy(self,created_by):
        try:
            cb = BoxUser(box_type='user')
            cb.newFromJsonDict(cb,created_by)
            self._created_by = cb
        except:
            self._created_by = created_by

    created_by = property(getCreatedBy,setCreatedBy,doc="")


    def getModifiedBy(self):
        return self._modified_by

    def setModifiedBy(self,modified_by):
        try:
            mb = BoxUser(box_type='user')
            mb.newFromJsonDict(mb,modified_by)
            self._modified_by = mb
        except:
            self._modified_by = modified_by

    modified_by = property(getModifiedBy,setModifiedBy,doc="")


    def getOwnedBy(self):
        return self._owned_by

    def setOwnedBy(self,owned_by):
        try:
            ob = BoxUser(box_type='user')
            ob.newFromJsonDict(mb,owned_by)
            self._owned_by = ob
        except:
            self._owned_by = owned_by

    owned_by = property(getOwnedBy,setOwnedBy,doc="")


    def getSharedLinkfolderUploadEmail(self):
        return self._shared_linkfolder_upload_email

    def setSharedLinkfolderUploadEmail(self,shared_linkfolder_upload_email):
        self._shared_linkfolder_upload_email = shared_linkfolder_upload_email

    shared_linkfolder_upload_email = property(getSharedLinkfolderUploadEmail,setSharedLinkfolderUploadEmail,doc="")


    def getParent(self):
        return self._parent

    def setParent(self,parent):
        try:
            bf = BoxFolder(box_type='folder')
            bf.newFromJsonDict(bf,parent)
            self._parent = bf
        except:
            self._parent = parent

    parent = property(getParent,setParent,doc="")


    def getItemStatus(self):
        return self._item_status

    def setItemStatus(self,item_status):
        self._item_status = item_status

    item_status = property(getItemStatus,setItemStatus,doc="")


    def getItemCollection(self):
        return self._item_collection

    def setItemCollection(self,item_collection):
        self._item_collection = item_collection

    item_collection = property(getItemCollection,setItemCollection,doc="")


    def getSyncState(self):
        return self._sync_state

    def setSyncState(self,sync_state):
        self._sync_state = sync_state

    sync_state = property(getSyncState,setSyncState,doc="")



class Comment(JSONAwareObject):
    '''
        Class representation of a Box Comment with the properties:
        type # For comments is 'comment'
        id # A unique string identifying this comment
        is_reply_comment # Whether or not this comment is a reply to another comment
        message # The comment text that the user typed
        tagged_message # The string representing the comment text with @mentions included. @mention format is @[id:username]. Field is not included by default.
        created_by # A mini user object representing the author of the comment
        created_at # The time this comment was created
        item # The object this comment was placed on
        modified_at # The time this comment was last modified
    '''

    FIELDS = ['box_type','id','is_reply_comment','message','tagged_message',
              'created_by','created_at','item','modified_at']

    def __init__(self,
                 box_type=None,
                 id=None,
                 is_reply_comment=None,
                 message=None,
                 tagged_message=None,
                 created_by=None,
                 created_at=None,
                 item=None,
                 modified_at=None):
        self.box_type = box_type
        self.id = id
        self.is_reply_comment = is_reply_comment
        self.message = message
        self.tagged_message = tagged_message
        self.created_by = created_by
        self.created_at = created_at
        self.item = item
        self.modified_at = modified_at


    def getType(self):
        return self._box_type

    def setType(self,box_type):
        self._box_type = box_type

    box_type = property(getType,setType,doc="")


    def getId(self):
        return self._id

    def setId(self,id):
        self._id = id

    id = property(getId,setId,doc="")


    def getIsReplyComment(self):
        return self._is_reply_comment

    def setIsReplyComment(self,is_reply_comment):
        self._is_reply_comment = is_reply_comment

    is_reply_comment = property(getIsReplyComment,setIsReplyComment,doc="")


    def getMessage(self):
        return self._message

    def setMessage(self,message):
        self._message = message

    message = property(getMessage,setMessage,doc="")


    def getTaggedMessage(self):
        return self._tagged_message

    def setTaggedMessage(self,tagged_message):
        self._tagged_message = tagged_message

    tagged_message = property(getTaggedMessage,setTaggedMessage,doc="")


    def getCreatedBy(self):
        return self._created_by

    def setCreatedBy(self,created_by):
        try:
            cb = BoxUser(box_type='user')
            cb.newFromJsonDict(cb,created_by)
            self._created_by = cb
        except:
            self._created_by = created_by

    created_by = property(getCreatedBy,setCreatedBy,doc="")


    def getCreatedAt(self):
        return self._created_at

    def setCreatedAt(self,created_at):
        self._created_at = created_at

    created_at = property(getCreatedAt,setCreatedAt,doc="")


    def getItem(self):
        return self._item

    def setItem(self,item):
        self._item = item

    item = property(getItem,setItem,doc="")


    def getModifiedAt(self):
        return self._modified_at

    def setModifiedAt(self,modified_at):
        self._modified_at = modified_at

    modified_at = property(getModifiedAt,setModifiedAt,doc="")



class Discussion(JSONAwareObject):
    '''
        Class representing a Box Discussion with the properties:

        type # For discussions is 'discussion'
        id # A unique string identifying this comment
        name # The title of this discussion
        parent # The folder this discussion is related to
        description # The description of this discussion
        created_by # The user who created this discussion
        created_at # The time this discussion was created
        modified_at # The time this discussion was last modified
    '''

    FIELDS = ['box_type','id','name','parent','description','created_by',
              'created_at','modified_at']

    def __init__(self,
                 box_type=None,
                 id=None,
                 name=None,
                 parent=None,
                 description=None,
                 created_by=None,
                 created_at=None,
                 modified_at=None):
        self.box_type = box_type
        self.id = id
        self.name = name
        self.parent = parent
        self.description = description
        self.created_by = created_by
        self.created_at = created_at
        self.modified_at = modified_at


    def getType(self):
        return self._box_type

    def setType(self,box_type):
        self._box_type = box_type

    box_type = property(getType,setType,doc="")


    def getId(self):
        return self._id

    def setId(self,id):
        self._id = id

    id = property(getId,setId,doc="")


    def getName(self):
        return self._name

    def setName(self,name):
        self._name = name

    name = property(getName,setName,doc="")


    def getParent(self):
        return self._parent

    def setParent(self,parent):
        try:
            bf = BoxFolder(box_type='folder')
            bf.newFromJsonDict(bf,parent)
            self._parent = bf
        except:
            self._parent = parent

    parent = property(getParent,setParent,doc="")


    def getDescription(self):
        return self._description

    def setDescription(self,description):
        self._description = description

    description = property(getDescription,setDescription,doc="")


    def getCreatedBy(self):
        return self._created_by

    def setCreatedBy(self,created_by):
        try:
            cb = BoxUser(box_type='user')
            cb.newFromJsonDict(cb,created_by)
            self._created_by = cb
        except:
            self._created_by = created_by

    created_by = property(getCreatedBy,setCreatedBy,doc="")


    def getCreatedAt(self):
        return self._created_at

    def setCreatedAt(self,created_at):
        self._created_at = created_at

    created_at = property(getCreatedAt,setCreatedAt,doc="")


    def getModifiedAt(self):
        return self._modified_at

    def setModifiedAt(self,modified_at):
        self._modified_at = modified_at

    modified_at = property(getModifiedAt,setModifiedAt,doc="")



class Collaboration(JSONAwareObject):
    '''
        Class representation of a Box Collaboration with the properties:

        type # For collaborations is 'collaboration'
        id # A unique string identifying this collaboration
        created_by # The user who created this collaboration
        created_at # The time this collaboration was created
        modified_at # The time this collaboration was last modified
        expires_at # The time this collaboration will expire
        status # The status of this collab. Can be accepted, pending, or rejected
        accessible_by # The user who the collaboration applies to
        role # The level of access this user has
        acknowledged_at # When the status of this collab was changed
        item # The folder this discussion is related to

    '''

    FIELDS = ['box_type','id','created_by','created_at','modified_at','expires_at',
              'status','accessible_by','role','acknowledged_at','item']

    def __init__(self,
                 box_type=None,
                 id=None,
                 created_by=None,
                 created_at=None,
                 modified_at=None,
                 expires_at=None,
                 status=None,
                 accessible_by=None,
                 role=None,
                 acknowledged_at=None,
                 item=None):
        self.box_type = box_type
        self.id = id
        self.created_by = created_by
        self.created_at = created_at
        self.modified_at = modified_at
        self.expires_at = expires_at
        self.status = status
        self.accessible_by = accessible_by
        self.role = role
        self.acknowledged_at = acknowledged_at
        self.item = item


    def getType(self):
        return self._box_type

    def setType(self,box_type):
        self._box_type = box_type

    box_type = property(getType,setType,doc="")


    def getId(self):
        return self._id

    def setId(self,id):
        self._id = id

    id = property(getId,setId,doc="")


    def getCreatedBy(self):
        return self._created_by

    def setCreatedBy(self,created_by):
        try:
            cb = BoxUser(box_type='user')
            cb.newFromJsonDict(cb,created_by)
            self._created_by = cb
        except:
            self._created_by = created_by

    created_by = property(getCreatedBy,setCreatedBy,doc="")


    def getCreatedAt(self):
        return self._created_at

    def setCreatedAt(self,created_at):
        self._created_at = created_at

    created_at = property(getCreatedAt,setCreatedAt,doc="")


    def getModifiedAt(self):
        return self._modified_at

    def setModifiedAt(self,modified_at):
        self._modified_at = modified_at

    modified_at = property(getModifiedAt,setModifiedAt,doc="")


    def getExpiresAt(self):
        return self._expires_at

    def setExpiresAt(self,expires_at):
        self._expires_at = expires_at

    expires_at = property(getExpiresAt,setExpiresAt,doc="")


    def getStatus(self):
        return self._status

    def setStatus(self,status):
        self._status = status

    status = property(getStatus,setStatus,doc="")


    def getAccessibleBy(self):
        return self._accessible_by

    def setAccessibleBy(self,accessible_by):
        self._accessible_by = accessible_by

    accessible_by = property(getAccessibleBy,setAccessibleBy,doc="")


    def getRole(self):
        return self._role

    def setRole(self,role):
        self._role = role

    role = property(getRole,setRole,doc="")


    def getAcknowledgedAt(self):
        return self._acknowledged_at

    def setAcknowledgedAt(self,acknowledged_at):
        self._acknowledged_at = acknowledged_at

    acknowledged_at = property(getAcknowledgedAt,setAcknowledgedAt,doc="")


    def getItem(self):
        return self._item

    def setItem(self,item):
        self._item = item

    item = property(getItem,setItem,doc="")


class Event(JSONAwareObject):
    '''
        Class representation of a Box Event with the properties:

        type # For events is 'event'
        event_id # The id of the event, used for de-duplication purposes
        created_by # The user that performed the action
        event_type # One of the above listed event types
        session_id # The session of the user that performed the action
        source # The object that was modified. See Object definitions for appropriate object: file, folder, comment, etc. Not all events have a source object.

    '''

    FIELDS = ['box_type','event_id','created_by','event_type','session_id','source']

    def __init__(self,
                 box_type=None,
                 event_id=None,
                 created_by=None,
                 event_type=None,
                 session_id=None,
                 source=None):
        self.box_type = box_type
        self.event_id = event_id
        self.created_by = created_by
        self.event_type = event_type
        self.session_id = session_id
        self.source = source


    def getType(self):
        return self._box_type

    def setType(self,box_type):
        self._box_type = box_type

    box_type = property(getType,setType,doc="")


    def getEventId(self):
        return self._event_id

    def setEventId(self,event_id):
        self._event_id = event_id

    event_id = property(getEventId,setEventId,doc="")


    def getCreatedBy(self):
        return self._created_by

    def setCreatedBy(self,created_by):
        try:
            cb = BoxUser(box_type='user')
            cb.newFromJsonDict(cb,created_by)
            self._created_by = cb
        except:
            self._created_by = created_by

    created_by = property(getCreatedBy,setCreatedBy,doc="")


    def getEventType(self):
        return self._event_type

    def setEventType(self,event_type):
        self._event_type = event_type

    event_type = property(getEventType,setEventType,doc="")


    def getSessionId(self):
        return self._session_id

    def setSessionId(self,session_id):
        self._session_id = session_id

    session_id = property(getSessionId,setSessionId,doc="")


    def getSource(self):
        return self._source

    def setSource(self,source):
        try:
            src_type = source['type']
            if src_type == 'folder':
                src = BoxFolder(box_type='folder')
                src.newFromJsonDict(src,source)
                self._source = src
            elif src_type == 'file':
                src = BoxFile(box_type='file')
                src.newFromJsonDict(src,source)
                self._source = src
            elif src_type == 'comment':
                src = Comment(box_type='comment')
                src.newFromJsonDict(src,source)
                self._source = src
            elif src_type == 'collaboration':
                src = Collaboration(box_type='collaboration')
                src.newFromJsonDict(src,source)
                self._source = src
            elif src_type == 'user':
                src = BoxUser(box_type='user')
                src.newFromJsonDict(src,source)
                self._source = src
            elif src_type == 'group':
                src = BoxGroup(box_type='group')
                src.newFromJsonDict(src,source)
                self._source = src
#            elif src_type == 'tag':
#                src = Tag(box_type='tag')
#                src.newFromJsonDict(src,source)
#                self._source = src
            else:
                self._source = source
        except:
            self._source = source

    source = property(getSource,setSource,doc="")

  

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
        return self._token_expiration < datetime.now()


    def authRefresh(self):
        url = 'https://api.box.com/oauth2/token'
        data = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'refresh_token': self._refresh_token,
            'grant_type': 'refresh_token'
        }

        response = requests.post(url, data=data)
        auth_info = response.json
        try:
            error = auth_info['error']
            error_desc = auth_info['error_description']
            return { "error": error, "error_desc": error_desc }
        except:
            self._access_token = auth_info['access_token']
            self._token_expiration = datetime.now() + timedelta(seconds=int(auth_info['expires_in']))
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

    def getFolderItems(self,folder_id,offset=None,limit=None):
        headers = self.getHeaders()
        data = {}
        if offset:
            data['offset'] = offset
        if limit:
            data['limit'] = limit
        url = self.base_url + '/folders/{0}/items'.format(folder_id)
        response = requests.get(url,headers=headers,params=data)
        folder_items = response.json
        try:
            item_count = folder_items['total_count'] 
        except:
            raise BoxError('getFolderItems failed: ' + folder_items)
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
        return items


    def getFolderInfo(self,folder_id):
        headers = self.getHeaders()
        url = self.base_url + '/folders/{0}'.format(folder_id)
        response = requests.get(url,headers=headers)
        folder_info = response.json


    def createFolder(self,folder_name,parent_id):
        headers = self.getHeaders()
        url = self.base_url + '/folders'
        data = json.dumps({
            "name": folder_name,
            "parent": { "id": parent_id }
        })
        response = requests.post(url,headers=headers,data=data)
        folder_info = response.json
        # parse folder_info into folder object??
        return folder_info


    def copyFolder(self,folder_id,dest_parent_id,new_folder_name):
        headers = self.getHeaders()
        url = self.base_url + '/folders/{0}/copy'.format(folder_id)
        data = json.dumps({
            "name": new_folder_name,
            "parent": { "id": dest_parent_id }
        })
        response = requests.post(url,headers=headers,data=data)
        folder_info = response.json
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
        file_info = response.json
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
        file_info = response.json
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
        file_info = response.json
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
        file_info = response.json
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
        user_info = response.json
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
        users_info = response.json
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

    def moveFolder(self,destination_user_id,notify,destination_folder_id):
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
        search_results = response.json
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
        events_json = response.json
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

