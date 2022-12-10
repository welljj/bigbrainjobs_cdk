# Big Brain Jobs

This is a job posting website based on Django.

It's built with AWS CDK and includes both the infrastructure to start the website as well as the actual Django website.

## Local development environment
The primary development environment uses [Multipass](https://multipass.run). This makes it easier to develop across platforms, and allows the development environment to match the production. It's particularly useful since this project is using PostGIS which has extra dependencies that can be tricky to install, or clutter the local machine.

The `multipass` folder contains a Python script that'll generate a cloud-init YAML file to use when creating a new Multipass virtual machine -- this file is generated so that it can load the SSH public key from the local machine, so that VSCode (or SSH) can be used for development.

Another tool used is `direnv` with the associated `.envrc` file in the project. `.envrc` contains environment variables for use during development, but should not be used on the production server.

`nodejs` and `npm` are used within the Django project to compile static files.
* `parcel_plugins` contains a single Namer plugin for Parceljs. This plugin simply prevents Parceljs from adding a hash to built files. The plugins main code is built with babel automatically on `npm install` from the top-level of the Django project, so there is no need to travel into this folder to install or build anything. 
* `package.json` is inside the Django project folder, so `npm install` needs to be run from there.
* `npm run build`: builds all static files
* `npm run watch`: watches static files
* `npm run clean`: deletes the static files build directory (useful before building)

`update_requirements.sh` is a helper script to install/update all Python dependencies in the `.venv`. NOTE: Dependencies should be versioned at release.

## Production server
CDK is designed to deploy to AWS. While there are many ways to deploy this application on AWS, this project uses a "simple and cheap" option since this is just a sample project:
* A single EC2 instance with:
   * The Django website in the `website` folder
   * `nginx` and `gunicorn` to serve the website
   * `postgresql` with `postgis` for the database
   * `systemd` socket and service to run the gunicorn server
      * A .env file needs to be created in the home directory with appropriate production env vars

Some of the alternatives (not used in the this project), which are more expensive but better for a real production environment:
* A Load Balancer with EC2 instances in the public subnet holding the Django application, and EC2 instances in a private subnet holding the postgresql + postgis databases.
* AWS Fargate (or AppRunner or ECS): these are container services that can be used with Docker.

NOTE: This is a work-in-progress, many things are not finished or do not work -- specifically the CDK infrastructure code, as that'll be the focus once the Django website is complete. More info to come as it's built.

## Features
 * Candidate app
    * Search through job postings
    * Create personal profile
    * Upload resume
 * Recruiter app
    * Create company profile
    * Search through candidates
    * Create job postings