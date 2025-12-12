# Quick Deploy to Vercel (Web Dashboard)

## 🚀 Quick Steps

### 1. Push Code to Git
```bash
git add .
git commit -m "Ready for Vercel"
git push
```

### 2. Go to Vercel Website
- Visit [vercel.com](https://vercel.com)
- Sign in or create account

### 3. Import Project
- Click **"Add New..."** → **"Project"**
- Connect your Git provider (GitHub/GitLab/Bitbucket)
- Select your repository
- Click **"Import"**

### 4. Configure (Before Deploy)
- **Project Name**: Keep default or change
- **Root Directory**: `.` (default)
- **Build Command**: Leave empty
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt` (auto-detected)

### 5. Add Environment Variables
Click **"Environment Variables"** and add:

| Variable | Value | Environment |
|----------|-------|-------------|
| `SECRET_KEY` | Your Django secret key | All |
| `DEBUG` | `False` | Production |
| `DATABASE_URL` | Your database URL | All |

### 6. Deploy
- Click **"Deploy"** button
- Wait 2-5 minutes
- Get your URL: `https://your-project.vercel.app`

### 7. Test
- Visit your deployment URL
- Test API endpoints
- Check logs if issues occur

## ⚠️ Important Notes

- **Database Required**: Vercel doesn't support SQLite. Use PostgreSQL (Supabase/Neon) or MySQL
- **Auto-Deploy**: Future git pushes automatically deploy
- **Environment Variables**: Add them before first deploy or redeploy after adding

## 📝 After Deployment

1. **View Logs**: Project → Deployments → Click deployment → Logs
2. **Update Variables**: Settings → Environment Variables → Redeploy after changes
3. **Custom Domain**: Settings → Domains → Add domain

## 🔧 Troubleshooting

- **Build Fails**: Check logs, ensure `requirements.txt` is correct
- **500 Errors**: Check environment variables, especially `DATABASE_URL`
- **Import Errors**: Ensure `vercel.json` is in root directory
