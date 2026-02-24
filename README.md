# Task Management System API

A RESTful API for managing organizations, projects, and issues (tasks) built with Django and Django REST Framework.

## Features

- JWT Authentication
- Role-based permissions (OWNER, MANAGER, MEMBER)
- CRUD operations for Organizations, Projects, and Issues
- Filtering, searching, and ordering for issues
- Proper business logic enforcement

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv myenv`
3. Activate the virtual environment: `myenv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the server: `python manage.py runserver`

## API Endpoints

### Authentication
- `POST /api/register/` - User registration
- `POST /api/login/` - User login (returns JWT tokens)
- `POST /api/token/refresh/` - Refresh JWT token

### Organizations
- `GET /api/organizations/` - List user's organizations
- `POST /api/organizations/` - Create organization (user becomes OWNER)
- `GET /api/organizations/{id}/` - Get organization details
- `PUT /api/organizations/{id}/` - Update organization (OWNER only)
- `DELETE /api/organizations/{id}/` - Delete organization (OWNER only)

### Memberships
- `GET /api/organizations/{org_id}/memberships/` - List organization members
- `POST /api/organizations/{org_id}/memberships/` - Add member (OWNER/MANAGER only)
- `PUT /api/organizations/{org_id}/memberships/{id}/` - Update member role
- `DELETE /api/organizations/{org_id}/memberships/{id}/` - Remove member

### Projects
- `GET /api/organizations/{org_id}/projects/` - List organization projects
- `POST /api/organizations/{org_id}/projects/` - Create project (OWNER/MANAGER only)
- `GET /api/organizations/{org_id}/projects/{id}/` - Get project details
- `PUT /api/organizations/{org_id}/projects/{id}/` - Update project
- `DELETE /api/organizations/{org_id}/projects/{id}/` - Delete project (OWNER only)

### Issues
- `GET /api/organizations/{org_id}/projects/{project_id}/issues/` - List project issues (with filtering/searching/ordering)
- `POST /api/organizations/{org_id}/projects/{project_id}/issues/` - Create issue
- `GET /api/organizations/{org_id}/projects/{project_id}/issues/{id}/` - Get issue details
- `PUT /api/organizations/{org_id}/projects/{project_id}/issues/{id}/` - Update issue
- `DELETE /api/organizations/{org_id}/projects/{project_id}/issues/{id}/` - Delete issue

## Filtering Issues

Use query parameters:
- `project` - Filter by project ID
- `status` - Filter by status (TODO, IN_PROGRESS, DONE)
- `priority` - Filter by priority (LOW, MEDIUM, HIGH)
- `assignee` - Filter by assignee ID
- `search` - Search in title and description
- `ordering` - Order by created_at or priority

Example: `GET /api/organizations/1/projects/1/issues/?status=TODO&search=bug&ordering=-created_at`

## Business Rules

- Organizations: Creator becomes OWNER. Only OWNER can promote to OWNER. Must have at least one OWNER.
- Projects: Only OWNER/MANAGER can create. Only members can view. Only OWNER can delete.
- Issues: Only members can create. Assignee must be organization member. Only OWNER/MANAGER can change priority. Only assignee or OWNER/MANAGER can mark as DONE. Creator or OWNER/MANAGER can delete.

## Assumptions

- User registration requires username, email, password, first_name, last_name.
- All endpoints require authentication except registration and login.
- Error responses follow DRF standards.
- Pagination is enabled with page size 10.
- SQLite is used for simplicity; can be changed to PostgreSQL for production.

## Testing

Use tools like Postman or curl to test the API. Include Authorization header with `Bearer <access_token>` for authenticated requests.