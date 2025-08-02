# Frontend Deployment Guide

## Azure Static Web Apps Deployment

### Prerequisites
1. Azure account with access to create Azure Static Web Apps
2. GitHub repository with the frontend code
3. Backend API deployed and running (e.g., https://perfburger-chatbot.azurewebsites.net)

### Steps to Deploy

#### 1. Create Azure Static Web App
1. Go to Azure Portal
2. Create a new resource → Static Web Apps
3. Configure:
   - **Name**: `perfburger-frontend` (or your preferred name)
   - **Subscription**: Choose your subscription
   - **Resource Group**: Use existing or create new
   - **Source**: GitHub
   - **Organization**: Your GitHub username
   - **Repository**: `ai-chatbot-perf-burger`
   - **Branch**: `main`
   - **Build Presets**: React
   - **App location**: `/frontend`
   - **Api location**: `` (leave empty, we use separate backend)
   - **Output location**: `dist`

#### 2. Configure GitHub Secrets
The Azure portal will automatically create a GitHub secret called:
`AZURE_STATIC_WEB_APPS_API_TOKEN_PERFBURGER_FRONTEND`

#### 3. Update Workflow (if needed)
The workflow file is already created at:
`.github/workflows/azure-static-web-apps-perfburger-frontend.yml`

#### 4. Environment Configuration
The frontend automatically detects:
- **Development**: `http://localhost:5000` (backend)
- **Production**: `https://perfburger-chatbot-a6eph3fsavbwc5bm.westeurope-01.azurewebsites.net` (backend)

### Accessing the Deployed Frontend
After deployment, your frontend will be available at:
`https://<app-name>.<random-id>.azurestaticapps.net`

### Custom Domain (Optional)
You can configure a custom domain in the Azure Static Web Apps settings.

### CORS Configuration
The backend is already configured to allow requests from:
- `*.azurestaticapps.net` domains
- Development localhost URLs

### Troubleshooting
1. **Build fails**: Check the GitHub Actions logs
2. **API calls fail**: Verify backend CORS configuration
3. **Routes not working**: Check `staticwebapp.config.json` configuration
