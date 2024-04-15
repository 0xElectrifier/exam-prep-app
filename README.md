# Exam Prep App API Documentation (v1)

## Authentication

### Public Endpoints:

- [ ] POST `/api/v1/auth/register/`: Register a new user.
- [ ] POST `/api/v1/auth/login/`: Log in a user and obtain an authentication token.

### Authenticated Endpoints (require valid authentication token):

- [ ] POST `/api/v1/auth/logout/`: Logout a user and invalidate the authentication token.
- [ ] POST `/api/v1/auth/refresh/`: Refresh an expiring authentication token and obtain a new one.

## User Management

### Authenticated Endpoints (require valid authentication token):

- [ ] GET `/api/v1/user/`: Retrieve user profile information. Returns: User object containing details like username, email (optional).
- [ ] PUT `/api/v1/user/`: Update user profile information. Returns: Updated user object.
- [ ] DELETE `/api/v1/user/`: Delete the user's account. Returns: Success message upon deletion.

## Image Handling

### Authenticated Endpoints (require valid authentication token):

- [ ] POST `/api/v1/images/upload/`: Upload an image. Returns: Object containing information about the uploaded image (e.g., ID, URL).
- [ ] DELETE `/api/v1/images/<image_id>/`: Delete a uploaded image. Returns: Success message upon deletion.

## Text Extraction & Summarization

### Authenticated Endpoints (require valid authentication token):

- [ ] POST `/api/v1/text/extract/`: Extract text from the uploaded image. Returns: Extracted text content.
- [ ] GET `/api/v1/text/summaries/`: Retrieve a list of generated summaries for the user. Returns: Array of summary objects containing details like ID, content, and creation date.
- [ ] GET `/api/v1/text/summaries/<summary_id>/`: Retrieve a specific summary. Returns: Summary object containing details like ID, content, and creation date.
- [ ] PUT `/api/v1/text/summaries/<summary_id>/`: Update an existing summary. Returns: Updated summary object.
- [ ] DELETE `/api/v1/text/summaries/<summary_id>/`: Delete a summary. Returns: Success message upon deletion.

## Flashcard Management

### Authenticated Endpoints (require valid authentication token):

- [ ] GET `/api/v1/flashcard_categories/`: Retrieve a list of flashcard categories for the user. Returns: Array of category objects containing details like ID, name, and creation date.
- [ ] POST `/api/v1/flashcard_categories/`: Create a new flashcard category. Returns: Newly created category object.
- [ ] GET `/api/v1/flashcard_categories/<category_id>/`: Retrieve a specific flashcard category. Returns: Category object containing details like ID, name, and creation date, and potentially a list of associated flashcards.
- [ ] PUT `/api/v1/flashcard_categories/<category_id>/`: Update an existing flashcard category. Returns: Updated category object.
- [ ] DELETE `/api/v1/flashcard_categories/<category_id>/`: Delete a flashcard category. Returns: Success message upon deletion.
- [ ] GET `/api/v1/flashcards/`: Retrieve a list of flashcards for the user. Returns: Array of flashcard objects containing details like ID, category ID (optional), question, answer, image URL (optional), and creation date.
- [ ] POST `/api/v1/flashcards/`: Create a new flashcard. Returns: Newly created flashcard object.
- [ ] GET `/api/v1/flashcards/<flashcard_id>/`: Retrieve a specific flashcard. Returns: Flashcard object containing details like ID, category ID (optional), question, answer, image URL (optional), and creation date.
- [ ] PUT `/api/v1/flashcards/<flashcard_id>/`: Update an existing flashcard. Returns: Updated flashcard object.
- [ ] DELETE `/api/v1/flashcards/<flashcard_id>/`: Delete a flashcard. Returns: Success message upon deletion.
