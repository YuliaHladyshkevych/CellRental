# Cell Rental Django Project


This is a simple Django project with Celery integration using Docker Compose. The project allows users to rent cells and sends email reminders before the rental period ends.

## Getting Started

### Prerequisites

- Python 3.x
- Docker
- Docker Compose

### ⚙️ Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/YuliaHladyshkevych/CellRental.git
    ```

2. Change to the project directory:

    ```bash
    cd cell_rental
    ```

3. You can open project in IDE and configure .env file using .env.sample file 
as an example.

4. Build and run the Docker containers:
    ````bash
    docker-compose up --build

Access the Django app at [http://localhost:8000/](http://localhost:8000/) and start renting cells.

## Endpoints

### 1. `/api/v1/orders/`

- **Method:** POST
- **Request Body:**
  
    ```json
    {
        "start_timestamp": 1707390825,
        "end_timestamp": 1707477225,
        "user_data": {
            "email": "somemail@gmail.com",
            "name": "Віталій"
        }
    }
    ```

### 2. `/orders/`

- **Method:** GET
- **Description:** Page with an HTML form for renting cells.


- **Method:** POST
- **Description:** Process the form. Redirects to `/orders/<slug>/` upon successful order creation.

### 3. `/orders/<slug>/`

- **Description:** Detailed information about the order.

### Celery Tasks

Celery tasks are configured to send email reminders to users 30 minutes before the end of their rental period. The tasks are scheduled to run every 15 minutes using Celery Beat.

## Notes

- Use the provided Celery tasks and configure Celery Beat for periodic execution.
- Emails are sent to the console (check the Docker logs) for demonstration purposes.

Feel free to explore the project and customize it according to your needs.