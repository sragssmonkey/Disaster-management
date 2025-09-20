# Deployment Guide for Disaster Management App on Render

This guide will help you deploy your Django disaster management application on Render.

## Prerequisites

1. A GitHub account with your code repository
2. A Render account (free tier available)
3. Your project code pushed to GitHub

## Deployment Steps

### 1. Prepare Your Repository

Make sure all the deployment files are in your repository:
- `render.yaml` - Render configuration
- `Dockerfile` - Container configuration
- `requirements.txt` - Python dependencies
- `build.sh` - Build script
- `env.example` - Environment variables template

### 2. Deploy on Render

1. **Log in to Render**: Go to [render.com](https://render.com) and sign in
2. **Create New Web Service**: Click "New +" and select "Web Service"
3. **Connect Repository**: Connect your GitHub repository
4. **Configure Service**:
   - **Name**: `disaster-management`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `./Dockerfile`
   - **Plan**: Free (or choose a paid plan for better performance)

### 3. Environment Variables

Render will automatically set these from your `render.yaml`:
- `DJANGO_SECRET_KEY` (auto-generated)
- `DEBUG=False`
- `ALLOWED_HOSTS=disaster-management.onrender.com`

### 4. Database Setup

The application uses SQLite database:
- **File**: `db.sqlite3` (stored in the container)
- **No external database required**
- **Note**: Data will be lost when the container is redeployed (ephemeral storage)

### 5. Deploy

1. Click "Create Web Service"
2. Render will build and deploy your application
3. The build process will:
   - Install Python dependencies
   - Collect static files
   - Run database migrations
   - Start the Gunicorn server

### 6. Access Your Application

Once deployed, your app will be available at:
`https://disaster-management.onrender.com`

## Important Notes

### Security
- The app is configured for production with `DEBUG=False`
- CORS is properly configured for Render domains
- Static files are served via WhiteNoise

### Database
- Uses SQLite for both development and production
- Migrations run automatically during deployment
- **Important**: Data is ephemeral and will be lost on redeployment

### Static Files
- Static files are collected during build
- Served via WhiteNoise middleware
- No additional CDN configuration needed

### Performance
- Uses Gunicorn with 3 workers
- 120-second timeout for long-running requests
- Optimized Docker image with non-root user

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check that all dependencies are in `requirements.txt`
   - Ensure `Dockerfile` is in the root directory
   - Verify Python version compatibility

2. **Database Issues**:
   - Check that migrations are running successfully
   - Remember that SQLite data is ephemeral on Render

3. **Static Files Not Loading**:
   - Verify `STATIC_ROOT` is set correctly
   - Check that `collectstatic` runs during build

4. **CORS Issues**:
   - Update `CORS_ALLOWED_ORIGINS` in settings if needed
   - Check that your domain is in `ALLOWED_HOSTS`

### Logs

View deployment logs in the Render dashboard:
1. Go to your service
2. Click on "Logs" tab
3. Check for any error messages

## Local Development

To run locally with the same configuration:

1. Copy `env.example` to `.env`
2. Set `DEBUG=True` in your environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## Updates

To update your deployed application:
1. Push changes to your GitHub repository
2. Render will automatically detect changes and redeploy
3. The new version will be available after the build completes

## Support

For issues specific to Render deployment, check:
- [Render Documentation](https://render.com/docs)
- [Django on Render Guide](https://render.com/docs/deploy-django)
