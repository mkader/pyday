Processing APIs in python use urllib, requests or urllib3
Free APIs to try: Zippopotamus, Sunrise/Sunset, Reddit
pip install urllib3, rich

PoolManager is a class in the urllib3 library used to manage connection pools for one or more HTTP connections. 
It is used to create an instance of an HTTP connection pool with a specified number of connections. 
You can use this instance to send multiple requests to the same host and reuse the same connection for each request, 
which can result in faster response times and reduced overhead.

rich is a Python library for rich text and beautiful formatting in the terminal. 
It provides various features such as syntax highlighting, progress bars, tables, markdown, and more. 
It aims to make it easier to create beautiful and informative console output. It supports both Python 3.6+ and PyPy3.

FastAPI is a python framework designed specifically for building HTTP APIs.
    Fast to build and fast to execute
    Relies on python types (via pydnatic)
    Auto-generated documentation (via Swagger-UI)
    Based on the OpenAPI specifications.

    Running FastAPI locally
        Put code in api/main.py
        Install requiremets: Pip install fastapi, "uvicorn[standard]"
        Run the server: uvicorn  api.main:app --reload --port=8000
        Try the API and docs : http://127.0.0.1:8000/generate_name
                               http://127.0.0.1:8000/docs   
                               http://127.0.0.1:8000/openapi.json 

    FastAPI also supports passing parameters in the path, cookies, headers or body.

    Testing FastAPI apps
        Configuring pytest and coverage
            Create a requirements-dev.txt file:
                -r api/requirements.txt
                fastapi[all]
                pytest
                pytest-cov
                coverage
            Configure inside pyproject.toml
                [tool.pytest.ini_options]
                addopts = "-ra --cov api"
                testpaths = [ "tests" ]
                pythonpath = ['.']    
        Create tests folder
            Create  test_api.py        
        pip install -r requirements-dev.txt
        python -m pytest

API unit test with pytest (test_api.py)
    import random
    from fastapi.testclient import TestClient
    from api.main import app
    def test_generate_name():
        with TestClient(app) as client:
            random.seed(123)
            response = client.get("/generate_name")
            assert response.status_code == 200
            assert response.json() == {"name" : "Abdul"}

Property-based tests with schemathesis
    Add schemathesis to requirments-dev.txt
    Generaete tests based on the OpenAPI Spec:
        import schemathesis
        from api.main import app
        schema = schemathesis.from_asqi("/openapi.json",app)
        
        #schema.parametrize()
        def test_api():
            response = case.call_asqi()
            case.validate_response(response)

    pip install -r requirements-dev.txt

    Run the tests
        pytest -k test_api   
        pytest -v tests/property_based.py 

    Error, when i run pytest -v tests/property_based.py  

            E       schemathesis.exceptions.CheckFailed: 
            E       
            E       1. Received a response with a status code, which is not defined in the 
            schema: 404
            E       
            E       Declared status codes: 200, 422
            E       
            E       ----------
            E       
            E       Response status: 404
            E       Response payload: `{"detail":"No names available"}`    

        To solve the error either add 
            (property_based.py)
                if response.status_code == 404:
                    assert response.content == b'{"detail":"No names available"}'
                else:
                    case.validate_response(response)
            OR main.py
                @app.get("/generate_name_qs", responses={404:{}})

Through Visual Code, run unit test
    Configure Python Tests
    Select pytest pytest framework
    select "tests" folder
    "Run Tests"

Proudctionizing FastAPI apps
    Gunicorn- won't work windows, it will work on unix
        It's a production-level server that can run multiple worker process

        Add gunicorn to requirements.txt
            fastapi==0.95.1
            uvicorn[stanadard]==0.22.0
            gunicorn==20.1.0

        Pip install -r requirements-dev.txt
        Use gunicorn to run FastAPI app using uvicorn worker:
            python -m gunicorn api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000     
    
    Configuring gunicorn
        Gunicorn can be configured with a gunicorn.conf.py file to adjust worker count based on CPU cores

            # Gunicorn configuration file
            # https://docs.gunicorn.org/en/stable/configure.html#configuration-file
            # https://docs.gunicorn.org/en/stable/settings.html

            import multiprocessing

            max_requests = 1000
            max_requests_jitter = 50
            log_file = "-"
            bind = "0.0.0.0:3100"
            worker_class = "uvicorn.workers.UvicornWorker"
            workers = (multiprocessing.cpu_count() * 2) + 1

        Run command can be simplified to
            cd api
            python -m gunicorn main:app

Hosting an HTTP API on Azure!
    Hosting considerations
        How much traffic do you expect?
        How variable will the traffic be?
        Do you need scale-to-zero?
        What's your budget?
        Is it public facing?
        How will you manage API use?

    AZure hosting options
        Cloud       |           A           z           u           r           e         |
        
        Environment |   C   o   n  t    a  i   n ers    |   |  P        a           a   s |
        
                    |A zure K 8s|   | Container |           | Azure App | | Serverless | 
                    Services        Management              Service
                                    
                                    | Azure Container |                   | Azuer     |  
                                        Apps                             Functions
    
    Ways to deploy to Azure App Service
        VS Code extension
        Azure Portal (with Github integration)
        Azure CLI
        Azure Developer CLI with Bicep

    Deployig to App Service with VS Code
        VS code extension -> Search "Azure Tools" -> Install  "Azure Tools"
        Select "Create resource" > "Create App Service Web App"
            Enter a name
            Select runtime stack (Pythong 3.11)
            Select tier (Free - F1)
        Select "Deploy" and select "api" as the path to deploy.     

https://github.com/pamelafox        