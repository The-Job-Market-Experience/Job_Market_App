# Job Market Platforms

This repository provides a complete solution for gathering **data-related job listings for Germany** from the following websites: Stepstone and Welcome to the Jungle. It includes steps for changing the data into a uniform format and then putting it into an Elasticsearch database set up in Docker. Once the data is in the database, it's available through a FastAPI, which can be used for making data visualisations.

The project is organized into different folders: "data_collection", "elasticsearch" and "visualization" each containing the scripts needed to run each part of the project. There's also a "Sandbox" folder with extra scripts that were created during the project but aren't needed for the main solution.


## **Pre-requirements:**
- Python (3.x recommended)
- libaries: ```requests```, ```Selenium```, ```BeautifulSoup4```, ```pandas```, ```urllib```, ```datetime```, ```csv```, ```elasticsearch```, ```FastAPI```, ```plotly```, ```matplotlib```


## **Instructions:**

1. Install pre-requirements in terminal
2. Run the web scraping scripts in the terminal ```python3 Stepstone_fixed.py``` ```python3 WttJ_wscraping_code_final.py```
    - Result: ```jobs_stepstone.csv``` and ```WttJ_jobs.csv```
4. Download and install Docker:

   For macOS:
    - Find the URL for the latest version and use a command in the terminal like this (replace the URL with the latest one):
      ```curl -L -o ~/Downloads/Docker.dmg "https://download.docker.com/mac/stable/Docker.dmg"```
    - Mount the Docker Image ```hdiutil attach ~/Downloads/Docker.dmg```
    - Copy Docker to the Applications Folder for installation ```cp -R /Volumes/Docker/Docker.app /Applications```
    - Eject the Docker Image ```hdiutil detach /Volumes/Docker``` and run Docker from the terminal ```open -a Docker```
    - Follow On-screen Instructions - Docker might ask for additional setup steps once launched.
  
   For Windows:
   
   Download the installer using PowerShell and then run it manually!
    - Open PowerShell as Administrator: Search for PowerShell in the Start menu, right-click it, and select "Run as administrator".
    - To download Docker for Windows, use the ```Invoke-WebRequest``` command in PowerShell. First, obtain the latest installer URL from the Docker website.       Then execute the following command, replacing "<URL>" with the actual download link:
      powershell: ```Invoke-WebRequest -Uri   "https://download.docker.com/win/stable/Docker Desktop Installer.exe" -OutFile   "$HOME\Downloads\DockerInstaller.exe"```
    - Run "DockerInstaller.exe" and complete the installation by following the on-screen instructions

6. Data Cleaning and Feature Engineering:
    - output is a cleaned dataset and ready for ingestion into the dockerized ElasticSearch data warehouse
        ```run cleaning.py```


6. ElasticSearch Ingestion:
    - Move to elasticsearch folder ```cd elasticsearch```
    - run docker ```compose up -d```
    - check with docker ps --> two docker container should be running: kibana and elasticsearch ```run python3 ingest_data.py```
      you can check in browser if locally everything is running and investigate data in elasticsearch UI:
       ```elasticsearch container: http://localhost:9200/```
       ```elasticsearch UI: http://localhost:5601/```

7. FastAPI:
    - Run ```python3 main.py```
    - API is now running at http://localhost:8000/ and ready to retrieve data from.
9. Data Consumption:
     - generate data visualisation by ```run project_viz.ipynb```
