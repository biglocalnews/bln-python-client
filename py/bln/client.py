#!/usr/bin/env python3
'''Big Local News Python Client.'''
from multiprocessing import Pool, cpu_count
from http.client import responses
import argparse
import json
import os
import sys

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

    def get_download_link(self, projectId, filename):
        '''Returns download link for `filename` in project `projectId`.

        Args:
            projectId: the id of a Big Local News project.
            filename: the name of a file in the project.

        Returns:
            uri: a download link or None if error.
        '''
        uri, err = _get_download_uri(self.endpoint, self.token, projectId,
                                     filename)
        if err:
            return perr(err)
        return uri

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
        uri, err = _get_download_uri(self.endpoint, self.token, projectId,
                                     filename)
        if err:
            return perr(err)
        with requests.get(uri, stream=True) as r:
            if r.status_code != requests.codes.ok:
                return perr(responses[r.status_code])
            output_path = os.path.join(output_dir, filename)
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            return output_path

    def get_upload_link(self, projectId, filename):
        '''Returns upload link for `filename` in project `projectId`.

        Args:
            projectId: the id of a Big Local News project.
            filename: the name of a file in the project.

        Returns:
            uri: an upload link or None if error.
        '''
        uri, err = _get_upload_uri(self.endpoint, self.token, projectId,
                                   filename)
        if err:
            return perr(err)
        return uri

    def get_effective_project_roles(self):
        '''Returns [{'role': ..., 'project': ... }, ...] or None if error.'''
        res, err = _gql(self.endpoint, self.token,
                        q.query_effective_project_roles)
        if err:
            return perr(err)
        edges = res['effectiveProjectRoles']
        return [(e['role'], e['project']) for e in edges]

    def get_project_roles(self):
        '''Returns [{'role': ..., 'project': ... }, ...] or None if error.'''
        res, err = _gql(self.endpoint, self.token, q.query_project_roles)
        if err:
            return perr(err)
        edges = res['projectRoles']
        return [(e['role'], e['project']) for e in edges]

    def get_group_roles(self):
        '''Returns [{'role': ..., 'group': ... }, ...] or None if error.'''
        res, err = _gql(self.endpoint, self.token, q.query_group_roles)
        if err:
            return perr(err)
        edges = res['groupRoles']
        return [(e['role'], e['group']) for e in edges]

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

    def create_project(
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
        return self._upsert_project(
            name,
            contact,
            contactMethod,
            description,
            isOpen,
            userRoles,
            groupRoles,
            files,
        )

    def _upsert_project(
        self,
        name,
        contact,
        contactMethod,
        description,
        isOpen,
        userRoles,
        groupRoles,
        files,
        id=None,
    ):
        perr(f'Uploading Project "{name}"...')
        key = 'createProject'
        query = q.mutation_create_project
        variables = {
            'name': name,
            'contactMethod': contactMethod,
            'contact': contact,
            'description': description,
            'isOpen': isOpen,
            'userRoles': userRoles,
            'groupRoles': groupRoles,
        }
        if id:
            key = 'updateProject'
            query = q.mutation_update_project
            variables['id'] = id
        res, err = _gql(self.endpoint, self.token, query, variables)
        if err:
            return perr(err)
        data = res[key]
        if data['err']:
            return perr(data['err'])
        projectId = data['ok']['id']
        with Pool(cpu_count()) as p:
            args = [(self.endpoint, self.token, projectId, f) for f in files]
            p.starmap(_upload, args)
        perr('Done.')
        project, err = self.get_project(projectId)
        if err:
            return perr(err)
        return project

    def update_project(
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
        project = self.get_project(id)
        if not project:
            return
        if name:
            project['name'] = name
        if contactMethod:
            project['contactMethod'] = contactMethod
        if contact:
            project['contact'] = contact
        if description:
            project['description'] = description
        if userRoles:
            project['userRoles'] = userRoles
        if groupRoles:
            project['groupRoles'] = groupRoles
        return self._upsert_project(
            name,
            contact,
            contactMethod,
            description,
            isOpen,
            userRoles,
            groupRoles,
            files,
            id,
        )

    def get_project(self, id):
        '''Returns a project or None if error.'''
        data, err = self._get_node(id)
        if err:
            return perr(err)
        return data

    def _get_node(self, id):
        res, err = _gql(self.endpoint, self.token, q.query_node, {
            'id': id,
        })
        if err:
            return None, err
        return res['data'], None

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
        return self._upsert_group(
            self,
            name,
            contactMethod,
            contact,
            description,
            userRoles,
        )

    def _upsert_group(
        self,
        name,
        contactMethod,
        contact,
        description,
        userRoles,
        id=None,
    ):
        perr(f'Uploading group "{name}"...')
        key = 'createGroup'
        query = q.mutation_create_group
        variables = {
            'name': name,
            'contactMethod': contactMethod,
            'contact': contact,
            'description': description,
            'userRoles': userRoles,
        }
        if id:
            key = 'updateGroup'
            query = q.mutation_update_group
            variables['id'] = id
        data = _gql(self.endpoint, self.token, query, variables)['data'][key]
        if data['err']:
            return perr(data['err'])
        perr('Done.')
        return data['ok']

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
        group = self.get_group(id)
        if not group:
            return
        if name:
            group['name'] = name
        if contactMethod:
            group['contactMethod'] = contactMethod
        if contact:
            group['contact'] = contact
        if description:
            group['description'] = description
        if userRoles:
            group['userRoles'] = userRoles
        return self._upsert_group(
            self,
            name,
            contactMethod,
            contact,
            description,
            userRoles,
            id,
        )

    def get_group(self, id):
        '''Returns a group or None if error.'''
        data, err = self._get_node(id)
        if err:
            return perr(err)
        return data


def _upload(endpoint, token, projectId, path):
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return perr(f'invalid path: {path}')
    upload, err = _get_upload_uri(endpoint, token, projectId, path)
    if err:
        return err
    err = _put(path, upload['uri'])
    if err:
        return err


def _get_upload_uri(endpoint, token, projectId, path):
    fname = os.path.basename(path)
    data = _gql(endpoint, token, q.mutation_create_file_upload_uri, {
        'projectId': projectId,
        'fileName': fname
    })['createFileUploadUri']
    if data['err']:
        return None, data['err']
    return data['ok'], None


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
    print(res.json())
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


def _put(path, uri):
    headers = {
        'content-type': 'application/octet-stream',
        'host': 'storage.googleapis.com',
    }
    with open(path, 'rb') as f:
        res = requests._put(uri, data=f, headers=headers)
        if res.status_code != requests.codes.ok:
            return responses[res.status_code]


def _get_download_uri(endpoint, token, projectId, filename):
    res, err = _gql(endpoint, token, q.mutation_create_file_download_uri, {
        'projectId': projectId,
        'fileName': filename
    })
    if err:
        return perr(err)
    data = res['createFileDownloadUri']
    if data['err']:
        return None, data['err']
    return data['ok'], None


def perr(msg):
    print(msg, file=sys.stderr)


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
