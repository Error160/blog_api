"""
Vercel serverless function handler for Django
"""
import os
import sys
import io
from urllib.parse import parse_qs

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Initialize Django application (this will be called once per cold start)
application = get_wsgi_application()

# Handler for Vercel Python runtime
def handler(request):
    """
    Vercel serverless function handler
    Converts Vercel request to WSGI format
    """
    try:
        # Handle different request formats (dict or object)
        if isinstance(request, dict):
            method = request.get('method', 'GET')
            path = request.get('path', '/')
            headers = request.get('headers', {})
            body = request.get('body', b'')
            query_string = request.get('queryString', '')
        else:
            # Object format
            method = getattr(request, 'method', 'GET')
            path = getattr(request, 'path', '/')
            headers = dict(getattr(request, 'headers', {}))
            body = getattr(request, 'body', b'')
            query_string = getattr(request, 'queryString', '')
        
        # Ensure body is bytes
        if isinstance(body, str):
            body = body.encode('utf-8')
        
        # Parse query string from path if needed
        if '?' in path:
            path, query_string = path.split('?', 1)
        
        # Build WSGI environ
        host = headers.get('host', 'localhost')
        host_parts = host.split(':')
        server_name = host_parts[0]
        server_port = host_parts[1] if len(host_parts) > 1 else '80'
        
        environ = {
            'REQUEST_METHOD': method,
            'SCRIPT_NAME': '',
            'PATH_INFO': path,
            'QUERY_STRING': query_string,
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)) if body else '',
            'SERVER_NAME': server_name,
            'SERVER_PORT': server_port,
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https' if headers.get('x-forwarded-proto') == 'https' else 'http',
            'wsgi.input': io.BytesIO(body) if body else io.BytesIO(),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Add HTTP headers to environ
        for key, value in headers.items():
            if key.lower() not in ('content-type', 'content-length'):
                key = 'HTTP_' + key.upper().replace('-', '_')
                environ[key] = value
        
        # Call WSGI application
        response_data = []
        status_code = 200
        response_headers = []
        
        def start_response(status, headers, exc_info=None):
            nonlocal status_code, response_headers
            status_code = int(status.split()[0])
            response_headers = headers
        
        response_body = application(environ, start_response)
        
        # Collect response body
        for chunk in response_body:
            if isinstance(chunk, bytes):
                response_data.append(chunk)
            else:
                response_data.append(chunk.encode('utf-8'))
        
        # Build response headers dict
        headers_dict = {}
        for key, value in response_headers:
            headers_dict[key] = value
        
        # Return response
        return {
            'statusCode': status_code,
            'headers': headers_dict,
            'body': b''.join(response_data).decode('utf-8', errors='ignore')
        }
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        
        # Log error (will appear in Vercel logs)
        print(f"Error: {error_msg}")
        print(traceback_str)
        sys.stderr.write(f"Error: {error_msg}\n{traceback_str}\n")
        
        # Return error response
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': f'{{"error": "Internal Server Error", "message": "{error_msg}"}}'
        }
