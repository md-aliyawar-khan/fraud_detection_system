# Heroku Deployment Guide

This guide will walk you through deploying your Fraud Detection API to Heroku.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure your project is in a Git repository

## Step-by-Step Deployment

### 1. Prepare Your Project

Ensure your project has all the necessary files:
- `app.py` - Flask application
- `requirements.txt` - Python dependencies
- `Procfile` - Heroku process configuration
- `runtime.txt` - Python version specification
- Trained model files in `models/` directory

### 2. Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit for fraud detection API"
```

### 3. Login to Heroku

```bash
heroku login
```

### 4. Create Heroku App

```bash
heroku create your-fraud-detection-app-name
```

Replace `your-fraud-detection-app-name` with your desired app name (must be unique).

### 5. Add Heroku Remote

```bash
heroku git:remote -a your-fraud-detection-app-name
```

### 6. Deploy to Heroku

```bash
git add .
git commit -m "Deploy fraud detection API"
git push heroku main
```

### 7. Verify Deployment

```bash
heroku open
```

This will open your deployed app in the browser.

## Testing Your Deployed API

### 1. Health Check

```bash
curl https://your-fraud-detection-app-name.herokuapp.com/health
```

### 2. Single Prediction

```bash
curl -X POST https://your-fraud-detection-app-name.herokuapp.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "V1": -1.3598071336738,
    "V2": -0.0727811733098497,
    "V3": 2.53634673796914,
    "V4": 1.37815522427443,
    "V5": -0.338320769942518,
    "V6": 0.462387777762292,
    "V7": 0.239598554061257,
    "V8": 0.0986979012610507,
    "V9": 0.363786969611213,
    "V10": 0.0907941719789316,
    "V11": -0.551599533260813,
    "V12": -0.617800855762348,
    "V13": -0.991389847235408,
    "V14": -0.311169353699879,
    "V15": 1.46817697209427,
    "V16": -0.470400525259478,
    "V17": 0.207971241929242,
    "V18": 0.0257905801985591,
    "V19": 0.403992960255733,
    "V20": 0.251412098239705,
    "V21": -0.018306777944153,
    "V22": 0.277837575558899,
    "V23": -0.110473910188767,
    "V24": 0.0669280749146731,
    "V25": 0.128539358273528,
    "V26": -0.189114843888824,
    "V27": 0.133558376740387,
    "V28": -0.0210530534538215,
    "Amount": 149.62
  }'
```

## Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   heroku logs --tail
   ```
   Check the logs for specific error messages.

2. **Model Loading Issues**
   - Ensure model files are committed to Git
   - Check file paths in `app.py`
   - Verify model files are in the `models/` directory

3. **Memory Issues**
   - Heroku has memory limits
   - Consider using smaller model files
   - Optimize model size if needed

4. **Dependency Issues**
   - Check `requirements.txt` for correct versions
   - Ensure all dependencies are listed

### Useful Heroku Commands

```bash
# View app logs
heroku logs --tail

# Check app status
heroku ps

# Restart the app
heroku restart

# Scale the app
heroku ps:scale web=1

# View app info
heroku info
```

## Environment Variables (Optional)

If you need to set environment variables:

```bash
heroku config:set VARIABLE_NAME=value
```

## Monitoring

### Heroku Dashboard
- Visit [dashboard.heroku.com](https://dashboard.heroku.com)
- Select your app
- Monitor performance, logs, and errors

### Add-ons (Optional)
```bash
# Add monitoring
heroku addons:create papertrail:choklad

# Add logging
heroku addons:create logentries:le_tryit
```

## Cost Considerations

- **Free Tier**: No longer available on Heroku
- **Basic Dyno**: $7/month
- **Standard Dyno**: $25/month
- **Performance Dyno**: $250/month

## Security Best Practices

1. **Environment Variables**: Store sensitive data as config vars
2. **HTTPS**: Heroku provides SSL certificates automatically
3. **Input Validation**: Already implemented in the API
4. **Rate Limiting**: Consider adding rate limiting for production

## Performance Optimization

1. **Model Optimization**: Consider model compression
2. **Caching**: Implement response caching
3. **Database**: Add database for storing predictions (if needed)
4. **CDN**: Use CDN for static assets

## Next Steps

After successful deployment:

1. **Update Documentation**: Add your Heroku app URL to README
2. **Set Up Monitoring**: Configure alerts and monitoring
3. **Add Authentication**: Implement API key authentication
4. **Scale**: Monitor usage and scale as needed
5. **Backup**: Set up regular backups of your model

## Support

- **Heroku Documentation**: [devcenter.heroku.com](https://devcenter.heroku.com)
- **Heroku Support**: Available in your dashboard
- **Community**: Stack Overflow, Reddit r/Heroku 