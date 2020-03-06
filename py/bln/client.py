#!/usr/bin/env python3
'''Big Local News Python Client.'''
from multiprocessing import Pool, cpu_count
from http.client import responses
import argparse
import json
import os
import re
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
        # special case: node query, which doesn't use an *Input type
        is_node = len(variables) == 1 and 'id' in variables
        if not is_node:
            # other than node, only mutations use variables, and they all have
            # *Input object types, so nest variables inside 'input'; also,
            # remove 'self' so mutations can just pass 'locals()'
            variables = {
                'input': {k: v
                          for k, v in variables.items() if k != 'self'}
            }
        data, err = _gql(self.endpoint, self.token, query, variables)
        # network error
        if err:
            return perr(err)
        if isinstance(data, dict):
            for k, v in data.items():
                # unwrap single-item dict lists
                if len(data) == 1 and isinstance(v, list):
                    return v
                if isinstance(v, dict):
                    # mutation error
                    if 'err' in v and v['err']:
                        return perr(v['err'])
                    # mutation result
                    if 'ok' in v:
                        return v['ok']
        # query result
        return data

    def raw(self, query, variables={}, ungraphql=False):
        '''Execute a raw query directly with variables.'''
        data, err = _gql(self.endpoint, self.token, query, variables,
                         ungraphql)
        if err:
            return perr(err)
        return data

    def everything(self):
        '''Returns all information accessible by the current user.'''
        return self._gql(q.query_everything)

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

    def createGroup(
        self,
        name,
        contact,
        contactMethod='EMAIL',
        description='',
        userRoles=None,
    ):
        '''Creates a group.

        Args:
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
        variables = {k: v for k, v in locals().items() if k != 'files'}
        project = self._gql(q.mutation_createProject, variables)
        if not project:
            return
        self._upload_files(project['id'], files)
        return self._gql(q.query_project, {'id': project['id']})

    def _upload_files(self, projectId, files):
        with Pool(cpu_count()) as p:
            args = [(self.endpoint, self.token, projectId, f) for f in files]
            p.starmap(_upload_file, args)

    def deleteFile(self, projectId, fileName):
        '''Deletes `filename` from `projectId`.'''
        return self._gql(q.mutation_deleteFile, locals())

    def deleteProject(self, id):
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

    def updateGroup(
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
        group = self._gql(q.query_group, {'id': id})
        if not group:
            return
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
        client = self._gql(q.query_oauth2Client, {'id': id})
        if not client:
            return
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
        project = self._gql(q.query_project, {'id': id})
        if not project:
            return
        d = {k: v for k, v in locals().items() if k != 'self' and v}
        project.update(d)
        return self._gql(q.mutation_updateOauth2Client, project)

    def updateUser(
        self,
        id,
        name=None,
        displayName=None,
        contact=None,
        contactMethod=None,
    ):
        '''Updates a user.

        Args:
            id: id of user to update.
            name: a valid user name.
            displayName: display name of user.
            contact: a phone number with format "+X (XXX) XXX-XXXX" or email.
            contactMethod: PHONE or EMAIL.

        Returns:
            user: the resulting user.
        '''
        user = self._gql(q.query_user, {'id': id})
        if not user:
            return
        d = {k: v for k, v in locals().items() if k != 'self' and v}
        user.update(d)
        return self._gql(q.mutation_updateUser, user)

    # python SDK convenience functions

    def download_file(self, projectId, filename, output_dir=None):
        '''Downloads `filename` in project `projectId` to `output_dir`.

        Args:
            projectId: the id of a Big Local News project.
            filename: the name of a file in the project.
            output_dir: uses current working directory if not specified.

        Returns:
            ouput_path: location where file was saved or None if error.
        '''
        output_dir = os.path.expanduser(output_dir)
        if not output_dir:
            output_dir = os.getcwd()
        uri = self.createFileDownloadUri(projectId, filename)
        if not uri:
            return
        with requests.get(uri['uri'], stream=True) as r:
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

        See example_config.json.
        '''
        path = os.path.expanduser(json_path)
        if not os.path.exists(path):
            return perr(f'invalid json_path: {path}')
        with open(path) as f:
            data = json.load(f)
        if 'groups' in data:
            for group in data['groups']:
                if 'id' in group:
                    self.createGroup(**group)
                else:
                    self.updateGroup(**group)
        if 'projects' in data:
            for project in data['projects']:
                if 'id' in project:
                    self.updateProject(**project)
                else:
                    self.createProject(**project)

    def file_to_pandas(self, projectId, fileName):
        '''Returns a pandas DataFrame of `fileName` in project `projectId`.

        Args:
            projectId: the id of the project.
            fileName: the remote file name.

        Returns:
            df: a pandas DataFrame.
        '''
        uri = self.createFileDownloadUri(projectId, fileName)
        if not uri:
            return
        return self._uri_to_pandas(uri)

    def _uri_to_pands(self, uri):
        if _is_excel(uri['name']):
            return pd.read_excel(uri['uri'])
        # sep=None and engine='python' tells pandas to detect the type
        return pd.read_table(uri['uri'], sep=None, engine='python')

    def pandas_to_csv(self, df, projectId, fileName):
        '''Uploads a pandas DataFrame to project `projectId` as `fileName`.

        Args:
            df: a pandas DataFrame.
            projectId: the id of the project.
            fileName: the remote filename.
        '''
        if not isinstance(df, pd.DataFrame):
            return perr('Can only upload pandas DataFrames.')
        if os.path.splitext(fileName)[1] != '.csv':
            return perr('Must upload to a file with a csv extension.')
        uri = self.createFileUploadUri(projectId, fileName)
        if not uri:
            return
        return _put_string(df.to_csv(index=False), uri['uri'])

    def search_groups(self, predicate=lambda g: re.match('.*', g['name'])):
        '''Returns groups where `predicate(group)` is True.

        Args:
            predicate: (optional) a function that takes a group and returns
                True or False, i.e. if `predicate(group)` returns True, the
                group is added to the result list.

        Returns:
            groups: list of groups where `predicate(group)` is true.
        '''
        groups = []
        for v in self.groupRoles():
            if predicate(v['group']):
                groups.append(v['group'])
        return groups

    def search_projects(self, predicate=lambda p: re.match('.*', p['name'])):
        '''Returns projects where `predicate(project)` is True.

        Args:
            predicate: (optional) a function that takes a project and returns
                True or False, i.e. if `predicate(project)` returns True, the
                project is added to the result list.

        Returns:
            projects: list of projects where `predicate(project)` is true.
        '''
        projects = []
        for v in self.effectiveProjectRoles():
            if predicate(v['project']):
                projects.append(v['project'])
        return projects

    def search_files(self, predicate=lambda f: re.match('.*', f['name'])):
        '''Returns projects where `predicate(file)` is True.

        Args:
            predicate: (optional) a function that takes a file object and
                returns True or False, i.e. if `predicate(file_obj)` returns
                True, the file object is added to the result list. File objects
                are the graphql File type with projectId and projectName added
                for convenience.

        Returns:
            files: list of file objects where `predicate(file_obj)` is true.
        '''
        files = []
        for v in self.effectiveProjectRoles():
            for f in v['project']['files']:
                if predicate(f):
                    f['projectId'] = v['project']['id']
                    f['projectName'] = v['project']['name']
                    files.append(f)
        return files

    def search_to_pandas(
        self,
        file_predicate=lambda f: re.match('.*', f['name']),
        project_predicate=lambda p: re.match('.*', p['name']),
    ):
        '''Returns matching project/file name regex to pandas DataFrame.

        Args:
            file_predicate: (optional) a function that takes a File object and
                returns True or False.
            project_predicate: (optional) a function that takes a project and
                returns True or False.

            The for those files that match both the `file_predicate` and
            the `project_predicate`, the user is asked to select one to load
            into pandas.

        Returns:
            df: a pandas DataFrame.
        '''
        uris = []
        for v in self.effectiveProjectRoles():
            if project_predicate(v['project']):
                for f in v['project']['files']:
                    if file_predicate(f):
                        f['projectId'] = v['project']['id']
                        f['projectName'] = v['project']['name']
                        uris.append(f)
        if not uris:
            return perr('No matching files')
        idx = _select_idx([uri['name'] for uri in uris])
        uri = dict(enumerate(uris))[idx]
        return self._uri_to_pands(uri)


