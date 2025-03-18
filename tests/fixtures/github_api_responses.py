"""Mock GitHub API responses for testing."""

# Mock issue response
MOCK_ISSUE = {
    "url": "https://api.github.com/repos/owner/repo/issues/123",
    "repository_url": "https://api.github.com/repos/owner/repo",
    "labels_url": "https://api.github.com/repos/owner/repo/issues/123/labels{/name}",
    "comments_url": "https://api.github.com/repos/owner/repo/issues/123/comments",
    "events_url": "https://api.github.com/repos/owner/repo/issues/123/events",
    "html_url": "https://github.com/owner/repo/issues/123",
    "id": 1234567890,
    "node_id": "MDExOlB1bGxSZXF1ZXN0MTIzNDU2Nzg5MA==",
    "number": 123,
    "title": "Test Issue",
    "user": {
        "login": "testuser",
        "id": 12345,
        "node_id": "MDQ6VXNlcjEyMzQ1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12345?v=4",
        "url": "https://api.github.com/users/testuser",
        "html_url": "https://github.com/testuser",
        "type": "User",
        "site_admin": False
    },
    "labels": [
        {
            "id": 123456789,
            "node_id": "MDU6TGFiZWwxMjM0NTY3ODk=",
            "url": "https://api.github.com/repos/owner/repo/labels/bug",
            "name": "bug",
            "color": "d73a4a",
            "default": True,
            "description": "Something isn't working"
        },
        {
            "id": 987654321,
            "node_id": "MDU6TGFiZWw5ODc2NTQzMjE=",
            "url": "https://api.github.com/repos/owner/repo/labels/enhancement",
            "name": "enhancement",
            "color": "a2eeef",
            "default": True,
            "description": "New feature or request"
        }
    ],
    "state": "open",
    "locked": False,
    "assignee": {
        "login": "assignee",
        "id": 54321,
        "node_id": "MDQ6VXNlcjU0MzIx",
        "avatar_url": "https://avatars.githubusercontent.com/u/54321?v=4",
        "url": "https://api.github.com/users/assignee",
        "html_url": "https://github.com/assignee",
        "type": "User",
        "site_admin": False
    },
    "assignees": [
        {
            "login": "assignee",
            "id": 54321,
            "node_id": "MDQ6VXNlcjU0MzIx",
            "avatar_url": "https://avatars.githubusercontent.com/u/54321?v=4",
            "url": "https://api.github.com/users/assignee",
            "html_url": "https://github.com/assignee",
            "type": "User",
            "site_admin": False
        }
    ],
    "milestone": {
        "url": "https://api.github.com/repos/owner/repo/milestones/1",
        "html_url": "https://github.com/owner/repo/milestone/1",
        "labels_url": "https://api.github.com/repos/owner/repo/milestones/1/labels",
        "id": 123456,
        "node_id": "MDk6TWlsZXN0b25lMTIzNDU2",
        "number": 1,
        "title": "Test Milestone",
        "description": "Test milestone description",
        "creator": {
            "login": "testuser",
            "id": 12345,
            "node_id": "MDQ6VXNlcjEyMzQ1",
            "avatar_url": "https://avatars.githubusercontent.com/u/12345?v=4",
            "url": "https://api.github.com/users/testuser",
            "html_url": "https://github.com/testuser",
            "type": "User",
            "site_admin": False
        },
        "open_issues": 5,
        "closed_issues": 3,
        "state": "open",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-02T00:00:00Z",
        "due_on": "2023-03-01T00:00:00Z",
        "closed_at": None
    },
    "comments": 5,
    "created_at": "2023-01-15T00:00:00Z",
    "updated_at": "2023-01-16T00:00:00Z",
    "closed_at": None,
    "author_association": "OWNER",
    "body": "This is a test issue body.\n\nWith multiple paragraphs."
}

# Mock project response
MOCK_PROJECT = {
    "owner_url": "https://api.github.com/repos/owner/repo",
    "url": "https://api.github.com/projects/456",
    "html_url": "https://github.com/owner/repo/projects/1",
    "columns_url": "https://api.github.com/projects/456/columns",
    "id": 456,
    "node_id": "MDc6UHJvamVjdDQ1Ng==",
    "name": "Test Project",
    "body": "Test project description",
    "number": 1,
    "state": "open",
    "creator": {
        "login": "testuser",
        "id": 12345,
        "node_id": "MDQ6VXNlcjEyMzQ1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12345?v=4",
        "url": "https://api.github.com/users/testuser",
        "html_url": "https://github.com/testuser",
        "type": "User",
        "site_admin": False
    },
    "created_at": "2023-01-15T00:00:00Z",
    "updated_at": "2023-01-16T00:00:00Z"
}

