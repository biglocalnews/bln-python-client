#!/usr/bin/env python3
'''Big Local News Python Client.'''
from multiprocessing import Pool, cpu_count
from http.client import responses
import argparse
import json
import os
import sys

import pandas as pd
import requests
from . import queries as q


class Client:
    '''Big Local News Python Client.'''
    def __init__(self, token, tier='prod'):
        '''Creates a Big Local News Python Client.

        Args:
            token: a personal token generated on the Big Local News website.
            tier: only 'prod' will work for external developers.

        Returns:
            client: a Big Local News Python Client.
        '''
        self.token = token
        self.endpoint = {
            'local': 'http://localhost:8080/graphql',
            'dev': 'https://dev-api.biglocalnews.org/graphql',
            'prod': 'https://api.biglocalnews.org/graphql',
        }[tier]

    def _gql(self, query, variables={}):
        # remove 'self' so mutations can just pass 'locals()'
        variables = {k: v for k, v in variables.items() if k != 'self'}
        data, err = _gql(self.endpoint, self.token, query, variables)
        # network error
        if err:
            return perr(err)
        for k, v in data.items():
            # mutation error
            if 'err' in v:
                return perr(v['err'])
            # mutation result
            if 'ok' in v:
                return v['ok']
        # query result
        return data

    def node(self, id):
        '''Returns data on the specified node or None if error.'''
        return self._gql(q.query_node, {'id': id})

    def user(self):
        '''Returns information about the current user.'''
        return self._gql(q.query_user)

    def groupRoles(self):
        '''Returns the current user's group roles and groups.'''
        return self._gql(q.query_groupRoles)

    def projectRoles(self):
        '''Returns the current user's project roles and projects.'''
        return self._gql(q.query_projectRoles)

    def effectiveProjectRoles(self):
        '''Returns the current user's effective project roles and projects.'''
        return self._gql(q.query_effectiveProjectRoles)

    def personalTokens(self):
        '''Returns the current user's personal tokens.'''
        return self._gql(q.query_personalTokens)

    def oauth2Codes(self):
        '''Returns the current user's OAuth2 codes (authorized plugins).'''
        return self._gql(q.query_oauth2Codes)

    def oauth2Tokens(self):
        '''Returns the current user's OAuth2 tokens (authorized plugins).'''
        return self._gql(q.query_oauth2Tokens)

    def oauth2Clients(self):
        '''Returns the current user's owned OAuth2 clients (plugins).'''
        return self._gql(q.query_oauth2Clients)

    def userNames(self):
        '''Returns a list of the user names on the platform.'''
        return self._gql(q.query_userNames)

    def groupNames(self):
        '''Returns a list of the group names on the platform.'''
        return self._gql(q.query_groupNames)

    def openProjects(self):
        '''Returns a list of open projects.'''
        return self._gql(q.query_openProjects)

    def oauth2ClientsPublic(self):
        '''Returns a list of Public OAuth2 Clients, i.e. plugins.'''
        return self._gql(q.query_oauth2ClientsPublic)

    def authorizeOauth2Client(self, id, state):
        '''Authorize an OAuth2 client by id with state.'''
        return self._gql(q.mutation_authorizeOauth2Client, locals())

    def authorizeWithPkceOauth2Client(self, id, state, codeChallenge):
        '''Authorize an OAuth2 client by id with state and code challenge.'''
        return self._gql(q.mutation_authorizeWithPkceOauth2Client, locals())

    def createFileDownloadUri(self, projectId, fileName):
        '''Create a file download uri with a projectId and fileName.'''
        return self._gql(q.mutation_createFileDownloadUri, locals())

    def createFileUploadUri(self, projectId, fileName):
        '''Create a file upload uri with a projectId and fileName.'''
        return self._gql(q.mutation_createFileUploadUri, locals())

    def create_group(
        self,
        name,
        contact,
        contactMethod='EMAIL',
        description='',
        userRoles=None,
    ):
        '''Creates a group.

        Args:
            id: id of group to update.
            name: a valid group name.
            contact: a phone number with format "+X (XXX) XXX-XXXX" or email.
            contactMethod: PHONE or EMAIL.
            description: a group description.
            userRoles: list who is an admin, editor, and viewer.

        Returns:
            group: the resulting group or None if error.
        '''
        return self._gql(q.mutation_createGroup, locals())

    def createOauth2Client(
        self,
        name,
        contact,
        contactMethod='EMAIL',
        description='',
        scopes=['project_read', 'project_write'],
        redirectUris=[],
        pkceRequired=False,
    ):
        '''Creates an OAuth2 Client (plugin).'''
        return self._gql(q.mutation_createOauth2Client, locals())

    def createPersonalToken(self):
        '''Creates a personal token.'''
        return self._gql(q.mutation_createPersonalToken)

    def createProject(
        self,
        name,
        contact,
        contactMethod='EMAIL',
        description='',
        isOpen=False,
        userRoles={
            'admin': [],
            'editor': [],
            'viewer': []
        },
        groupRoles={
            'admin': [],
            'editor': [],
            'viewer': []
        },
        files=[],
    ):
        '''Creates a project.

        Args:
            name: a valid project name.
            contact: a phone number with format "+X (XXX) XXX-XXXX" or email.
            contactMethod: PHONE or EMAIL.
            description: a project description.
            isOpen: whether to make the project open to others on the platform.
            userRoles: list who is an admin, editor, and viewer.
            groupRoles: list who is an admin, editor, and viewer.
            files: list of files locally to upload.

        Returns:
            project: the resulting project or None if error.
        '''
        project = self._gql(q.mutation_createProject, locals())
        if not project:
            return
        self._upload_files(project['id'], files)
        return self.node(project['id'])

    def _upload_files(self, projectId, files):
        with Pool(cpu_count()) as p:
            args = [(self.endpoint, self.token, projectId, f) for f in files]
            p.starmap(_upload_file, args)

    def deleteFile(self, projectId, fileName):
        '''Deletes `filename` from `projectId`.'''
        return self._gql(q.mutation_deleteFile, locals())

    def deleteProject(self, projectId):
        '''Deletes project `projectId`.'''
        return self._gql(q.mutation_deleteProject, locals())

    def deleteOauth2Client(self, id):
        '''Deletes OAuth2 Client with id `id`.'''
        return self._gql(q.mutation_deleteOauth2Client, locals())

    def exchangeOauth2CodeForToken(self, code):
        '''Exchanges an OAuth2 code for a token.'''
        return self._gql(q.mutation_exchangeOauth2CodeForToken, locals())

    def exchangeOauth2CodeWithPkceForToken(self, code, codeVerifier):
        '''Exchanges an OAuth2 code and code verifier for a token.'''
        return self._gql(q.mutation_exchangeOauth2CodeForToken, locals())

    def revokeOauth2Token(self, token):
        '''Revokes an OAuth2 token (used by clients).'''
        return self._gql(q.mutation_revokeOauth2Token, locals())

    def revokePersonalTokens(self, token):
        '''Revokes a Personal Tokens.'''
        return self._gql(q.mutation_revokePersonalToken, locals())

    def unauthorizeOauth2Client(self, id):
        '''Unauthorizes an OAuth2 client by id.'''
        return self._gql(q.mutation_unauthorizeOauth2Client, locals())

    def update_group(
        self,
        id,
        name=None,
        contactMethod=None,
        contact=None,
        description=None,
        userRoles=None,
    ):
        '''Updates a group.

        Args:
            id: id of group to update.
            name: a valid group name.
            contact: a phone number with format "+X (XXX) XXX-XXXX" or email.
            contactMethod: PHONE or EMAIL.
            description: a group description.
            userRoles: list admins and members.

        Returns:
            group: the resulting group.
        '''
        group = self.node(id)
        d = {k: v for k, v in locals().items() if k != 'self' and v}
        group.update(d)
        return self._gql(q.mutation_updateGroup, group)

    def updateOauth2Client(
        self,
        id,
        name=None,
        contact=None,
        contactMethod=None,
        description=None,
        scopes=None,
        redirectUris=None,
        pkceRequired=None,
    ):
        '''Creates an OAuth2 Client (plugin).'''
        client = self.node(id)
        d = {k: v for k, v in locals().items() if k != 'self' and v}
        client.update(d)
        return self._gql(q.mutation_updateOauth2Client, client)

    def updateProject(
        self,
        id,
        name=None,
        contact=None,
        contactMethod=None,
        description=None,
        isOpen=None,
        userRoles=None,
        groupRoles=None,
        files=[],
    ):
        '''Updates a project.

        Args:
            id: id of project to update.
            name: a valid project name.
            contact: a phone number with format "+X (XXX) XXX-XXXX" or email.
            contactMethod: PHONE or EMAIL.
            description: a project description.
            isOpen: whether to make the project open to others on the platform.
            userRoles: list who is an admin, editor, and viewer.
            groupRoles: list who is an admin, editor, and viewer.
            files: list of files locally to upload.

        Returns:
            project: the resulting project.
        '''
        project = self.node(id)
        d = {k: v for k, v in locals().items() if k != 'self' and v}
        project.update(d)
        return self._gql(q.mutation_updateOauth2Client, project)

    def updateUser(
        self,
        id,
        name=None,
        contact=None,
        contactMethod=None,
    ):
        '''Updates a user.

        Args:
            id: id of user to update.
            name: a valid user name.
            contact: a phone number with format "+X (XXX) XXX-XXXX" or email.
            contactMethod: PHONE or EMAIL.

        Returns:
            user: the resulting user.
        '''
        project = self.get_project(id)
        d = {k: v for k, v in locals().items() if k != 'self' and v}
        project.update(d)
        return self._gql(q.mutation_updateOauth2Client, project)

    # python SDK convenience functions

    def download_to_file(self, projectId, filename, output_dir=None):
        '''Downloads `filename` in project `projectId` to `output_dir`.

        Args:
            projectId: the id of a Big Local News project.
            filename: the name of a file in the project.
            output_dir: uses current working directory if not specified.

        Returns:
            ouput_path: location where file was saved or None if error.
        '''
        if not output_dir:
            output_dir = os.getcwd()
        uri = self.createFileDownloadUri(projectId, filename)
        if not uri:
            return
        with requests.get(uri.uri, stream=True) as r:
            if r.status_code != requests.codes.ok:
                return perr(responses[r.status_code])
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            return output_path

    def upload_from_json(self, json_path):
        '''Uploads groups and projects from a json config.

        See example_config.json for an example.
        '''
        path = os.path.expanduser(json_path)
        if not os.path.exists(path):
            return perr(f'invalid json_path: {path}')
        with open(path) as f:
            data = json.load(f)
        if 'groups' in data:
            for group in data['groups']:
                if 'id' in group:
                    self.create_group(**group)
                else:
                    self.update_group(**group)
        if 'projects' in data:
            for project in data['projects']:
                if 'id' in project:
                    self.update_project(**project)
                else:
                    self.create_project(**project)

    def to_pandas_df(self, projectId, filename):
        '''Returns a pandas dataframe of `filename` in project `projectId`.'''
        uri = self.createFileDownloadUri(projectId, filename)
        if not uri:
            return
        raise NotImplementedError('Not ready yet!')

    def from_pandas_df(self, df, projectId, filename):
        '''Uploads a pandas dataframe to project `projectId` as `filename`.'''
        uri = self.createFileUploadUri(projectId, filename)
        if not uri:
            return
        raise NotImplementedError('Not ready yet!')


