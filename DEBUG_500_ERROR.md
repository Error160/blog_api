# How to Debug Your 500 Error on Vercel

## 🔍 Step 1: Check Vercel Logs (Most Important!)

The logs will tell you exactly what went wrong:

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Sign in and go to your project

2. **View Deployment Logs**
   - Click on your project
   - Click on the failed deployment (red status)
   - Click **"Functions"** tab
   - Click on **`api/index.py`**
   - Click **"Logs"** tab
   - **Look for error messages** - this is your key to fixing it!

3. **What to Look For:**
   - Red error messages
   - Stack traces (lines showing file paths and line numbers)
   - Import errors
   - Database connection errors
   - Missing environment variables

## 🎯 Step 2: Common Issues Based on Error Type

### If you see: `django.db.utils.OperationalError` or `psycopg2.OperationalError`

**Problem**: Database connection failed

**Fix**:
1. Check `DATABASE_URL` in Vercel environment variables
2. Verify the connection string format:
   ```
   postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
   ```
3. Make sure you replaced `[YOUR-PASSWORD]` with actual password
4. Test the connection string locally:
   ```bash
   export DATABASE_URL="your-connection-string"
   python manage.py migrate
   ```

### If you see: `ModuleNotFoundError` or `ImportError`

**Problem**: Missing Python package

**Fix**:
1. Check `requirements.txt` has all packages
2. Make sure package versions are correct
3. Redeploy after updating requirements.txt

### If you see: `ImproperlyConfigured` or `SECRET_KEY`

**Problem**: Missing environment variable

**Fix**:
1. Go to Vercel → Settings → Environment Variables
2. Add missing variables:
   - `SECRET_KEY`
   - `DEBUG`
   - `DATABASE_URL`
3. Redeploy after adding

### If you see: `ALLOWED_HOSTS` error

**Problem**: Vercel domain not in ALLOWED_HOSTS

**Fix**: Already handled in settings.py, but verify it's working

## 🛠️ Step 3: Quick Fixes to Try

### Fix 1: Verify Environment Variables

1. Go to Vercel → Your Project → Settings → Environment Variables
2. Verify you have:
   - ✅ `SECRET_KEY` (with a value)
   - ✅ `DEBUG` (set to `False` for production)
   - ✅ `DATABASE_URL` (your Supabase connection string)

### Fix 2: Test Database Connection

Test your Supabase connection string locally:

```bash
# Set the environment variable
export DATABASE_URL="postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres"

# Try to connect
python manage.py migrate
```

If this fails locally, the connection string is wrong.

### Fix 3: Check Requirements.txt

Make sure `requirements.txt` includes:
```
Django==5.2.7
djangorestframework==3.16.1
django-cors-headers==4.3.1
whitenoise==6.8.2
psycopg2-binary==2.9.10
dj-database-url==2.3.0
```

### Fix 4: Run Migrations

After fixing database connection, you need to run migrations:

**Option A: Via Vercel Function (Temporary)**
Create a temporary endpoint to run migrations (remove after use):

```python
# In api/urls.py or a view
from django.core.management import call_command
from django.http import JsonResponse

def run_migrations(request):
    if request.method == 'POST':
        call_command('migrate', verbosity=0)
        return JsonResponse({'status': 'Migrations completed'})
    return JsonResponse({'error': 'Use POST'}, status=400)
```

**Option B: Via Local Machine**
1. Set `DATABASE_URL` to your Supabase URL
2. Run: `python manage.py migrate`
3. This will create tables in Supabase

## 📋 Step 4: Deployment Checklist

Before redeploying, verify:

- [ ] `DATABASE_URL` is set in Vercel (with correct password)
- [ ] `SECRET_KEY` is set in Vercel
- [ ] `DEBUG` is set to `False` in Production
- [ ] `requirements.txt` has all dependencies
- [ ] `vercel.json` exists and is correct
- [ ] `api/index.py` exists
- [ ] Database connection works locally
- [ ] Migrations have been run (or will run on first request)

## 🚀 Step 5: Redeploy

After making fixes:

1. **If you changed code**: Push to Git, Vercel will auto-deploy
2. **If you only changed environment variables**: 
   - Go to Deployments
   - Click "..." on latest deployment
   - Click "Redeploy"

## 📞 Step 6: Still Not Working?

If you've tried everything:

1. **Copy the exact error from Vercel logs**
2. **Check**:
   - What the error message says
   - Which file/line it's failing on
   - What the stack trace shows
3. **Share the error** (remove sensitive info like passwords)

## 💡 Pro Tips

1. **Always check logs first** - They tell you exactly what's wrong
2. **Test locally** - Use `vercel dev` to test locally
3. **Start simple** - Make sure basic setup works before adding complexity
4. **Check environment variables** - Most issues are missing/wrong env vars
5. **Database first** - Make sure database connection works before deploying

---

## Quick Reference: Where to Find Logs

```
Vercel Dashboard
  └── Your Project
      └── Deployments
          └── [Failed Deployment]
              └── Functions
                  └── api/index.py
                      └── Logs ← HERE!
```

The logs will show you the exact error. That's your starting point! 🎯
