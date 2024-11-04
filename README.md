# Flask Web Application

This is a Flask web application designed to be hosted on AWS. The application uses Docker for containerization.

## Table of Contents

- [Flask Web Application](#flask-web-application)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Directory Structure](#directory-structure)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  
  
  
## Features

- Flask for the web framework
- Docker for containerization
- Deployment ready for AWS

## Directory Structure

Within Computing Component :
- **download**: Directory for files to be downloaded by the user.
- **input**: Directory for files inputed by the user.
- **output**: Directory for files to be outputed to the user.
- **pythonPrograms**: Directory containing the main logic components of the Computing Component.
- **templates**: Directory containing Flask HTML templates.
- **webAppEnv**: Directory for virtual environment or related files.
- **Dockerfile**: Docker configuration file.
- **LICENSE**: License file.
- **main.py**: Main entry point for the Flask application.
- **README.md**: This README file.
- **requirements.txt**: Python dependencies.

Within Other analyis programs :
- **Commonalities and Sub group analysis**: Python programs used to compute Chi Square, and commonalities they are included for reproducibility.

## Prerequisites

- Python 3.8 or higher
- Docker

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name``
   
2. **Set up a virtual environment:**

    ```sh
    python3 -m venv webAppEnv
    source webAppEnv/bin/activate```
    
3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. **Run the Flask application:**

    ```sh
    python main.py
    ```

2. **Access the application:**

    Open your browser and navigate to `http://localhost:5000`.

The application is made to be deployable in any cloud service platform.
