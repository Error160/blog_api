# Supabase Quick Reference - Get Database URL

## 🚀 Quick Steps

### 1. Sign Up & Create Project
- Go to [supabase.com](https://supabase.com)
- Sign up (GitHub recommended)
- Click **"New Project"**
- Enter project name
- **Create a strong password** (save it!)
- Choose region
- Click **"Create new project"**
- Wait 2-3 minutes

### 2. Get Connection String
1. Click **⚙️ Settings** (gear icon, bottom left)
2. Click **"Database"** (left sidebar)
3. Scroll to **"Connection string"** section
4. Find the **URI** format:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
5. **Copy the string**
6. **Replace `[YOUR-PASSWORD]`** with your actual password
7. Final format:
   ```
   postgresql://postgres:YourActualPassword123!@db.xxxxx.supabase.co:5432/postgres
   ```

### 3. Use in Vercel
- Go to Vercel project settings
- Add environment variable:
  - **Name**: `DATABASE_URL`
  - **Value**: Your connection string (with password replaced)
  - **Environment**: All (Production, Preview, Development)

## 🔗 Connection Pooling (Recommended for Vercel)

For better performance with serverless:

1. Same steps as above
2. In Database settings, find **"Connection pooling"** section
3. Copy the connection string (port 6543)
4. Format: `postgresql://postgres:password@db.xxxxx.supabase.co:6543/postgres?pgbouncer=true`

## ⚠️ Important

- ✅ Save your database password securely
- ✅ Never commit connection string to Git
- ✅ Use environment variables only
- ✅ Replace `[YOUR-PASSWORD]` in the connection string

## 📍 Where to Find It

```
Supabase Dashboard
  └── Your Project
      └── ⚙️ Settings (bottom left)
          └── Database (left sidebar)
              └── Connection string section
                  └── Copy URI
```

## 🆘 Troubleshooting

- **Can't find it?** → Settings → Database → Scroll down
- **Wrong password?** → Make sure you replaced `[YOUR-PASSWORD]`
- **Connection failed?** → Check password, host, and port

---

**Full Guide**: See `SUPABASE_SETUP.md` for detailed instructions with screenshots descriptions.
