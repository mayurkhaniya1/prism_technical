**Django REST Framework — Backend API Assignment**

**Estimated Time:** ~24 hours
**Objective:** Build a RESTful backend API using Django and Django REST Framework (DRF) with proper authentication, permissions, and business logic.

This assignment focuses only on backend API development. No frontend is required.

---

# Assignment Description

You need to develop a **Task Management System API** that allows users to manage organizations, projects, and issues (tasks). The system must support role-based permissions and secure access control.

The API should be designed following REST principles and production-style coding practices.

---

# Core Requirements

## 1. Authentication

Implement user authentication using:

* JWT (preferred) OR Token Authentication

Provide endpoints for:

* User registration
* User login

All other endpoints must require authentication.

---

## 2. Entities

Your system should support the following main entities:

### Organizations

Represents a company or group of users.

Users can create organizations and invite other users to join.

Each organization must maintain member roles.

Roles:

* OWNER
* MANAGER
* MEMBER

---

### Memberships

Represents the relationship between a user and an organization.

A user can belong to multiple organizations but only once per organization.

Membership includes the user’s role inside that organization.

---

### Projects

Projects belong to an organization.

Users create projects within organizations they are members of.

---

### Issues (Tasks)

Issues belong to projects.

Issues represent work items with status and priority.

Each issue may optionally be assigned to a user.

---

# Business Rules

You must enforce proper permissions and validation:

## Organization Rules

* When a user creates an organization, they become its OWNER.
* Only OWNER or MANAGER can add members.
* Only OWNER can promote another user to OWNER.
* An organization must always have at least one OWNER.

---

## Project Rules

* Only OWNER or MANAGER can create projects.
* Only organization members can view projects.
* Only OWNER can delete a project.

---

## Issue Rules

* Only organization members can create issues.
* Issues can only be assigned to users belonging to the same organization.
* Only OWNER or MANAGER can change issue priority.
* Only the assignee or OWNER/MANAGER can mark an issue as DONE.
* Issues can be deleted by creator or OWNER/MANAGER.

---

# API Requirements

You should implement CRUD APIs for:

* Organizations
* Membership management
* Projects
* Issues

The issue listing endpoint must support:

* Filtering (by project, status, priority, assignee)
* Searching (title or description)
* Pagination
* Ordering (created date, priority)

Use proper HTTP methods and status codes.

---

# Technical Expectations

Your implementation should demonstrate:

* Proper use of Django models and relationships
* DRF serializers and viewsets (or APIViews)
* Input validation
* Clean project structure
* Reusable and maintainable code

---

# Submission Requirements

Your submission must include:

* Source code repository
* README documentation

---

# Evaluation Criteria

Candidates will be evaluated based on:

* Correctness of permissions and business logic
* Code quality and structure
* DRF knowledge
* Validation and error handling
* Documentation clarity
* Performance awareness

---

**Important:**
Focus on correctness and clean implementation. If you make assumptions, document them clearly in the README.
