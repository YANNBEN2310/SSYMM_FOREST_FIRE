
# Fire Simulation

This project is a simulation of a fire spread using Flask for the backend and Node.js with Three.js for the 3D rendering.

## Installation

1. Clone the repository.
2. Navigate to the project directory.

### Flask Setup

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the Flask application:
   ```bash
   python app.py
   ```

### Node.js and Three.js Setup

7. Install Node.js if you haven't already from [here](https://nodejs.org/).

8. Navigate to the `static` directory (or wherever your Node.js project is located).

9. Initialize a new Node.js project and install the necessary packages:
   ```bash
   npm init -y
   npm install three
   ```

10. Run your Node.js application (modify as needed for your specific setup):
    ```bash
    node your-nodejs-file.js
    ```

## Docker Setup

To containerize and run the application using Docker, follow these steps:

1. Ensure you have Docker installed. If not, download and install it from [here](https://www.docker.com/products/docker-desktop).

2. Create a `Dockerfile` in the root of your project with the following content:
   ```Dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```

3. Build the Docker image:
   ```bash
   docker build -t flask-forest-fire .
   ```

4. Run the Docker container:
   ```bash
   docker run -p 5000:5000 flask-forest-fire
   ```

By following these steps, you can set up and run the Fire Simulation project both locally using a virtual environment and in a Docker container. Enjoy simulating fire spread with Flask and Three.js!
