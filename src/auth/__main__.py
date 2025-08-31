from auth.bootstrap.cli_web import main as web_main
from auth.bootstrap.cli_worker import main as worker_main

if __name__ == "__main__":
    web_main()
    worker_main()
