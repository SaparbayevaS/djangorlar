# Education API

This project is a Django REST Framework application for managing courses and lessons with JWT authentication.

## Authentication

JWT authentication is implemented.

- **Obtain Token**
  - Method: POST
  - URL: `/api/token/`
  - Permissions: Public
  - Request body: 
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - Response:
    ```json
    {
      "refresh": "refresh_token",
      "access": "access_token"
    }
    ```

- **Refresh Token**
  - Method: POST
  - URL: `/api/token/refresh/`
  - Permissions: Public
  - Request body:
    ```json
    {
      "refresh": "refresh_token"
    }
    ```
  - Response:
    ```json
    {
      "access": "new_access_token"
    }
    ```

## Course Endpoints

- **List Courses**
  - Method: GET
  - URL: `/api/v1/education/courses/`
  - Permissions: Authenticated
  - Optional query param: `?is_active=true|false`
  - Response: List of courses including `lessons_count`.

- **Create Course**
  - Method: POST
  - URL: `/api/v1/education/courses/`
  - Permissions: Authenticated
  - Request body:
    ```json
    {
      "title": "Course title",
      "description": "Course description"
    }
    ```
  - Response: Created course object.

- **Retrieve Course**
  - Method: GET
  - URL: `/api/v1/education/courses/{id}/`
  - Permissions: Authenticated
  - Response: Course details.

- **Update Course**
  - Method: PUT
  - URL: `/api/v1/education/courses/{id}/`
  - Permissions: Authenticated + owner
  - Request body: Full course data
  - Response: Updated course object.

- **Delete Course**
  - Method: DELETE
  - URL: `/api/v1/education/courses/{id}/`
  - Permissions: Authenticated + owner
  - Response: 204 No Content

- **Activate Course**
  - Method: POST
  - URL: `/api/v1/education/courses/{id}/activate/`
  - Permissions: Authenticated + owner
  - Response: Course object with `is_active=true`.

- **Deactivate Course**
  - Method: POST
  - URL: `/api/v1/education/courses/{id}/deactivate/`
  - Permissions: Authenticated + owner
  - Response: Course object with `is_active=false`.

- **List Lessons of a Course**
  - Method: GET
  - URL: `/api/v1/education/courses/{id}/lessons/`
  - Permissions: Authenticated
  - Response: List of non-deleted lessons.

## Lesson Endpoints

- **Create Lesson**
  - Method: POST
  - URL: `/api/v1/education/lessons/`
  - Permissions: Authenticated + course owner
  - Request body:
    ```json
    {
      "course": 1,
      "title": "Lesson title",
      "content": "Lesson content"
    }
    ```
  - Response: Created lesson object.

- **Retrieve Lesson**
  - Method: GET
  - URL: `/api/v1/education/lessons/{id}/`
  - Permissions: Authenticated
  - Response: Lesson details.

- **Update Lesson**
  - Method: PUT
  - URL: `/api/v1/education/lessons/{id}/`
  - Permissions: Authenticated + course owner
  - Request body: Full lesson data
  - Response: Updated lesson object.

- **Delete Lesson**
  - Method: DELETE
  - URL: `/api/v1/education/lessons/{id}/`
  - Permissions: Authenticated + course owner
  - Response: 204 No Content

- **Publish Lesson**
  - Method: POST
  - URL: `/api/v1/education/lessons/{id}/publish/`
  - Permissions: Authenticated + course owner
  - Response: Lesson object with `is_published=true`.

- **Unpublish Lesson**
  - Method: POST
  - URL: `/api/v1/education/lessons/{id}/unpublish/`
  - Permissions: Authenticated + course owner
  - Response: Lesson object with `is_published=false`.

- **Move Lesson**
  - Method: PUT
  - URL: `/api/v1/education/lessons/{id}/move/`
  - Permissions: Authenticated + course owner
  - Request body:
    ```json
    {
      "before_lesson_id": 2
    }
    ```
  - Response: Lesson object with updated order.

## Soft Deletion

All courses and lessons use soft deletion. `deleted_at` field is used to mark deletion.

## Notes

- JWT authentication is required for all protected endpoints.
- Only course owners can modify, delete, activate/deactivate, or manage lessons of their course.- **Retrieve Lesson**
  - Method: GET
  - URL: `/api/v1/education/lessons/{id}/`
  - Permissions: Authenticated
  - Response: Lesson details.
  
- **Update Lesson**
  - Method: PUT
  - URL: `/api/v1/education/lessons/{id}/`
  - Permissions: Authenticated + course owner
  - Request body: Full lesson data
  - Response: Updated lesson object.
  
- **Delete Lesson**
  - Method: DELETE
  - URL: `/api/v1/education/lessons/{id}/`
  - Permissions: Authenticated + course owner
  - Response: 204 No Content
  
- **Publish Lesson**
  - Method: POST
  - URL: `/api/v1/education/lessons/{id}/publish/`
  - Permissions: Authenticated + course owner
  - Response: Lesson object with `is_published=true`.
      
ø# djangorlal
