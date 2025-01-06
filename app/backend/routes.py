from flask import Blueprint, request, jsonify, redirect, url_for, session
from .oauth_config import setup_oauth
from .storage_simple import SimpleStorageManager
import secrets

bp = Blueprint('auth', __name__)
storage = SimpleStorageManager()

@bp.route('/login')
def login():
    # Generate state token for security
    session['state'] = secrets.token_urlsafe(16)
    # Redirect to GitHub login
    return oauth.github.authorize_redirect(
        redirect_uri=url_for('auth.callback', _external=True),
        state=session['state']
    )

@bp.route('/callback')
def callback():
    # Verify state token
    if request.args.get('state') != session.get('state'):
        return jsonify({'error': 'Invalid state parameter'}), 400
    
    # Get token from GitHub
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user', token=token)
    user_info = resp.json()
    
    # Store user info in session
    session['user_id'] = user_info['id']
    session['username'] = user_info['login']
    
    return redirect('/upload')

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    
    # Validate file type
    allowed_extensions = {'pdf', 'txt', 'docx'}
    if not file.filename.lower().endswith(tuple(allowed_extensions)):
        return jsonify({'error': 'File type not allowed'}), 400
        
    # Validate file size (100MB limit)
    if len(file.read()) > 100 * 1024 * 1024:  # 100MB in bytes
        return jsonify({'error': 'File too large'}), 400
    file.seek(0)  # Reset file pointer
    
    try:
        blob_name = storage.upload_file(file, session['user_id'])
        return jsonify({
            'success': True,
            'filename': blob_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 