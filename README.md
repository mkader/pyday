https://diataxis.fr/ - A systematic framework for technical documentation authoring.

GitHub Codespaces is a cloud-based development environment that enables developers to write, build, and debug their code directly from their web browser.

Free APIs to try: Zippopotamus, Sunrise/Sunset, Reddit

pip install urllib3 rich fastapi "uvicorn[standard]"

Processing APIs in python use urllib, requests or urllib3

    PoolManager is a class in the urllib3 library used to manage connection pools for one or more HTTP connections. 
    It is used to create an instance of an HTTP connection pool with a specified number of connections. 
    You can use this instance to send multiple requests to the same host and reuse the same connection for each request, 
    which can result in faster response times and reduced overhead.

    rich is a Python library for rich text and beautiful formatting in the terminal. 
    It provides various features such as syntax highlighting, progress bars, tables, markdown, and more. 
    It aims to make it easier to create beautiful and informative console output. It supports both Python 3.6+ and PyPy3.

FastAPI - https://fastapi.tiangolo.com/
    FastAPI is a web framework for building APIs with Python 3.7+. It is designed to be easy, fast and to provide high performance.

    It uses the Python type hinting system to validate data types and function parameters, which makes it write and maintain type-safe APIs.

    FastAPI is a lightweight ASGI (Asynchronous Server Gateway Interface) framework, compatible with a wide range of ASGI servers such as Uvicorn and Hypercorn, which provide high-performance web servers.

    It contains a built-in OpenAPI and JSON Schema generator, which allows to generate API documentation and client libraries. Additionally, It has built-in support for testing and debugging your API.

FastAPI is a python framework designed specifically for building HTTP APIs.
    Fast to build and fast to execute
    Relies on python types (via pydnatic)
    Auto-generated documentation (via Swagger-UI)
    Based on the OpenAPI specifications.
    Supports passing parameters in the path, cookies, headers or body.

    Running FastAPI locally
        Put code in api/main.py
        Run the server: uvicorn  api.main:app --reload --port=8000
            api.main:app specifies the module and the variable name of the application that needs to be run.
            --reload enables hot-reloading, any code changes, the server will restart automatically.
            --port=8000, which the server will be listening for incoming requests.
        
        Try the API and docs : http://127.0.0.1:8000/generate_name
                               http://127.0.0.1:8000/docs   
                               http://127.0.0.1:8000/redoc
                               http://127.0.0.1:8000/openapi.json 

    Testing FastAPI apps
        Configuring pytest and coverage
            Create a requirements-dev.txt file:
                -r api/requirements.txt
                fastapi[all]
                pytest
                pytest-cov
                coverage

                "-r api/requirements.txt" flag,install the required Python packages listed in the api/requirements.txt file.
                "fastapi[all]" package, installs FastAPI with all dependencies (Uvicorn, Pydantic and other libraries)
                "pytest" package is a testing framework that allows you to write and run automated tests for your Python code.
                "pytest-cov" package is a plugin for pytest that provides code coverage reports for your tests.
                "coverage" package is a tool that measures code coverage during Python program execution.

            Configure inside pyproject.toml
                [tool.pytest.ini_options]
                addopts = "-ra --cov api"
                testpaths = [ "tests" ]
                pythonpath = ['.']    

                pyproject.toml is a configuration file used by modern Python projects that adopt the poetry build tool. It is similar to other configuration files like setup.cfg, setup.py, or requirements.txt, but with additional features and functionalities.
                    "[tool.pytest.ini_options]" - contains additional configuration options to pass to pytest, a popular Python testing framework.
                    "addopts" - specifies additional command-line options to pass to pytest. 
                        "-ra" tells pytest to output all test results
                        "--cov api" enables test coverage reporting for the api module.
                    "testpaths" -specifies directories tests (containing all tests).
                    "pythonpath" - specifies which directories to include in the Python module search path. In this case, . (the current directory) is included, so that modules in the current directory can be imported and used in the tests.

        Create folde and file - "tests\test_api.py"        
        pip install -r requirements-dev.txt
        python -m pytest
            - Name          Stmts   Miss  Cover
            ---------------------------------
            api/main.py      19      9    53%
            - not giving missing lines details
        python -m pytest --cov-report=html
            - it will create folder htmlcov
            - go to the folder, run python3 -m http.server 8000 --bind 127.0.0.1
            - browse to see the coverage report https://127.0.0.1/htmlcov/index.html

