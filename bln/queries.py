# FRAGMENTS
fragment_user = """
id
username
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
tags {{
    edges {{
        node {{
            id
            tag {{
                id
                name
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

# MUTATIONS

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

mutation_revokePersonalToken = """
mutation RevokePersonalToken($input: RevokeTokenInput!) {
    revokePersonalToken(input: $input) {
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
