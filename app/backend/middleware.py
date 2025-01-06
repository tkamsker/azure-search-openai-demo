from flask import request, jsonify
from functools import wraps
import time
from collections import defaultdict

# Simple in-memory rate limiting
upload_counts = defaultdict(list)
RATE_LIMIT = 10  # uploads per hour
WINDOW_SIZE = 3600  # 1 hour in seconds

def rate_limit_uploads(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401

        current_time = time.time()
        
        # Remove old timestamps
        upload_counts[user_id] = [
            timestamp for timestamp in upload_counts[user_id]
            if current_time - timestamp < WINDOW_SIZE
        ]
        
        # Check rate limit
        if len(upload_counts[user_id]) >= RATE_LIMIT:
            return jsonify({
                'error': 'Rate limit exceeded. Please try again later.'
            }), 429
            
        # Add new timestamp
        upload_counts[user_id].append(current_time)
        
        return f(*args, **kwargs)
    return decorated_function 