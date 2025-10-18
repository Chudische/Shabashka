# Shabashka

Shabashka is an online marketplace that connects people who need to get jobs done with skilled workers who can help. Whether it's home repairs, cleaning, or running errands, Shabashka provides a platform for users to find reliable help for their everyday tasks.

## Key Features

*   **User Authentication:** Secure user registration and login system.
*   **Offer Creation:** Users can easily create new offers for the jobs they need done.
*   **Reviews and Ratings:** A comprehensive review and rating system to help users choose the best worker for the job.
*   **Real-time Chat:** A built-in chat feature for seamless communication between users.
*   **Categorized Services:** A dedicated services page with a grid of categories, making it easy to find the right service.

## User Flow

1.  A user registers and logs in to the platform.
2.  The user creates a new offer, providing a title, description, and price.
3.  Other users can view the offer and leave comments, ask questions, and offer their services.
4.  The offer creator can then choose a worker and accept their proposal.
5.  Once the job is complete, the offer creator can mark the offer as done and leave a review for the worker.

## Technologies Used

*   **Backend:**
    *   Django
    *   Django REST Framework
*   **Frontend:**
    *   HTML
    *   CSS
    *   Bootstrap
    *   JavaScript
    *   jQuery
*   **Database:**
    *   PostgreSQL
*   **Other Key Libraries:**
    *   `social-auth-app-django`
    *   `django-crispy-forms`
    *   `easy-thumbnails`
*   **Dependency Management:**
    *   `uv`
*   **Containerization:**
    *   `Docker`
    *   `Docker Compose`

## Installation and Setup

### Prerequisites

*   Docker
*   Docker Compose

### Instructions

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/Shabashka.git
    cd Shabashka
    ```

2.  **Build and run the containers:**

    ```bash
    docker compose up -d --build
    ```

3.  **Apply database migrations:**
    ```bash
    docker compose exec web uv run manage.py makemigrations
    docker compose exec web uv run manage.py migrate
    ```

4.  **Create a superuser:**

    ```bash
    docker compose exec web uv run python manage.py createsuperuser
    ```

5.  **Import services to Database**
    
    You can import services in Admin interface at http://127.0.0.1:8000/admin
    In the Categories table using `IMPORT` button and `categories.json` file.

### Email Configuration

Shabashka uses Gmail's SMTP server for sending emails. To enable this feature, you will need to configure your Gmail account to allow access for less secure apps.

    
For testing purposes you can use Django console backend in `settings.py`:

    
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    

## API Documentation

*   **/api/offers/**: Get a list of all offers.
*   **/api/offers/&lt;pk&gt;/**: Get the details of a specific offer.
*   **/api/offers/&lt;pk&gt;/comments/**: Get or post comments on a specific offer.

## TODO List

*   Integrate Google Maps for location-based services
*   Add search by location functionality
*   Implement drag-and-drop for image uploads