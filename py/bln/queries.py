query_user_names = '''
query UserNames {
    userNames
}
'''

query_group_names = '''
query UserNames {
    groupNames
}
'''

data_user = '''
id
name
displayName
contactMethod
contactMethod
'''

query_user = f'''
query {{
    user {{
        {data_user}
    }}
}}
'''

mutation_update_user = f'''
mutation UpdateUser($input: UpdateUserInput!) {{
    updateUser(input: $input) {{
        ok {{
            {data_user}
        }}
        err
    }}
}}
'''

data_group = '''
id
updatedAt
name
contactMethod
contact
description
userRoles {
  edges {
    node {
      id
      role
      user {
        id
        name
        contactMethod
        contact
      }
    }
  }
}
'''

data_project = '''
id
updatedAt
name
contactMethod
contact
description
isOpen
userRoles {
  edges {
    node {
      id
      role
      user {
        id
        name
        contactMethod
        contact
      }
    }
  }
}
groupRoles {
  edges {
    node {
      id
      role
      group {
        id
        name
        contactMethod
        contact
      }
    }
  }
}
effectiveUserRoles {
  edges {
    node {
      id
      role
      user {
        id
        name
        contactMethod
        contact
      }
    }
  }
}
files {
  name
  uri
  updatedAt
}
'''

query_open_projects = f'''
query {{
    openProjects {{
        edges {{
            node {{
                {data_project}
            }}
        }}
    }}
}}
'''

query_node = f'''
query Node($id: ID!) {{
    node(id: $id) {{
        ... on Group {{
            {data_group}
        }}
        ... on Project {{
            {data_project}
        }}
    }}
}}
'''

query_effective_project_roles = f'''
query {{
    user {{
        id
        effectiveProjectRoles {{
            edges {{
                node {{
                    id
                    role
                    project {{
                        {data_project}
                    }}
                }}
            }}
        }}
    }}
}}
'''

query_group_roles = f'''
query {{
    user {{
        id
        groupRoles {{
            edges {{
                node {{
                    id
                    role
                    group {{
                        {data_group}
                    }}
                }}
            }}
        }}
    }}
}}
'''

query_personal_tokens = '''
query {
    user {
        id
        personalTokens {
            edges {
                node {
                    id
                    token
                }
            }
        }
    }
}
'''

query_oauth2_clients = '''
query {
    user {
        id
        oauth2Clients {
            edges {
                node {
                    id
                    name
                    description
                }
            }
        }
    }
}
'''

query_oauth2_codes = '''
query {
    user {
        id
        oauth2Codes {
            edges {
                node {
                    id
                    scopes
                    client {
                        id
                        name
                        description
                    }
                }
            }
        }
    }
}
'''

query_oauth2_tokens = '''
query {
    user {
        id
        oauth2Tokens {
            edges {
                node {
                    id
                    scopes
                    client {
                        id
                        name
                        description
                    }
                }
            }
        }
    }
}
'''

mutation_create_project = f'''
mutation CreateProject($input: CreateProjectInput!) {{
    createProject(input: $input) {{
        ok {{
            {data_project}
        }}
        err
    }}
}}
'''

mutation_update_project = f'''
mutation UpdateProject($input: UpdateProjectInput!) {{
    updateProject(input: $input) {{
        ok {{
            {data_project}
        }}
        err
    }}
}}
'''

mutation_create_group = f'''
mutation CreateGroup($input: CreateGroupInput!) {{
    createGroup(input: $input) {{
        ok {{
            {data_group}
        }}
        err
    }}
}}
'''

mutation_update_group = f'''
mutation UpdateGroup($input: UpdateGroupInput!) {{
    updateGroup(input: $input) {{
        ok {{
            {data_group}
        }}
        err
    }}
}}
'''

mutation_create_personal_token = '''
mutation CreatePersonalToken {
    createPersonalToken {
        ok
        err
    }
}
'''

mutation_revoke_personal_token = '''
mutation RevokePersonalToken($input: RevokeTokenInput!) {
    revokePersonalToken(input: $input) {
        ok
        err
    }
}
'''

