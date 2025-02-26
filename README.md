# OFI Services API

This is a Django REST application that provides API endpoints to a front-end dashboard for the company OFI Services.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

OFI Services API allows you to interact with the company's data through a RESTful interface. This API is designed to support the front-end dashboard, enabling users to visualize and analyze the data.

## Features

- Retrieve process data
- Filter and search process instances
- Create, update, and delete process-related data

## Installation

To get started with the API, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/slacorazza/APIBaseOfiServices.git
    cd ofi-services-api
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

Access the API at `http://127.0.0.1:8000/api/` (for local development) 

Use a tool like Postman or cURL to interact with the API endpoints.

## API Endpoints

- `GET /api/processes/` - Retrieve a list of processes
- `GET /api/processes/{id}/` - Retrieve a specific process by ID
- `POST /api/processes/` - Create a new process
- `PUT /api/processes/{id}/` - Update an existing process
- `DELETE /api/processes/{id}/` - Delete a process


