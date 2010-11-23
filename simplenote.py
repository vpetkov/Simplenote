"""
    simplenote api implementation
    support authentication, creation of new notes, merging existing notes
    with new content, deleteing (moving to trash), geting note from server by key,
    listing notest.

    using urllib2 and json
"""
import urllib2
import base64
import json

class User(object):
    def __init__(self, email, password):
        self.api_url = 'https://simple-note.appspot.com/api'
        self.email = email
        self.authenticate(password)

    def authenticate(self, password):
        """
        return authentication token
        """
        req_data = base64.encodestring('email=%s&password=%s' % (self.email, password))
        req_url = self.api_url+'/login'
        response = urllib2.urlopen(req_url, req_data)
        if response.code != 200:
            raise Exception(response.code)
        self.token = response.read()

class Note(object):
    def __init__(self, user):
        self.user = user
        self.content = ''

    def create(self):
        """
        create new note object on server
        """
        note_object = {'content': self.content}
        req_data = json.dumps(note_object)
        req_url = self.user.api_url+'2/data?auth=%s&email=%s' % (self.user.token, self.user.email)
        response = urllib2.urlopen(req_url, req_data)
        note_object = json.load(response)
        self.key     = note_object[u'key']
        self.deleted = note_object[u'deleted']
        self.version = note_object[u'version']

    def delete(self):
        """
        move note to trash on server
        """
        note_object = {'key': self.key, 'deleted': 1}
        req_data = json.dumps(note_object)
        req_url = self.user.api_url+'2/data/%s?auth=%s&email=%s' % (self.key, self.user.token, self.user.email)
        response = urllib2.urlopen(req_url, req_data)

    def restore(self):
        """
        move note to trash on server
        """
        note_object = {'key': self.key, 'deleted': 0}
        req_data = json.dumps(note_object)
        req_url = self.user.api_url+'2/data/%s?auth=%s&email=%s' % (self.key, self.user.token, self.user.email)
        response = urllib2.urlopen(req_url, req_data)

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content.split('\n')[0]

    def __call__(self):
        return self.content

    def update(self):
        """
        update note object from server
        """
        req_url = self.user.api_url+'2/data/%s?auth=%s&email=%s' % (self.key, self.user.token, self.user.email)
        response = urllib2.urlopen(req_url)
        note_object = json.load(response)
        self.key     = note_object[u'key']
        self.deleted = note_object[u'deleted']
        self.version = note_object[u'version']
        self.content = note_object[u'content']

    def merge(self):
        """
        merge note content
        """
        note_object = {'key': self.key, 'content': self.content, 'version': self.version}
        req_data = json.dumps(note_object)
        req_url = self.user.api_url+'2/data/%s?auth=%s&email=%s' % (self.key, self.user.token, self.user.email)
        urllib2.urlopen(req_url, req_data)


def list_notes(auth_token, email):
    req_url = api_url+'2/index?auth=%s&email=%s' % (auth_token, email)
    response = urllib2.urlopen(req_url)
    index_object = json.load(response)
    return index_object

