# NestCare - Household Services Marketplace

NestCare is a full-stack web application designed to connect customers with skilled professionals for a variety of household services. It provides a seamless, role-based experience for customers, professionals, and administrators, ensuring efficient service management and communication.

The platform features distinct dashboards for each user role, an admin-controlled approval process for professionals, and an integrated system for managing service requests from creation to completion.

## Features

### 👨‍💼 Admin Features
- **Secure Admin Login**: Separate authentication endpoint for administrators.
- **Comprehensive Dashboard**: A central view of all users, services, service requests, and pending professional approvals.
- **User Management**:
  - Approve or reject new professional registrations.
  - Flag or unflag users (customers and professionals) to manage their platform access.
- **Service Management (CRUD)**: Create, read, update, and delete the services offered on the platform.
- **Analytics Summary**: View key metrics and data visualizations for:
  - User distribution by role (Professionals vs. Customers).
  - Service request status distribution (Pending, Accepted, Rejected, Closed).
- **Asynchronous CSV Export**: Trigger a background task to export all closed service requests into a CSV file, which is then emailed to the admin.

### 🙋 Customer Features
- **Simple Registration**: Easy sign-up process to get started.
- **Browse & Search**:
  - View all available services.
  - Search for professionals providing a specific service.
- **Service Request Management**:
  - Create detailed service requests for a chosen professional.
  - View and track the status of all submitted requests.
  - Close a service request once the job is completed.
- **Monthly Email Reports**: Receive an automated monthly summary of service request activity.

### 👷 Professional Features
- **Specialized Registration**: Register as a professional by providing details like experience and uploading a portfolio (PDF).
- **Admin Approval Workflow**: New professional accounts are inactive until approved by an administrator.
- **Request Management Dashboard**: Manage all job requests with clear categorization:
  - **Pending**: Accept or reject new requests.
  - **Active**: View currently accepted jobs.
  - **Completed**: See a history of all finished jobs.
  - **Rejected**: Keep track of rejected requests.
- **Daily Email Reminders**: Receive a daily email notification for any pending service requests that require action.

---

## Tech Stack

| Area         | Technology                                                                                             |
|--------------|--------------------------------------------------------------------------------------------------------|
| **Backend**  | Python, Flask, Flask-RESTful, SQLAlchemy, Celery, Redis, Flask-JWT-Extended, Flask-Mail, Flask-Caching |
| **Frontend** | Vue.js 3 (Composition API), Vite, Vue Router, Chart.js, Bootstrap 5                                    |
| **Database** | SQLAlchemy ORM (agnostic, can be used with PostgreSQL, SQLite, etc.)                                   |

---

## Project Setup

### Prerequisites
- Python 3.8+
- Node.js 18+ and npm
- Redis Server (for caching and Celery message broker)

### Backend Setup

1.  **Navigate to the backend directory:**
    ```sh
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Python dependencies:**
    *(Note: A `requirements.txt` file should be generated using `pip freeze > requirements.txt`)*
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configure Environment:**
    - Ensure your Redis server is running.
    - Update the configuration in `apps/config.py` with your database URI, mail server settings, etc.

5.  **Run the Backend Services:**
    - **Flask Application:**
      ```sh
      python main.py
      ```
    - **Celery Worker (for background tasks):**
      ```sh
      celery -A main.celery worker -l info
      ```
    - **Celery Beat (for scheduled tasks):**
      ```sh
      celery -A main.celery beat -l info
      ```

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```sh
    cd frontend
    ```

2.  **Install Node.js dependencies:**
    ```sh
    npm install
    ```

3.  **Run the development server:**
    ```sh
    npm run dev
    ```

4.  **Access the application:**
    Open your browser and navigate to the URL provided by Vite (usually `http://localhost:5173`). The frontend is configured to proxy API requests to the Flask backend running on `http://127.0.0.1:5000`.
