# How to Add Environment Variables in Vercel Dashboard

This guide explains step-by-step how to add environment variables when deploying your Django API on Vercel.

## 📍 Where to Find Environment Variables

When you're on the **"Import Project"** or **"Configure Project"** page in Vercel, you'll see a section called **"Environment Variables"**. It's usually located:
- Below the build settings
- Before the "Deploy" button
- You may need to scroll down to see it

## 🎯 Step-by-Step Instructions

### Step 1: Locate the Environment Variables Section

1. After importing your repository, you'll be on the project configuration page
2. Scroll down past:
   - Project Name
   - Framework Preset
   - Build Settings
   - Root Directory
3. You'll see a section titled **"Environment Variables"** with a button that says **"Add"** or **"Add Variable"**

### Step 2: Add Your First Variable (SECRET_KEY)

1. **Click the "Add" button** (or "Add Variable" button)
2. A form will appear with three fields:
   - **Name** (or Key)
   - **Value**
   - **Environment** (checkboxes or dropdown)

3. **Fill in SECRET_KEY:**
   - **Name/Key field**: Type `SECRET_KEY` (exactly as shown, case-sensitive)
   - **Value field**: 
     - If you have a secret key, paste it here
     - If you need to generate one, you can:
       - Use Django's secret key generator online
       - Or run: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
       - Copy the generated key and paste it in the Value field
   - **Environment checkboxes**: 
     - ✅ Check **Production**
     - ✅ Check **Preview** 
     - ✅ Check **Development**
     - (Or select "All" if there's an option)

4. **Click "Add"** or "Save" button to save this variable

### Step 3: Add DEBUG Variable

1. **Click "Add" button again** to add another variable
2. **Fill in DEBUG:**
   - **Name/Key**: Type `DEBUG`
   - **Value**: Type `False` (capital F, lowercase rest)
   - **Environment**: 
     - ✅ Check **Production** only
     - ❌ Uncheck Preview and Development (or leave unchecked)
   - **Why?** You want DEBUG=False only in production, but True in development/preview

3. **Click "Add"** to save

### Step 4: Add DATABASE_URL Variable

1. **Click "Add" button again**
2. **Fill in DATABASE_URL:**
   - **Name/Key**: Type `DATABASE_URL`
   - **Value**: Your database connection string
     - **Format examples:**
       - PostgreSQL: `postgresql://username:password@host:port/database_name`
       - Example: `postgresql://myuser:mypass@db.example.com:5432/mydb`
     - **Where to get this?**
       - If using **Supabase**: Project Settings → Database → Connection String
       - If using **Neon**: Dashboard → Connection String
       - If using **Railway**: Service → Variables → DATABASE_URL
       - If using **PlanetScale**: Connect → Connection String
   - **Environment**: 
     - ✅ Check **Production**
     - ✅ Check **Preview**
     - ✅ Check **Development**
     - (Or select "All")

3. **Click "Add"** to save

### Step 5: Verify Your Variables

After adding all variables, you should see a list showing:
- ✅ SECRET_KEY (Production, Preview, Development)
- ✅ DEBUG (Production)
- ✅ DATABASE_URL (Production, Preview, Development)

## 🖼️ Visual Guide (What You'll See)

```
┌─────────────────────────────────────────┐
│  Environment Variables                   │
├─────────────────────────────────────────┤
│  [Add] or [Add Variable] button         │
│                                          │
│  ┌───────────────────────────────────┐ │
│  │ Name: [SECRET_KEY        ]        │ │
│  │ Value: [your-secret-key-here]     │ │
│  │ Environment: ☑ Production          │ │
│  │            ☑ Preview               │ │
│  │            ☑ Development           │ │
│  │ [Add] [Cancel]                     │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## ⚠️ Important Tips

### 1. **Case Sensitivity**
- Variable names are case-sensitive
- Use exactly: `SECRET_KEY`, `DEBUG`, `DATABASE_URL` (all uppercase)

### 2. **Value Format**
- **No quotes needed**: Don't wrap values in quotes unless the value itself contains quotes
- **Spaces matter**: Be careful with spaces before/after values
- **Special characters**: If your password has special characters, they should be URL-encoded in DATABASE_URL

### 3. **Environment Selection**
- **Production**: Used when your site is live (your-project.vercel.app)
- **Preview**: Used for preview deployments (branch deployments)
- **Development**: Used for local development with `vercel dev`

### 4. **When to Add Variables**
- ✅ **Best**: Add them BEFORE clicking "Deploy" (first time)
- ✅ **Alternative**: Add them after deployment, then redeploy

### 5. **Editing Variables Later**
If you need to edit variables after deployment:
1. Go to your project dashboard
2. Click **"Settings"** (top menu)
3. Click **"Environment Variables"** (left sidebar)
4. Find the variable and click **"Edit"** or the pencil icon
5. Make changes and save
6. **Important**: Redeploy your project for changes to take effect

## 🔍 Example: Complete Variable Setup

Here's what your environment variables section should look like:

| Name | Value | Environments |
|------|-------|--------------|
| `SECRET_KEY` | `django-insecure-abc123xyz...` | Production, Preview, Development |
| `DEBUG` | `False` | Production |
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` | Production, Preview, Development |

## 🚨 Common Mistakes to Avoid

1. ❌ **Forgetting to add variables before deploy** - Your app will fail
2. ❌ **Typos in variable names** - `SECRET_KEY` not `secret_key` or `Secret_Key`
3. ❌ **Adding quotes around values** - `"False"` instead of `False`
4. ❌ **Wrong environment selection** - DEBUG should be Production only
5. ❌ **Not redeploying after adding variables** - Changes won't take effect

## ✅ Checklist Before Deploying

- [ ] SECRET_KEY added (all environments)
- [ ] DEBUG set to False (Production only)
- [ ] DATABASE_URL added (all environments)
- [ ] All variable names are correct (case-sensitive)
- [ ] All values are correct (no extra spaces/quotes)
- [ ] Environment checkboxes are correct

## 🆘 If You Can't Find the Section

If you don't see "Environment Variables" on the import page:
1. You can still deploy first
2. After deployment, go to: **Project → Settings → Environment Variables**
3. Add your variables there
4. Then go to **Deployments → Latest → Redeploy**

## 📝 After Adding Variables

Once you've added all variables:
1. Review the list to make sure everything is correct
2. Scroll down and click the **"Deploy"** button
3. Wait for deployment to complete
4. Your variables will be available to your Django app!

---

**Need help?** If you're stuck, you can also add environment variables after deployment in the Settings page, then redeploy your project.
