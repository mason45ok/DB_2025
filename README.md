# Database System EMI

- **Lecture**: NTNU TAHRD Yun-Cheng Tsai (Pecu)

## Flask CRUD Application

This repository contains a simple Flask application that demonstrates CRUD (Create, Read, Update, Delete) operations using MySQL as the database. The application is divided into different blueprints for better organization and clarity.

### Features

- **Create**: Add a new post to the database.
- **Read**: Display all posts from the database.
- **Delete**: Remove selected posts from the database.

### Requirements

To run this application, you will need the following:

- Python 3.x
- Flask
- MySQL or MariaDB
- `mysql-connector-python` package for MySQL integration

### Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Install the necessary dependencies:

    ```bash
    pip install flask mysql-connector-python
    ```

3. Set up your MySQL database:

    - Import the provided SQL file from the [sql directory](https://github.com/peculab/Database/tree/main/sql) or
    - Manually create a MySQL database named `testdb` and run the following SQL to create the `example_table`:

    ```sql
    CREATE TABLE example_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        post TEXT NOT NULL
    );
    ```

4. Configure the database connection by updating the `db_config` in the `create.py`, `delete.py`, and `read.py` files if necessary:

    ```python
    db_config = {
        'user': 'your-username',
        'password': 'your-password',
        'host': 'localhost',
        'database': 'testdb'
    }
    ```

### Running the Application

1. Start the Flask app:

    ```bash
    python app.py
    ```

2. Open your browser and navigate to `http://localhost:5000` to view the application.

### Folder Structure

- `app.py`: The main application file that registers the blueprints for CRUD operations.
- `create.py`: Contains the logic for adding new posts.
- `delete.py`: Contains the logic for deleting selected posts.
- `read.py`: Contains the logic for reading and displaying all posts.
- `templates/index.html`: A simple HTML template for displaying posts and forms for creating and deleting posts.

### Routes

- `/`: Displays all posts.
- `/add`: Adds a new post (POST method).
- `/delete`: Deletes selected posts (POST method).

### Usage

1. **Add a Post**: Fill in the form and submit it to add a new post to the database.
2. **Delete Posts**: Select posts and submit them to delete from the database.
