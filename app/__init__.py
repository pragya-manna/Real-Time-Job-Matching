from flask import Flask
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, '..', 'templates'),
    static_folder=os.path.join(base_dir, '..', 'static')
)

from app import routes


