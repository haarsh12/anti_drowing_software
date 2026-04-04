# Vercel Deployment Guide

## Prerequisites
- GitHub account
- Vercel account (free)
- Your backend deployed and accessible via public URL

## Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

## Step 2: Deploy to Vercel

### Option A: Vercel Dashboard (Recommended)
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Import your repository
5. Configure project settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend_anti`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### Option B: Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend_anti

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? (select your account)
# - Link to existing project? N
# - Project name: anti-drowning-dashboard
# - Directory: ./
```

## Step 3: Configure Environment Variables

In Vercel Dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variables:

### Production Environment Variables:
```
Name: VITE_API_BASE_URL
Value: https://your-backend-domain.com/api
Environment: Production
```

### Preview Environment Variables:
```
Name: VITE_API_BASE_URL
Value: https://your-staging-backend.com/api
Environment: Preview
```

### Development Environment Variables:
```
Name: VITE_API_BASE_URL
Value: http://localhost:8000/api
Environment: Development
```

## Step 4: Backend Configuration

Your backend needs to be accessible from the internet. Options:

### Option A: Deploy Backend to Cloud
- **Railway**: Easy Python deployment
- **Heroku**: Popular platform
- **DigitalOcean**: VPS hosting
- **AWS/GCP**: Cloud platforms

### Option B: Expose Local Backend (Development Only)
```bash
# Install ngrok
npm install -g ngrok

# Expose your local backend
ngrok http 8000

# Use the ngrok URL in VITE_API_BASE_URL
# Example: https://abc123.ngrok.io/api
```

## Step 5: Update CORS Settings

Update your backend CORS configuration to allow your Vercel domain:

```python
# In your FastAPI backend (main.py)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-vercel-app.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Step 6: Test Deployment

1. **Check build logs** in Vercel dashboard
2. **Visit your deployed URL**
3. **Test API connectivity**:
   - Open browser developer tools
   - Check Network tab for API calls
   - Verify no CORS errors

## Step 7: Custom Domain (Optional)

1. In Vercel dashboard, go to "Domains"
2. Add your custom domain
3. Configure DNS records as instructed
4. Update environment variables if needed

## Troubleshooting

### Build Errors
```bash
# Check build locally
cd frontend_anti
npm run build

# Fix any build errors before deploying
```

### API Connection Issues
1. **Check environment variables** in Vercel dashboard
2. **Verify backend URL** is accessible
3. **Check CORS configuration** in backend
4. **Check browser console** for errors

### Environment Variable Issues
```bash
# Test locally with production URL
VITE_API_BASE_URL=https://your-backend.com/api npm run dev
```

## Automatic Deployments

Vercel automatically deploys when you push to GitHub:
- **Main branch** → Production deployment
- **Other branches** → Preview deployments

## Performance Optimization

1. **Enable compression** (automatic in Vercel)
2. **Optimize images** before deployment
3. **Use CDN** for static assets (automatic in Vercel)
4. **Enable caching** headers

## Security Considerations

1. **Never commit** `.env` files with secrets
2. **Use environment variables** for all configuration
3. **Enable HTTPS** (automatic in Vercel)
4. **Configure proper CORS** in backend

## Monitoring

1. **Vercel Analytics**: Built-in performance monitoring
2. **Error tracking**: Check Vercel function logs
3. **API monitoring**: Monitor your backend separately

## Example URLs

After deployment, your URLs will be:
- **Production**: `https://anti-drowning-dashboard.vercel.app`
- **Preview**: `https://anti-drowning-dashboard-git-feature-username.vercel.app`

## Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] Vercel project created
- [ ] Environment variables configured
- [ ] Backend CORS updated
- [ ] Build successful
- [ ] API connectivity tested
- [ ] Custom domain configured (optional)