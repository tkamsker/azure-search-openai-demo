from authlib.integrations.flask_client import OAuth
from flask import Flask
import os

def setup_oauth(app: Flask):
    oauth = OAuth(app)
    
    # Configure OAuth provider (e.g., GitHub)
    oauth.register(
        name='github',
        client_id=os.getenv('GITHUB_CLIENT_ID'),
        client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )
    
    return oauth 