def _gql(
    endpoint,
    token,
    query_string,
    variables={},
    operation_name=None,
):
    data = {
        'query': query_string,
        'variables': {
            'input': variables
        },
        'operation_name': operation_name,
    }
    headers = {'Authorization': f'JWT {token}'}
    res = requests.post(endpoint, json=data, headers=headers)
    if res.status_code != requests.codes.ok:
        return None, responses[res.status_code]
    return _ungraphql(res.json()), None


def _ungraphql(root):
    if isinstance(root, dict) and 'data' in root:
        return _ungraphql(root['data'])
    if isinstance(root, dict) and 'user' in root:
        return _ungraphql(root['user'])
    if isinstance(root, dict) and 'node' in root:
        return _ungraphql(root['node'])
    if isinstance(root, dict) and 'edges' in root:
        return _ungraphql(root['edges'])
    if isinstance(root, dict):
        d = {}
        for k, v in root.items():
            d[k] = _ungraphql(v)
        return d
    if isinstance(root, list):
        return [_ungraphql(item) for item in root]
    return root


def _upload_file(endpoint, token, projectId, path):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return perr(f'invalid path: {path}')
    uri, err = _get_upload_uri(endpoint, token, projectId, path)
    if err:
        return err
    err = _put(path, uri['uri'])
    if err:
        return err


def _get_upload_uri(endpoint, token, projectId, path):
    fname = os.path.basename(path)
    data = _gql(endpoint, token, q.mutation_createFileUploadUri, {
        'projectId': projectId,
        'fileName': fname
    })['createFileUploadUri']
    if data['err']:
        return None, data['err']
    return data['ok'], None


def _put(path, uri):
    headers = {
        'content-type': 'application/octet-stream',
        'host': 'storage.googleapis.com',
    }
    with open(path, 'rb') as f:
        res = requests._put(uri, data=f, headers=headers)
        if res.status_code != requests.codes.ok:
            return responses[res.status_code]


def perr(msg, end='\n'):
    print(msg, file=sys.stderr, end=end)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog=argv[0],
        description='Big Local News Python Client',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('json_path',
                        help='json config; see example test_projects.json')
    parser.add_argument('token', help='personal token')
    parser.add_argument('-tier', default='dev', help='tier to send to')
    return parser.parse_args(argv[1:])


if __name__ == '__main__':
    args = parse_args(sys.argv)
    client = Client(args.token, args.tier)
    client.upload_from_json(args.json_path)
