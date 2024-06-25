Guess Quest - ArgoCD Deployment
Welcome to the Guess Quest project! This repository contains the necessary files and instructions to deploy the Guess Quest web application using ArgoCD.

Project Overview
Guess Quest is a web application that presents users with a new riddle each day. Users can solve riddles, view leaderboards, and manage their profiles. This project leverages a variety of technologies and tools to ensure a seamless deployment and operation experience.

Repository Contents
db_manager.py: Manages interactions with the MongoDB database.
dockerfile: Dockerfile for building the web application container.
guessquest-packge-0.1.0.tgz: Helm chart package for deploying Guess Quest.
guessquest-packge: Directory containing the Helm chart for deploying Guess Quest.
jenkins-agent-container: Configuration for Jenkins agent container.
Jenkinsfile: Jenkins pipeline script for CI/CD.
requirements.txt: Python dependencies required for the project.
riddle_generator.py: Script for generating new riddles.
riddle_update.py: Script for updating riddles in the database.
static: Directory containing static files (CSS, JavaScript, images).
templates: Directory containing HTML templates.
tests: Directory containing unit tests for the application.
webapp.py: Main Flask application file.
Prerequisites
Before deploying the application, ensure you have the following tools installed:

Docker
Kubernetes
Helm
ArgoCD
Jenkins
Installation and Deployment
Step 1: Set Up Kubernetes Cluster
Ensure you have a running Kubernetes cluster. You can use Minikube, Docker Desktop, or any other Kubernetes setup.

Step 2: Install ArgoCD
Follow the ArgoCD installation instructions to install ArgoCD in your Kubernetes cluster.

Step 3: Deploy Guess Quest with Helm
Package the Helm chart (if not already packaged):

sh
Copy code
helm package guessquest-packge
Deploy the Helm chart:

sh
Copy code
helm install guessquest guessquest-packge-0.1.0.tgz
Step 4: Configure Jenkins
Set up a Jenkins server if you don't already have one.
Use the provided Jenkinsfile to create a pipeline job in Jenkins.
Step 5: Access the Application
Once the deployment is complete, you can access the Guess Quest application via the exposed service URL.

Configuration
The application can be configured using environment variables and configuration files. Ensure your MongoDB instance details are correctly set in the application's configuration.

Testing
Run the unit tests using the following command:

sh
Copy code
pytest tests/
Contributing
We welcome contributions to improve the Guess Quest project. Please fork the repository and submit a pull request with your changes.