def _gql(
    endpoint,
    token,
    query_string,
    variables={},
    ungraphql=True,
):
    inpt = {'query': query_string, 'variables': variables}
    headers = {'Authorization': f'JWT {token}'}
    res = requests.post(endpoint, json=inpt, headers=headers)
    if res.status_code != requests.codes.ok:
        return None, responses[res.status_code]
    data = res.json()
    if ungraphql:
        data = _ungraphql(data)
    return data, None


def _ungraphql(root):
    # unwraps levels that are simply (id, <item>: <value>) to just <value>
    if isinstance(root, dict) and 'id' in root and len(root) == 2:
        for k, v in root.items():
            if k != 'id':
                return _ungraphql(v)
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
        res = requests.put(uri, data=f, headers=headers)
        if res.status_code != requests.codes.ok:
            return responses[res.status_code]


def _put_string(string, uri):
    headers = {
        'content-type': 'application/octet-stream',
        'host': 'storage.googleapis.com',
    }
    res = requests.put(uri, data=string.encode('utf-8'), headers=headers)
    if res.status_code != requests.codes.ok:
        return responses[res.status_code]


def _is_excel(filename):
    return os.path.splitext(filename)[1] in ['.xls', '.xlsx']


def _select_idx(options):
    for idx, option in enumerate(options):
        print(f'{idx}: {option}')
    msg = 'Select index: '
    idx = _to_idx(input(msg))
    while idx < 0 or idx >= len(options):
        idx = _to_idx(input(msg))
    return idx


def _to_idx(s):
    try:
        return int(s)
    except Exception:
        return -1


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
    parser.add_argument('-tier', default='prod', help='tier to send to')
    return parser.parse_args(argv[1:])


if __name__ == '__main__':
    args = parse_args(sys.argv)
    client = Client(args.token, args.tier)
    client.upload_from_json(args.json_path)
