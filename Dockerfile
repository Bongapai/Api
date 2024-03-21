# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory
WORKDIR /app

# Copy environment file and create Conda environment
COPY environment.yml .
RUN conda env create -f environment.yml

# Activate Conda environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Copy the application code into the container
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 8080

# Set the default command to run the Flask app
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "app.py"]

