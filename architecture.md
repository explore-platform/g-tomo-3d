# SDA architecture

## 
- **_local**: The local environement to launch for development, for example using flask's file detection and development server or CRA's webpack
- **_prod**: The production environement for the end build, building what's neccessary and 

## Stacks

1. Machine learning
    * local
        - Flask (with its development server)
    * production
        - Flask
        - Gunicorn
2. Science
    * local
        - Fast API
        - Uvicorn
    * production
        - Fast API
        - Uvicorn
3. Visualiser
    * local
        - React
        - Webpack/CRA
    * production
        - web bundle (served from nginx)

All load balanced/proxied via nginx


## Access

1. Machine learning
    * host
        - localhost:8015/machine_learning/ (nginx)
        - localhost:5001 (direct)
    * docker
        - 0.0.0.0:5001
2. Science
    * host
        - localhost:8015/science/ (nginx)
        - localhost:5002 (direct)
    * docker
        - 0.0.0.0:8000
2. Visualiser
    * host
        - localhost:8015 (nginx)
        - localhost:3030 (direct) *Preferable for development, the current nginx conf is not configured to work correctly with the websocket and with the subpath*
    * docker
        - 0.0.0.0:5001



## Environment Variables

* PATH_PREFIX
The sub path on which the SDA is deployed on.

* SERVICE_INPUT_DATA (Read-Only)
User's file space or the files passed into the SDA.

* SERVICE_APP_DATA (Read-Write-Execute)
The app's appdata directory for persistent data or large datasets.

* SERVICE_USER_APP_DATA (Read-Write-Execute)
The user's appdata directory, for string user inputs or other usefull peristent data.

* SERVICE_OUTPUT_DATA (Read-Write-Execute)
The file space which will then be saved in the user's basket later on.
