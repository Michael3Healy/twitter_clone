# Warbler

## A Twitter Clone with a Springboard Spin

Warbler is a Twitter clone designed as a project exercise for Springboard students. The purpose of this project was to practice reading and understanding an existing codebase, fixing bugs, writing tests, and adding new features. This README outlines the features implemented and instructions for running the application.

## Features

- User authentication (sign up, log in, log out)
- User profiles with editable information (username, email, bio, profile image, and header image)
- Follow and unfollow functionality
- Tweet-like "warbles" with the ability to post, view, and delete
- Liking and unliking warbles
- Displaying liked warbles on user profiles

## Setup

### Installation

1. **Clone the repository:**
    ```bash
    $ git clone <repository-url>
    $ cd warbler
    ```

2. **Create and activate the virtual environment:**
    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    (venv) $ pip install -r requirements.txt
    ```

4. **Set up the database:**
    ```bash
    (venv) $ createdb warbler
    (venv) $ python seed.py
    ```

5. **Start the server:**
    ```bash
    (venv) $ flask run
    ```

## Usage

After starting the server, you can access the application at `http://127.0.0.1:5000`. Create an account, log in, and start exploring Warbler!

## Testing

To ensure the application works correctly, run the provided tests. The tests cover models, views, and other aspects of the application.

    (venv) $ python3 -m unittest discover -s unittests/
    

