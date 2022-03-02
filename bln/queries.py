# FRAGMENTS
fragment_user = """
id
name
displayName
contactMethod
contact
"""

fragment_group = f"""
id
updatedAt
name
contactMethod
contact
description
userRoles {{
    edges {{
        node {{
            id
            role
            user {{
                {fragment_user}
            }}
        }}
    }}
}}
"""

fragment_group_public = """
id
name
contactMethod
contact
"""

fragment_file = """
id
name
createdAt
updatedAt
size
md5
tags {
    edges {
        node {
            id
            tag {
                id
                name
            }
        }
    }
}
"""

fragment_project = f"""
id
updatedAt
name
contactMethod
contact
description
isOpen
userRoles {{
    edges {{
        node {{
            id
            role
            user {{
                {fragment_user}
            }}
        }}
    }}
}}
groupRoles {{
    edges {{
        node {{
            id
            role
            group {{
                {fragment_group_public}
            }}
        }}
    }}
}}
effectiveUserRoles {{
    edges {{
        node {{
            id
            role
            user {{
                {fragment_user}
            }}
        }}
    }}
}}
files {{
    edges {{
        node {{
            {fragment_file}
        }}
    }}
}}
"""

fragment_oauth2_client_public = f"""
id
name
contactMethod
contact
description
scopes
author {{
    {fragment_user}
}}
"""

fragment_oauth2_client_private = f"""
{fragment_oauth2_client_public}
secret
pkceRequired
scopes
redirectUris
defaultRedirectUri
oauth2Codes {{
    edges {{
        node {{
            id
            code
            challenge
            scopes
            user {{
                {fragment_user}
            }}
        }}
    }}
}}
oauth2Tokens {{
    edges {{
        node {{
            id
            token
            scopes
            user {{
                {fragment_user}
            }}
        }}
    }}
}}
"""

# QUERIES

query_everything = f"""
query {{
    user {{
        {fragment_user}
        groupRoles {{
            edges {{
                node {{
                    id
                    role
                    group {{
                        {fragment_group}
                    }}
                }}
            }}
        }}
        projectRoles {{
            edges {{
                node {{
                    id
                    role
                    project {{
                        {fragment_project}
                    }}
                }}
            }}
        }}
        effectiveProjectRoles {{
            edges {{
                node {{
                    id
                    role
                    project {{
                        {fragment_project}
                    }}
                }}
            }}
        }}
        personalTokens {{
            edges {{
                node {{
                    id
                    token
                }}
            }}
        }}
        oauth2Codes {{
            edges {{
                node {{
                    id
                    code
                    expiresAt
                    scopes
                    client {{
                        {fragment_oauth2_client_public}
                    }}
                }}
            }}
        }}
        oauth2Tokens {{
            edges {{
                node {{
                    id
                    token
                    scopes
                    client {{
                        {fragment_oauth2_client_public}
                    }}
                }}
            }}
        }}
        oauth2Clients {{
            edges {{
                node {{
                    {fragment_oauth2_client_private}
                }}
            }}
        }}
    }}
}}
"""

query_user = f"""
query {{
    user {{
        {fragment_user}
    }}
}}
"""

query_group = f"""
query Node($id: ID!) {{
    node(id: $id) {{
        ... on Group {{
            {fragment_group}
    }}
}}
"""

query_project = f"""
query Node($id: ID!) {{
    node(id: $id) {{
        ... on Project {{
            {fragment_project}
        }}
    }}
}}
"""

query_oauth2Client = f"""
query Node($id: ID!) {{
    node(id: $id) {{
        ... on OAuth2Client {{
            {fragment_oauth2_client_private}
        }}
    }}
}}
"""

query_oauth2ClientPublic = f"""
query Node($id: ID!) {{
    node(id: $id) {{
        ... on OAuth2Client {{
            {fragment_oauth2_client_public}
        }}
    }}
}}
"""

query_groupRoles = f"""
query {{
    user {{
        id
        groupRoles {{
            edges {{
                node {{
                    id
                    role
                    group {{
                        {fragment_group}
                    }}
                }}
            }}
        }}
    }}
}}
"""

query_projectRoles = f"""
query {{
    user {{
        id
        projectRoles {{
            edges {{
                node {{
                    id
                    role
                    project {{
                        {fragment_project}
                    }}
                }}
            }}
        }}
    }}
}}
"""

query_effectiveProjectRoles = f"""
query {{
    user {{
        id
        effectiveProjectRoles {{
            edges {{
                node {{
                    id
                    role
                    project {{
                        {fragment_project}
                    }}
                }}
            }}
        }}
    }}
}}
"""

query_personalTokens = """
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
"""

query_oauth2Codes = f"""
query {{
    user {{
        id
        oauth2Codes {{
            edges {{
                node {{
                    id
                    code
                    expiresAt
                    scopes
                    client {{
                        {fragment_oauth2_client_public}
                    }}
                }}
            }}
        }}
    }}
}}
"""

query_oauth2Tokens = f"""
query {{
    user {{
        id
        oauth2Tokens {{
            edges {{
                node {{
                    id
                    token
                    scopes
                    client {{
                        {fragment_oauth2_client_public}
                    }}
                }}
            }}
        }}
    }}
}}
"""

query_oauth2Clients = f"""
query {{
    user {{
        id
        oauth2Clients {{
            edges {{
                node {{
                    {fragment_oauth2_client_private}
                }}
            }}
        }}
    }}
}}
"""

