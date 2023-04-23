import uvicorn
import argparse
from files_searcher import FileSearcher


argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('--host', default='localhost', help='Host to run the server on')
argument_parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
argument_parser.add_argument('--directory', default="C:\\", help='Directory where you need to find file paths')

if __name__ == "__main__":
    args = argument_parser.parse_args()
    FileSearcher.search_dir = args.directory
    config = uvicorn.Config("app:my_app", host=args.host, port=args.port)
    my_server = uvicorn.Server(config)
    my_server.run()
