# Deploying Django API to Vercel

This guide will help you deploy your Django REST API to Vercel using the web dashboard.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps (Using Vercel Website)

### Step 1: Push Your Code to Git

Make sure your code is pushed to a Git repository (GitHub, GitLab, or Bitbucket). If you haven't already:

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Import Project to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click on **"Add New..."** button (or **"New Project"**)
3. You'll see options to import from:
   - **GitHub** (most common)
   - **GitLab**
   - **Bitbucket**
4. Click on your Git provider and authorize Vercel if needed
5. Select your repository from the list
6. Click **"Import"**

### Step 3: Configure Project Settings

Vercel will auto-detect your project, but verify these settings:

1. **Project Name**: You can change it or keep the default
2. **Root Directory**: Should be `.` (current directory) - leave as default
3. **Framework Preset**: Vercel may auto-detect, but you can leave it or select "Other"
4. **Build Command**: Leave empty (Django doesn't need a build step)
5. **Output Directory**: Leave empty
6. **Install Command**: `pip install -r requirements.txt` (should auto-detect)

**Important**: Make sure the `vercel.json` file is in your repository root.

### Step 4: Add Environment Variables

**Before clicking Deploy**, add your environment variables:

1. In the project configuration page, scroll down to **"Environment Variables"**
2. Click **"Add"** for each variable:

   **Required Variables:**
   - **Name**: `SECRET_KEY`
     - **Value**: Your Django secret key (generate a new one for production)
     - **Environment**: Select all (Production, Preview, Development)
   
   - **Name**: `DEBUG`
     - **Value**: `False` (for production)
     - **Environment**: Production only
   
   - **Name**: `DATABASE_URL`
     - **Value**: Your database connection string (e.g., `postgresql://user:password@host:port/dbname`)
     - **Environment**: Select all
   
   **Optional but Recommended:**
   - **Name**: `VERCEL_URL`
     - **Value**: Leave empty (Vercel sets this automatically)
     - **Environment**: All

3. Click **"Add"** after entering each variable

### Step 5: Deploy

1. Click the **"Deploy"** button at the bottom
2. Wait for the deployment to complete (usually 2-5 minutes)
3. You'll see build logs in real-time
4. Once complete, you'll get a deployment URL like: `https://your-project-name.vercel.app`

### Step 6: Verify Deployment

1. Click on your deployment to view details
2. Test your API endpoints using the provided URL
3. Check the **"Functions"** tab to see your serverless function
4. View **"Logs"** if there are any issues

### Step 7: Set Up Production Domain (Optional)

1. Go to your project dashboard
2. Click **"Settings"** → **"Domains"**
3. Add your custom domain if you have one
4. Follow the DNS configuration instructions

## Alternative: Using Vercel CLI (Optional)

If you prefer using the command line:

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

## Important Notes

### Database Considerations

Vercel serverless functions are stateless and have execution time limits. For production:

1. **Use an external database**: Vercel doesn't support persistent file storage, so you cannot use SQLite. Use:
   - PostgreSQL (recommended): Use services like [Supabase](https://supabase.com), [Neon](https://neon.tech), or [Railway](https://railway.app)
   - MySQL: Use services like [PlanetScale](https://planetscale.com)

2. **Update DATABASE_URL**: Set the `DATABASE_URL` environment variable in Vercel with your database connection string.

### Static Files

Static files are handled by WhiteNoise middleware. Make sure to:
1. Run `python manage.py collectstatic` before deployment (or add it to a build script)
2. Static files will be served from the serverless function

### CORS Configuration

Your CORS settings are already configured in `settings.py`. Make sure to add your Vercel API domain to `CORS_ALLOWED_ORIGINS` if needed.

### Cold Starts

Serverless functions may experience cold starts (initial delay on first request). This is normal for serverless platforms.

## Testing Locally

You can test the Vercel deployment locally:

```bash
vercel dev
```

This will start a local server that mimics Vercel's serverless environment.

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **Database Connection**: Ensure `DATABASE_URL` is set correctly
3. **Static Files**: Run `collectstatic` before deployment
4. **Timeout Errors**: Vercel has execution time limits. Optimize slow operations or use background jobs

### Viewing Logs

View deployment logs in the Vercel dashboard:
1. Go to your project
2. Click on a deployment
3. View the build and function logs

## Production Checklist

- [ ] Set `DEBUG=False` in environment variables
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure external database
- [ ] Set up proper CORS origins
- [ ] Run `collectstatic` (or automate it)
- [ ] Test all API endpoints
- [ ] Monitor function logs for errors

## Updating Your Deployment

After making changes to your code:

1. Push your changes to Git:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. Vercel will automatically detect the push and start a new deployment
3. You can also manually trigger a redeploy from the Vercel dashboard:
   - Go to your project
   - Click on **"Deployments"**
   - Click the **"..."** menu on any deployment
   - Select **"Redeploy"**

## Managing Environment Variables

To add or update environment variables after deployment:

1. Go to your project on Vercel
2. Click **"Settings"** → **"Environment Variables"**
3. Add, edit, or delete variables as needed
4. **Important**: After changing environment variables, you need to redeploy:
   - Go to **"Deployments"**
   - Click **"..."** → **"Redeploy"** on the latest deployment

## Support

For more information, see:
- [Vercel Python Documentation](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
