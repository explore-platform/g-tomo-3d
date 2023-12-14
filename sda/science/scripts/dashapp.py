import os
import dash
import dash_bootstrap_components as dbc

from flask import Flask

def initialize_dash_app() -> dash.Dash:
    server = Flask('sda_dash')
    
    external_stylesheets = [dbc.themes.YETI]
    # define Trebuchet MS font in custom stylesheet in assets/
    
    prefix = os.environ.get("PATH_PREFIX")
    mount = f"{prefix}dash/" if prefix else "/dash/"
    
    print(f"Mounting Dash at: {mount}")
    
    sda = dash.Dash(__name__, #suppress_callback_exceptions=True,
        #serve_locally = False,
        external_stylesheets=external_stylesheets,
        # requests_pathname_prefix = '/',
        requests_pathname_prefix = mount,
        meta_tags = [
            {"name": "viewport",
             "content": "width=device-width, initial-scale=1.0"},
        ],
        server=server,
    )
    return sda