# Mock column response
MOCK_COLUMNS = [
    {
        "url": "https://api.github.com/projects/columns/1",
        "project_url": "https://api.github.com/projects/456",
        "cards_url": "https://api.github.com/projects/columns/1/cards",
        "id": 1,
        "node_id": "MDEzOlByb2plY3RDb2x1bW4x",
        "name": "To Do",
        "created_at": "2023-01-15T00:00:00Z",
        "updated_at": "2023-01-15T00:00:00Z"
    },
    {
        "url": "https://api.github.com/projects/columns/2",
        "project_url": "https://api.github.com/projects/456",
        "cards_url": "https://api.github.com/projects/columns/2/cards",
        "id": 2,
        "node_id": "MDEzOlByb2plY3RDb2x1bW4y",
        "name": "In Progress",
        "created_at": "2023-01-15T00:00:00Z",
        "updated_at": "2023-01-15T00:00:00Z"
    },
    {
        "url": "https://api.github.com/projects/columns/3",
        "project_url": "https://api.github.com/projects/456",
        "cards_url": "https://api.github.com/projects/columns/3/cards",
        "id": 3,
        "node_id": "MDEzOlByb2plY3RDb2x1bW4z",
        "name": "Done",
        "created_at": "2023-01-15T00:00:00Z",
        "updated_at": "2023-01-15T00:00:00Z"
    }
]

# Mock milestone response
MOCK_MILESTONE = {
    "url": "https://api.github.com/repos/owner/repo/milestones/1",
    "html_url": "https://github.com/owner/repo/milestone/1",
    "labels_url": "https://api.github.com/repos/owner/repo/milestones/1/labels",
    "id": 123456,
    "node_id": "MDk6TWlsZXN0b25lMTIzNDU2",
    "number": 1,
    "title": "Test Milestone",
    "description": "Test milestone description",
    "creator": {
        "login": "testuser",
        "id": 12345,
        "node_id": "MDQ6VXNlcjEyMzQ1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12345?v=4",
        "url": "https://api.github.com/users/testuser",
        "html_url": "https://github.com/testuser",
        "type": "User",
        "site_admin": False
    },
    "open_issues": 5,
    "closed_issues": 3,
    "state": "open",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z",
    "due_on": "2023-03-01T00:00:00Z",
    "closed_at": None
}

# Mock repository response
MOCK_REPOSITORY = {
    "id": 123456789,
    "node_id": "MDEwOlJlcG9zaXRvcnkxMjM0NTY3ODk=",
    "name": "repo",
    "full_name": "owner/repo",
    "private": False,
    "owner": {
        "login": "owner",
        "id": 654321,
        "node_id": "MDQ6VXNlcjY1NDMyMQ==",
        "avatar_url": "https://avatars.githubusercontent.com/u/654321?v=4",
        "url": "https://api.github.com/users/owner",
        "html_url": "https://github.com/owner",
        "type": "User",
        "site_admin": False
    },
    "html_url": "https://github.com/owner/repo",
    "description": "Test repository",
    "fork": False,
    "url": "https://api.github.com/repos/owner/repo",
    "created_at": "2022-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z",
    "pushed_at": "2023-01-15T00:00:00Z",
    "homepage": None,
    "size": 1000,
    "stargazers_count": 10,
    "watchers_count": 10,
    "language": "Python",
    "forks_count": 5,
    "open_issues_count": 3,
    "master_branch": "main",
    "default_branch": "main",
    "topics": ["github", "api", "python"],
    "has_issues": True,
    "has_projects": True,
    "has_wiki": True,
    "has_pages": False,
    "has_downloads": True,
    "archived": False,
    "disabled": False,
    "visibility": "public",
    "license": {
        "key": "mit",
        "name": "MIT License",
        "url": "https://api.github.com/licenses/mit",
        "spdx_id": "MIT",
        "node_id": "MDc6TGljZW5zZW1pdA==",
        "html_url": "https://github.com/license/mit/"
    }
}

# Mock user response
MOCK_USER = {
    "login": "testuser",
    "id": 12345,
    "node_id": "MDQ6VXNlcjEyMzQ1",
    "avatar_url": "https://avatars.githubusercontent.com/u/12345?v=4",
    "url": "https://api.github.com/users/testuser",
    "html_url": "https://github.com/testuser",
    "type": "User",
    "site_admin": False,
    "name": "Test User",
    "company": "Test Company",
    "blog": "https://testuser.com",
    "location": "Test Location",
    "email": "test@example.com",
    "hireable": None,
    "bio": "Test bio",
    "twitter_username": "testuser",
    "public_repos": 20,
    "public_gists": 5,
    "followers": 10,
    "following": 15,
    "created_at": "2020-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
}