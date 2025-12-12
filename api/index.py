"""
Vercel serverless function handler for Django
"""
import os
import sys
import io
import base64

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Get the WSGI application
application = get_wsgi_application()

# Export handler for Vercel
def handler(request):
    """
    Vercel serverless function handler
    Converts Vercel request to WSGI and back to Vercel response
    """
    # Extract request data
    method = request.method if hasattr(request, 'method') else request.get('method', 'GET')
    path = request.path if hasattr(request, 'path') else request.get('path', '/')
    headers = request.headers if hasattr(request, 'headers') else request.get('headers', {})
    body = request.body if hasattr(request, 'body') else request.get('body', b'')
    query_string = request.query_string if hasattr(request, 'query_string') else request.get('query_string', '')
    
    # Convert body to bytes if it's a string
    if isinstance(body, str):
        body = body.encode('utf-8')
    
    # Build WSGI environ from Vercel request
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
    
    try:
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
            headers_dict[key.lower()] = value
        
        # Determine if body should be base64 encoded (for binary content)
        body_bytes = b''.join(response_data)
        content_type = headers_dict.get('content-type', '')
        is_binary = any(
            content_type.startswith(prefix) 
            for prefix in ['image/', 'application/octet-stream', 'application/pdf']
        ) or 'charset' not in content_type.lower()
        
        # Return response (Vercel Python runtime format)
        if is_binary:
            return {
                'statusCode': status_code,
                'headers': headers_dict,
                'body': base64.b64encode(body_bytes).decode('utf-8'),
                'isBase64Encoded': True
            }
        else:
            return {
                'statusCode': status_code,
                'headers': headers_dict,
                'body': body_bytes.decode('utf-8', errors='ignore')
            }
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': f'{{"error": "Internal Server Error", "message": "{str(e)}"}}'
        }
