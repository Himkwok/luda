from flask import Flask
from ludaweb import app


def create_app():
    return app


application = create_app()

if __name__ == '__main__':
    application.run()
