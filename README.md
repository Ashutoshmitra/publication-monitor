# Publication Monitor

Automatically monitor and download digital publications from various platforms (currently supporting Issuu) and store them in Google Drive.

## Features

- Monitor multiple Issuu publishers for new publications
- Automatically download new publications published after a specified date
- Store publications in Google Drive
- Send email notifications when new publications are found
- Run automatically using GitHub Actions
- Extensible architecture for adding new publication sources

## Setup Instructions

### 1. Repository Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 2. Google Drive API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Drive API
4. Create OAuth 2.0 credentials:
   - Go to Credentials
   - Create OAuth client ID
   - Application type: Desktop application
   - Download the client configuration file
   - Rename it to `gdrive_credentials.json`
5. Create a folder in Google Drive for storing publications
6. Get the folder ID from the URL when inside the folder

### 3. Configuration

1. Copy `config.yaml` and modify according to your needs:
   - Update the Google Drive folder ID
   - Add your Issuu publishers
   - Configure email notifications

2. Set up GitHub repository secrets:
   ```
   GDRIVE_CREDENTIALS: Base64 encoded content of gdrive_credentials.json
   EMAIL_PASSWORD: Your email password or app-specific password
   ```

   To encode credentials:
   ```bash
   base64 -w 0 credentials/gdrive_credentials.json
   ```

### 4. First Run

1. Run the script locally first to authenticate with Google Drive:
   ```bash
   python -m src.main
   ```
2. Follow the authentication flow in your browser
3. The token will be saved for future use

## Adding New Publication Sources

1. Create a new monitor class in `src/monitors/`:
   ```python
   from .base import BaseMonitor
   
   class NewSourceMonitor(BaseMonitor):
       def check_new_publications(self):
           # Implementation
           pass
           
       def download_publication(self, publication, output_path):
           # Implementation
           pass
   ```

2. Update `config.yaml` to include the new source:
   ```yaml
   monitors:
     new_source:
       enabled: true
       # source-specific configuration
   ```

3. Add the new monitor in `src/main.py`:
   ```python
   if config["monitors"]["new_source"]["enabled"]:
       monitors.append(NewSourceMonitor(config["monitors"]["new_source"]))
   ```

## Monitoring and Maintenance

- Check GitHub Actions logs for execution status
- Monitor the email notifications for new publications
- Verify Google Drive storage usage periodically
- Update `min_date` in config.yaml as needed

## Limitations

- GitHub Actions free tier limitations:
  - 2,000 minutes per month
  - Runs every 12 hours (configurable)
- Google Drive storage limits based on your account
- Rate limiting by publication platforms

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

MIT License