query_userNames = """
query {
    userNames
}
"""

query_groupNames = """
query {
    groupNames
}
"""

query_openProjects = f"""
query {{
    openProjects {{
        edges {{
            node {{
                {fragment_project}
            }}
        }}
    }}
}}
"""

query_oauth2ClientsPublic = f"""
query {{
    oauth2Clients {{
        {fragment_oauth2_client_public}
    }}
}}
"""

# MUTATIONS

mutation_authorizeOauth2Client = """
mutation AuthorizeOAuth2Client($input: AuthorizeOAuth2ClientInput!) {
    authorizeOauth2Client(input: $input) {
        ok
        err
    }
}
"""

mutation_authorizeWithPkceOauth2Client = """
mutation AuthorizeWithPKCEOAuth2Client(
    $input: AuthorizeWithPKCEOAuth2ClientInput!
) {
    authorizeWithPkceOauth2Client(input: $input) {
        ok
        err
    }
}
"""

mutation_createFileDownloadUri = """
mutation CreateFileDownloadURI($input: FileURIInput!) {
    createFileDownloadUri(input: $input) {
        ok {
            name
            uri
            uriType
        }
        err
    }
}
"""

mutation_createFileUploadUri = """
mutation CreateFileUploadURI($input: FileURIInput!) {
    createFileUploadUri(input: $input) {
        ok {
            name
            uri
            uriType
        }
        err
    }
}
"""

mutation_createGroup = f"""
mutation CreateGroup($input: CreateGroupInput!) {{
    createGroup(input: $input) {{
        ok {{
            {fragment_group}
        }}
        err
    }}
}}
"""

mutation_createNewOauth2ClientSecret = f"""
mutation CreateNewOAuth2ClientSecret(
    $input: CreateNewOAuth2ClientSecretInput!
) {{
    createNewOauth2ClientSecret(input: $input) {{
        ok {{
            {fragment_oauth2_client_private}
        }}
        err
    }}
}}
"""

mutation_createOauth2Client = f"""
mutation CreateOAuth2Client($input: CreateOAuth2ClientInput!) {{
    createOauth2Client(input: $input) {{
        ok {{
            {fragment_oauth2_client_private}
        }}
        err
    }}
}}
"""

mutation_createPersonalToken = """
mutation CreatePersonalToken {
    createPersonalToken {
        ok
        err
    }
}
"""

mutation_createProject = f"""
mutation CreateProject($input: CreateProjectInput!) {{
    createProject(input: $input) {{
        ok {{
            {fragment_project}
        }}
        err
    }}
}}
"""

mutation_createTag = """
mutation CreateTag($input: CreateTagInput!) {
    createTag(input: $input) {
        ok
        err
    }
}
"""

mutation_deleteFile = """
mutation DeleteFile($input: FileURIInput!) {
    deleteFile(input: $input) {
        ok
        err
    }
}
"""

mutation_deleteProject = """
mutation DeleteProject($input: DeleteProjectInput!) {
    deleteProject(input: $input) {
        ok
        err
    }
}
"""

mutation_deleteOauth2Client = """
mutation DeleteOAuth2Client($input: DeleteOAuth2ClientInput!) {
    deleteOauth2Client(input: $input) {
        ok
        err
    }
}
"""

mutation_exchangeOauth2CodeForToken = """
mutation ExchangeOAuth2CodeForToken($input: ExchangeOAuth2CodeForTokenInput!) {
    exchangeOauth2CodeForToken(input: $input) {
        ok
        err
    }
}
"""

mutation_exchangeOauth2CodeWithPkceForToken = """
mutation ExchangeOAuth2CodeWithPKCEForToken(
    $input: ExchangeOAuth2CodeWithPKCEForTokenInput!
) {
    exchangeOauth2CodeWithPkceForToken(input: $input) {
        ok
        err
    }
}
"""

mutation_revokeOauth2Token = """
mutation RevokeOAuth2Token($input: RevokeTokenInput!) {
    revokeOauth2Token(input: $input) {
        ok
        err
    }
}
"""

mutation_revokePersonalToken = """
mutation RevokePersonalToken($input: RevokeTokenInput!) {
    revokePersonalToken(input: $input) {
        ok
        err
    }
}
"""

mutation_unauthorizeOauth2Client = """
mutation UnauthorizeOAuth2Client (
    $input: UnauthorizeOAuth2ClientInput!
) {
    unauthorizeOauth2Client(input: $input) {
        ok
        err
    }
}
"""

mutation_updateGroup = f"""
mutation UpdateGroup($input: UpdateGroupInput!) {{
    updateGroup(input: $input) {{
        ok {{
            {fragment_group}
        }}
        err
    }}
}}
"""

mutation_updateOauth2Client = f"""
mutation UpdateOAuth2Client($input: UpdateOAuth2ClientInput!) {{
    updateOauth2Client(input: $input) {{
        ok {{
            {fragment_oauth2_client_private}
        }}
        err
    }}
}}
"""

mutation_updateProject = f"""
mutation UpdateProject($input: UpdateProjectInput!) {{
    updateProject(input: $input) {{
        ok {{
            {fragment_project}
        }}
        err
    }}
}}
"""

mutation_updateUser = f"""
mutation UpdateUser($input: UpdateUserInput!) {{
    updateUser(input: $input) {{
        ok {{
            {fragment_user}
        }}
        err
    }}
}}
"""
