# Tracker API

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Additional](#additional)
- [Usage](#usage)

## Overview

The Tracker API provides device location tracking and monitoring capabilities.

### Additional

The following optimizations can be implemented to enhance system performance and scalability:

#### Database Optimization

- Consider adding PostgreSQL read replicas if needed for scaling
- Basic primary-replica setup may help with read/write separation
- Connection pooling could improve database performance

#### Caching Layer

- Redis caching may help with frequently accessed data
- Basic Redis setup for caching needs

#### Load Balancing

- Simple load balancer setup using NGINX

## Installation

### Prerequisites

- Docker
- Docker Compose plugin

### Steps

1. Install Docker Compose plugin:
   Follow the official [Docker Compose installation guide](https://docs.docker.com/compose/install/).

2. Clone the repository

    ```sh
    git clone https://github.com/muluel/tracker_api
    ```

3. Navigate to the project directory

    ```sh
    cd tracker_api
    ```

4. Navigate to the project directory

    Create a .env file. Examples in .env.examples

5. Start the application

    ```sh
    docker compose up -d
    ```

### Usage

1. Open your web browser and go to
    <http://localhost:8000/docs>

### Contact

Muhammed Uluel - <mhmmduluel@gmail.com>

Project Link: <https://github.com/muluel/tracker_api>