mutation_create_file_upload_uri = '''
mutation CreateFileUploadURI($input: FileURIInput!) {
    createFileUploadUri(input: $input) {
        ok {
            name
            uri
        }
        err
    }
}
'''

mutation_create_file_download_uri = '''
mutation CreateFileDownloadURI($input: FileURIInput!) {
    createFileDownloadUri(input: $input) {
        ok {
            name
            uri
        }
        err
    }
}
'''

mutation_delete_file = '''
mutation DeleteFile($input: FileURIInput!) {
    deleteFile(input: $input) {
        ok {
            name
        }
        err
    }
}
'''

mutation_delete_project = '''
mutation DeleteProject($input: DeleteProjectInput!) {
    deleteProject(input: $input) {
        ok
        err
    }
}
'''

data_oauth2_client_public = '''
id
name
contactMethod
contact
description
scopes
author {
    name
    contactMethod
    contact
}
'''

data_oauth2_client_private = f'''
{data_oauth2_client_public}
secret
pkceRequired
scopes
redirectUris
defaultRedirectUri
oauth2Codes {{
    edges {{
        node {{
            code
            challenge
            scopes
            user {{
                name
                contactMethod
                contact
            }}
        }}
    }}
}}
oauth2Tokens {{
    edges {{
        node {{
            token
            scopes
            user {{
                name
                contactMethod
                contact
            }}
        }}
    }}
}}
'''

query_oauth2_clients_public = f'''
query {{
    oauth2Clients {{
        {data_oauth2_client_public}
    }}
}}
'''

mutation_create_oauth2_client = f'''
mutation CreateOAuth2Client($input: CreateOAuth2ClientInput!) {{
    createOauth2Client(input: $input) {{
        ok {{
            {data_oauth2_client_private}
        }}
        err
    }}
}}
'''

mutation_update_oauth2_client = f'''
mutation UpdateOAuth2Client($input: UpdateOAuth2ClientInput!) {{
    updateOauth2Client(input: $input) {{
        ok {{
            {data_oauth2_client_private}
        }}
        err
    }}
}}
'''

mutation_delete_oauth2_client = '''
mutation DeleteOAuth2Client($input: DeleteOAuth2ClientInput!) {
    deleteOauth2Client(input: $input) {
        ok
        err
    }
}
'''

mutation_create_new_oauth2_client_secret = f'''
mutation CreateNewOAuth2ClientSecret(
    $input: CreateNewOAuth2ClientSecretInput!
) {{
    createNewOauth2ClientSecret(input: $input) {{
        ok {{
            {data_oauth2_client_private}
        }}
        err
    }}
}}
'''

mutation_authorize_oauth2_client = '''
mutation AuthorizeOAuth2Client($input: AuthorizeOAuth2ClientInput!) {
    authorizeOauth2Client(input: $input) {
        ok
        err
    }
}
'''

mutation_authorize_with_pkce_oauth2_client = '''
mutation AuthorizeWithPKCEOAuth2Client(
    $input: AuthorizeWithPKCEOAuth2ClientInput!
) {
    authorizeWithPkceOauth2Client(input: $input) {
        ok
        err
    }
}
'''

mutation_unauthorize_oauth2_client = '''
mutation UnauthorizeOAuth2Client (
    $input: UnauthorizeOAuth2ClientInput!
) {
    unauthorizeOauth2Client(input: $input) {
        ok
        err
    }
}
'''

mutation_exchange_oauth2_code_for_token = '''
mutation ExchangeOAuth2CodeForToken($input: ExchangeOAuth2CodeForTokenInput!) {
    exchangeOauth2CodeForToken(input: $input) {
        ok
        err
    }
}
'''

mutation_exchange_oauth2_code_with_pkce_for_token = '''
mutation ExchangeOAuth2CodeWithPKCEForToken(
    $input: ExchangeOAuth2CodeWithPKCEForTokenInput!
) {
    exchangeOauth2CodeWithPkceForToken(input: $input) {
        ok
        err
    }
}
'''

mutation_revoke_oauth2_token = '''
mutation RevokeOAuth2Token($input: RevokeTokenInput!) {
    revokeOauth2Token(input: $input) {
        ok
        err
    }
}
'''
