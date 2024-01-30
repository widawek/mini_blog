# Blog Application

## Overview
This blog application is built using Flask, a lightweight web application framework in Python. It features a simple yet effective blogging platform where users can create, edit, publish, and delete posts. Additionally, it includes a user authentication system for managing access to certain functionalities.

## Features
- **User Authentication**: Secure login and logout capabilities.
- **Blog Post Management**: Users can add new posts, edit existing ones, and delete them as needed.
- **Post Visibility Control**: Posts can be marked as published or draft, controlling their visibility on the homepage.
- **Draft Management**: A separate section for managing unpublished drafts.

## Installation and Setup
To run this application, you need Python installed on your system. The application also uses Flask and SQLAlchemy.

1. Clone the repository:

    https://github.com/widawek/mini_blog.git

2. Navigate to the app directory:

    blog.py / cd blog-app

3. Install the required packages:

    pip install -r requirements.txt

4. Initialize the database:

    flask db init
    flask db migrate
    flask db upgrade

5. Run the application:

    flask run

## Usage
Once the application is running, navigate to `http://localhost:5000` in your web browser to access the blog.

- **Home Page**: Displays all published blog posts.
- **Login**: Accessible at `/login`, used for user authentication.
- **Post Creation and Editing**: Accessible at `/post/new` and `/post/<entry_id>` for creating and editing posts, respectively.
- **Drafts**: View and manage drafts at `/drafts`.
- **Logout**: Logout from the application.

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your proposed changes.

## License
