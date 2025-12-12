# Vercel Deployment Troubleshooting Guide

## Common Errors and Solutions

### Error: 500 INTERNAL_SERVER_ERROR / FUNCTION_INVOCATION_FAILED

This error means your serverless function crashed. Here's how to debug:

#### 1. Check Vercel Logs

1. Go to your Vercel project dashboard
2. Click on the failed deployment
3. Click **"Functions"** tab
4. Click on your function (usually `api/index.py`)
5. View the **"Logs"** tab
6. Look for error messages and stack traces

#### 2. Common Causes and Fixes

**A. Database Connection Error**

**Symptoms:**
- Error mentions "database" or "connection"
- `django.db.utils.OperationalError`
- `psycopg2.OperationalError`

**Solution:**
1. Verify `DATABASE_URL` is set in Vercel environment variables
2. Check the connection string format:
   ```
   postgresql://user:password@host:port/database
   ```
3. Make sure password is URL-encoded if it has special characters
4. Test the connection string locally:
   ```bash
   python manage.py migrate
   ```

**B. Missing Environment Variables**

**Symptoms:**
- `SECRET_KEY` errors
- `KeyError` for environment variables

**Solution:**
1. Go to Vercel → Settings → Environment Variables
2. Verify all required variables are set:
   - `SECRET_KEY`
   - `DEBUG`
   - `DATABASE_URL`
3. Make sure they're set for the correct environment (Production/Preview/Development)
4. Redeploy after adding variables

**C. Import Errors / Module Not Found**

**Symptoms:**
- `ModuleNotFoundError`
- `ImportError`
- `No module named 'xxx'`

**Solution:**
1. Check `requirements.txt` includes all dependencies
2. Verify package names are correct
3. Check for typos in import statements
4. Make sure all your Python files are in the repository

**D. Path Issues**

**Symptoms:**
- `FileNotFoundError`
- Path-related errors

**Solution:**
1. Verify `vercel.json` points to correct file: `api/index.py`
2. Check that `api/index.py` exists in your repository
3. Verify project structure matches expected layout

**E. Django Settings Errors**

**Symptoms:**
- `ImproperlyConfigured`
- Settings-related errors

**Solution:**
1. Check `ALLOWED_HOSTS` includes Vercel domain
2. Verify `DATABASE_URL` is being read correctly
3. Check for missing required settings

#### 3. Debugging Steps

**Step 1: Check Function Logs**
```bash
# In Vercel dashboard:
# Deployments → Latest → Functions → api/index.py → Logs
```

**Step 2: Test Locally with Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Test locally
vercel dev
```

**Step 3: Add Debug Logging**

Temporarily add to `api/index.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

def handler(request):
    print("Handler called")
    print(f"Request: {request}")
    # ... rest of handler
```

**Step 4: Check Environment Variables**

In Vercel dashboard:
- Settings → Environment Variables
- Verify all variables are set
- Check for typos in variable names

**Step 5: Verify Database**

1. Test database connection locally:
   ```bash
   export DATABASE_URL="your-connection-string"
   python manage.py migrate
   python manage.py shell
   ```
2. Verify migrations are up to date
3. Check database is accessible from internet (not localhost)

#### 4. Quick Fixes

**Fix 1: Add Better Error Handling**

Update `api/index.py` to log more details:
```python
except Exception as e:
    import traceback
    error_msg = str(e)
    traceback_str = traceback.format_exc()
    print(f"Full error: {traceback_str}")
    # ... return error
```

**Fix 2: Verify Requirements**

Make sure `requirements.txt` has:
```
Django==5.2.7
djangorestframework==3.16.1
django-cors-headers==4.3.1
whitenoise==6.8.2
psycopg2-binary==2.9.10
dj-database-url==2.3.0
```

**Fix 3: Check Vercel Configuration**

Verify `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

#### 5. Testing Checklist

Before deploying, test locally:

```bash
# 1. Set environment variables
export SECRET_KEY="your-secret-key"
export DEBUG="False"
export DATABASE_URL="your-database-url"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Test Django
python manage.py runserver

# 5. Test with Vercel CLI
vercel dev
```

#### 6. Getting Help

If you're still stuck:

1. **Check Vercel Logs**: Most detailed error info is there
2. **Check Function Logs**: Specific to your serverless function
3. **Test Locally**: Use `vercel dev` to test locally
4. **Simplify**: Try a minimal handler first to verify setup
5. **Vercel Support**: Contact Vercel support with error logs

#### 7. Common Error Messages

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `FUNCTION_INVOCATION_FAILED` | Function crashed | Check logs for specific error |
| `ModuleNotFoundError` | Missing dependency | Add to requirements.txt |
| `OperationalError` | Database connection | Check DATABASE_URL |
| `ImproperlyConfigured` | Django settings | Check ALLOWED_HOSTS, SECRET_KEY |
| `Timeout` | Function too slow | Optimize code or increase timeout |

#### 8. Minimal Test Handler

To test if Vercel setup works, try this minimal handler:

```python
def handler(request):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"message": "Hello from Vercel!"}'
    }
```

If this works, the issue is with Django setup, not Vercel configuration.

---

## Next Steps

1. ✅ Check Vercel logs for specific error
2. ✅ Verify environment variables
3. ✅ Test database connection
4. ✅ Check requirements.txt
5. ✅ Test locally with `vercel dev`
6. ✅ Review error messages carefully