Property-based tests with schemathesis
    Property-based testing is a type of testing approach that focuses on generating a large number of random inputs to test functions and APIs. Instead of manually creating test, the testing framework generates automatically, based on predefined properties.

    Schemathesis is a Python library for property-based testing of APIs. It automatically generates API test cases based on their OpenAPI schema (Swagger). IT generates a large number of random requests to the API and checking that the responses match the expected schema.

    Schemathesis also has various features like test coverage analysis, response time tracking, and compatibility with different Python testing frameworks like pytest.

    By using schemathesis, developers can perform thorough testing of their APIs with minimal manual effort, which can lead to more reliable and bug-free code. It's useful for ensuring that your API is robust and can handle a variety of inputs and outputs.

    Add schemathesis to requirments-dev.txt
        
    Generaete tests based on the OpenAPI Spec: ("tests\property_based.py")
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
            E       1. Received a response with a status code, which is not defined in the schema: 404
            E       Declared status codes: 200, 422
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
    Gunicorn (Green Unicorn), is a Python Web Server Gateway Interface (WSGI) HTTP server.
        It's used in popular Python web frameworks (Flask, Django, Pyramid, and Bottle). It can handle requests from multiple clients simultaneously by pre-forking worker processes to handle each request, resulting in efficient resource utilization.

        It's easy use and configure (including logging, worker processes, worker class, timeout, and more). It can also be integrated with a wide range of deployment tools, such as Docker, Kubernetes, and Heroku.

    Gunicorn- won't work windows, it will work on unix
        It's a production-level server that can run multiple worker process

        Add gunicorn to requirements.txt
            fastapi==0.95.1
            uvicorn[stanadard]==0.22.0
            gunicorn==20.1.0

        Pip install -r requirements-dev.txt
        Use gunicorn to run FastAPI app using uvicorn worker:
            python -m gunicorn api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000     

            This command starts a Gunicorn server to run a Python web application located in api/main.py, using the FastAPI app instance app. The server will run with 4 worker processes to handle incoming requests, using the uvicorn worker class UvicornWorker to support asynchronous handling of requests. The server will listen on all available network interfaces (0.0.0.0) on port 8000.
            "python -m gunicorn" invokes the Gunicorn server using the python interpreter.
    
    Configuring gunicorn
        Gunicorn can be configured with a "gunicorn.conf.py" file to adjust worker count based on CPU cores

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

        In this particular example, we see the following configurations:
            max_requests: sets the maximum number of requests a worker will process before restarting
            max_requests_jitter: sets the maximum jitter to add to the max_requests value to reduce the likelihood of all workers restarting at the same time
            log_file: sets the location for the Gunicorn server logs, in this case, logs will be sent to standard output (-)
            bind: sets the address and port on which Gunicorn will listen for connections
            worker_class: sets the worker class for handling requests, in this case, it's using UvicornWorker, a worker for the Uvicorn ASGI server
            workers: sets the number of worker processes for handling incoming requests. The number of workers is calculated based on the number of available CPUs, adding 1 and then multiplying by 2.

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
        ![alt text](image_file_path)
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

    Customizing App Service for FastAPI
        App Service doesn't yet know hot to automatically run FastAPI apps, so we must tell it.
        Either use the portal
            Select "Settings" > "Configuration" in left nav, then select "General settings" tab.
            In "Startup Command" field, enter
                python -m gunicorn main:app
            Save and wait for server to restart.
        Or use the Azure CLI
            az webapp config set --resource-group <resource-group> --name <app-name> --startup-file "python -m gunicorn main:app"    

More API Examples
    FastAPI + API Management
        Azure API Management provides features of a public API: subscription keys, rate limiting, IP blocking, etc.
        https://github.com/pamelafox/fastapi-azure-function-apim

    FastAPI + CDN
        Azure CDN provides a global netowrk of servers to cache your API responses.
        https://github.com/pamelafox/staticmaps-function

    FastAPI + scikitleran
        A parameterized API based on a sklearn model.
        https://github.com/pamelafox/scikitlearn-model-to-fastapi-app

https://github.com/pamelafox        