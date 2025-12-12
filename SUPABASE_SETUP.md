# Setting Up Supabase Database for Django API

This guide will walk you through creating a PostgreSQL database on Supabase and getting the connection URL for your Django API.

## 🚀 Step 1: Sign Up for Supabase

1. Go to [supabase.com](https://supabase.com)
2. Click **"Start your project"** or **"Sign Up"** (top right)
3. Sign up using one of these methods:
   - **GitHub** (recommended - easiest)
   - **Google**
   - **Email** (create account with email/password)
4. Verify your email if required

## 📦 Step 2: Create a New Project

1. After signing in, you'll see your dashboard
2. Click the **"New Project"** button (usually green, top right or center)
3. Fill in the project details:

   **Organization:**
   - If this is your first project, you'll create an organization
   - Enter your organization name (e.g., "My Projects" or your name)
   - Click **"Create organization"**

   **Project Details:**
   - **Name**: Give your project a name (e.g., "django-api-db" or "blog-api")
   - **Database Password**: 
     - ⚠️ **IMPORTANT**: Create a STRONG password (save it somewhere safe!)
     - Must be at least 8 characters
     - Include uppercase, lowercase, numbers, and special characters
     - Example: `MySecurePass123!@#`
     - **Save this password** - you'll need it for the connection string
   
   **Region:**
   - Choose the region closest to you or your users
   - Examples: US East, US West, Europe, Asia Pacific
   - This affects database latency
   
   **Pricing Plan:**
   - Select **"Free"** plan (good for starting)
   - Free tier includes:
     - 500 MB database
     - 2 GB bandwidth
     - Unlimited API requests
     - Perfect for development and small projects

4. Click **"Create new project"**
5. Wait 2-3 minutes for Supabase to set up your project (you'll see a progress screen)

## 🔑 Step 3: Get Your Database Connection String

Once your project is ready:

1. **Go to Project Settings:**
   - In your project dashboard, click the **⚙️ Settings icon** (gear icon, usually bottom left sidebar)
   - Or click **"Project Settings"** from the left menu

2. **Navigate to Database:**
   - In the Settings page, click **"Database"** from the left sidebar
   - You'll see several sections

3. **Find Connection String:**
   - Scroll down to the **"Connection string"** section
   - You'll see different connection string formats
   - Look for the **"URI"** tab or **"Connection pooling"** section

4. **Copy the Connection String:**
   - You'll see something like:
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
     ```
   - **Click the "Copy" button** or select and copy the entire string
   - **IMPORTANT**: Replace `[YOUR-PASSWORD]` with the password you created in Step 2
   - The final string should look like:
     ```
     postgresql://postgres:MySecurePass123!@#@db.xxxxx.supabase.co:5432/postgres
     ```

### Alternative: Build Connection String Manually

If you prefer to build it yourself:

postgresql://postgres:OhnJM565GFEX7dz9@db.zjbuutlrqzpfpbnavhfo.supabase.co:5432/postgres
1. In **Settings → Database**, you'll see:
   - **Host**: `db.xxxxx.supabase.co`
   - **Database name**: `postgres`
   - **Port**: `5432`
   - **User**: `postgres`
   - **Password**: (the one you created)

2. Build the connection string:
   ```
   postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
   ```
   
   Example:
   ```
   postgresql://postgres:MySecurePass123!@#@db.abcdefghijklmnop.supabase.co:5432/postgres
   ```

## 🔒 Step 4: Get Connection Pooling URL (Recommended)

For better performance with serverless functions (like Vercel), use the **Connection Pooling** URL:

1. In **Settings → Database**
2. Scroll to **"Connection pooling"** section
3. Look for **"Connection string"** with **"Session mode"** or **"Transaction mode"**
4. Copy the connection string (it will have a different port, usually `6543` or `5432`)
5. Format: `postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:6543/postgres?pgbouncer=true`

**Why use pooling?**
- Better for serverless functions
- Handles many connections efficiently
- Recommended for Vercel deployments

## 📋 Step 5: Test Your Connection (Optional)

You can test if your connection string works:

1. **Using psql** (if installed):
   ```bash
   psql "postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres"
   ```

2. **Using Django** (local test):
   - Add `DATABASE_URL` to your local `.env` file
   - Run: `python manage.py migrate`
   - If it works, you'll see migrations applied

## 🎯 Step 6: Use in Vercel

1. **Copy your connection string** (from Step 3 or 4)
2. **Go to Vercel** project settings
3. **Add Environment Variable:**
   - Name: `DATABASE_URL`
   - Value: Paste your connection string
   - Environment: Select all (Production, Preview, Development)
4. **Save and redeploy**

## ⚙️ Step 7: Configure Django for Supabase

Your Django settings are already configured to use `DATABASE_URL` via `dj-database-url`, so it should work automatically!

However, if you need to verify:

1. Your `settings.py` should have:
   ```python
   import dj_database_url
   
   DATABASES = {
       'default': dj_database_url.config(
           default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
           conn_max_age=600
       )
   }
   ```

2. This will automatically use `DATABASE_URL` environment variable when set

## 🗄️ Step 8: Run Migrations

After setting up the database:

1. **Locally** (to test):
   ```bash
   python manage.py migrate
   ```

2. **On Vercel** (after deployment):
   - You can run migrations via Vercel's function logs
   - Or use a migration script
   - Or run migrations manually after first deployment

## 🔐 Security Best Practices

1. **Never commit your connection string to Git**
   - It contains your password
   - Always use environment variables

2. **Use different passwords for different environments**
   - Development database: one password
   - Production database: different password

3. **Rotate passwords regularly**
   - In Supabase: Settings → Database → Reset database password

4. **Use Connection Pooling for production**
   - Better performance
   - Handles connection limits better

## 📊 Step 9: Access Supabase Dashboard

You can manage your database through Supabase:

1. **Table Editor**: View and edit data
   - Left sidebar → "Table Editor"
   - See all your Django tables after migrations

2. **SQL Editor**: Run SQL queries
   - Left sidebar → "SQL Editor"
   - Write custom queries

3. **Database**: View schema
   - Left sidebar → "Database"
   - See tables, relationships, etc.

## 🆘 Troubleshooting

### Connection Refused
- **Check password**: Make sure you replaced `[YOUR-PASSWORD]` in the connection string
- **Check host**: Verify the host is correct
- **Check firewall**: Supabase allows connections from anywhere by default

### Authentication Failed
- **Wrong password**: Double-check the password you created
- **URL encoding**: If password has special characters, they might need URL encoding
  - Example: `@` becomes `%40`, `#` becomes `%23`
  - Or use Supabase's connection string builder

### Connection Timeout
- **Check region**: Make sure you selected the right region
- **Check network**: Verify your internet connection
- **Try connection pooling URL**: Use port 6543 instead of 5432

### Can't Find Connection String
- **Look in Settings → Database**: It's always there
- **Check Connection Pooling section**: Sometimes it's under pooling
- **Use the manual method**: Build it from Host, Port, Database, User, Password

## ✅ Checklist

Before using in Vercel, make sure you have:

- [ ] Created Supabase account
- [ ] Created a new project
- [ ] Saved your database password securely
- [ ] Copied the connection string
- [ ] Replaced `[YOUR-PASSWORD]` with actual password
- [ ] Tested connection (optional but recommended)
- [ ] Added `DATABASE_URL` to Vercel environment variables
- [ ] Ready to deploy!

## 📝 Example Connection Strings

**Standard Connection:**
```
postgresql://postgres:MyPassword123!@db.abcdefghijklmnop.supabase.co:5432/postgres
```

**Connection Pooling (Recommended for Vercel):**
```
postgresql://postgres:MyPassword123!@db.abcdefghijklmnop.supabase.co:6543/postgres?pgbouncer=true
```

**With URL-encoded special characters:**
If your password is `Pass@123#`, it becomes `Pass%40123%23`:
```
postgresql://postgres:Pass%40123%23@db.xxxxx.supabase.co:5432/postgres
```

## 🎉 Next Steps

1. ✅ Copy your connection string
2. ✅ Add it to Vercel as `DATABASE_URL`
3. ✅ Deploy your Django API
4. ✅ Run migrations
5. ✅ Test your API endpoints

---

**Need Help?**
- Supabase Docs: [supabase.com/docs](https://supabase.com/docs)
- Supabase Discord: Community support
- Check your project's "Support" section in Supabase dashboard
