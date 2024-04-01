# frontend-REST-repo
This repo will be used to be run on a front-end server that responds to REST APIs requests. 

# Installation
## Installing MS SQL Drivers [REQUIRED FOR BOTH OSes]
If you are running Windows, please follow this [instruction](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16). A separate instruction for Linux is also provided [here](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=alpine18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline)

## Using Docker
1. To install the Docker environment, type `sudo docker build -t <image_name> . ` where [image_name] is the name of the image.
2. Type `sudo docker run -it -e "$(pwd)":/code -p 8888:8888 <image_name> bash` to create the container and launch it.
3. Type `jupyter lab --ip 0.0.0.0 --no-browser --allow-root` to launch the JupyterLab IDE.
4. To stop the container, type `exit`, followed by `sudo docker container ps -a`. Then, type `sudo docker stop <container_id>` where container_id is the container you have created in step 2.
5. To restart the container and access it, type `sudo docker start <container_id>`, followed by `sudo docker exec -it <container_id> bash`.

## Using Python's Virtualenv
1. With the root directory of this repo as the current directory, type `python3 -m venv .env`.
2. On Linux, type `source activate .env/bin/activate`. If using Windows, type `.env\scripts\activate` in Command Prompt or `.env\scripts\activate.ps1` in PowerShell.
3. Install the dependencies by typing `python3 -m pip install -r requirements.txt`.

