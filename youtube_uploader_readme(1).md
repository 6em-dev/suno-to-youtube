# YouTube Auto-Uploader Setup Guide

This tutorial explains how to set up and run the automated YouTube uploader for your Suno AI songs.

## Prerequisites

### Software Requirements
- Python 3.7 or higher
- Git (optional, for cloning repositories)

### Required Files
Make sure you have these files in your project directory:
- `youtube_uploader.py` - The main uploader script
- `input.txt` - Contains your video filenames and URLs
- `download.sh` (Linux/Mac) or `download.bat` (Windows) - For downloading videos
- `db/` folder - Where your downloaded videos will be stored

## Step 1: Install Python Dependencies

### Linux/Mac:
```bash
pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib schedule
```

### Windows:
```cmd
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib schedule
```

## Step 2: Set Up YouTube API Credentials

### 2.1 Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project" or select an existing project
3. Give your project a name (e.g., "YouTube Auto Uploader")

### 2.2 Enable YouTube Data API v3
1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "YouTube Data API v3"
3. Click on it and press "Enable"

### 2.3 Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in required fields (App name, User support email, Developer email)
   - Add your email to test users
4. For Application type, choose "Desktop application"
5. Give it a name (e.g., "YouTube Uploader")
6. Click "Create"
7. Download the JSON file and rename it to `credentials.json`
8. Place `credentials.json` in the same folder as `youtube_uploader.py`

## Step 3: Download Your Videos

### Linux/Mac:
Make the download script executable and run it:
```bash
chmod +x download.sh
./download.sh
```

### Windows:
Run the batch file:
```cmd
download.bat
```

This will download all videos from `input.txt` into the `db/` folder.

## Step 4: Configure the Uploader

Open `youtube_uploader.py` and modify these settings if needed:

```python
self.video_folder = "db"  # Folder containing your videos
self.info_file = "input.txt"  # File with video info
```

You can also change the upload privacy setting:
```python
'privacyStatus': 'public'  # Options: 'public', 'private', 'unlisted'
```

## Step 5: Run the Uploader

### Linux/Mac:
```bash
python3 youtube_uploader.py
```

### Windows:
```cmd
python youtube_uploader.py
```

## How It Works

### First Run Authentication
- The script will open a web browser for Google OAuth
- Log in with your Google account
- Grant permissions for YouTube access
- The script will save authentication tokens for future use

### Upload Schedule
- First video uploads immediately
- Subsequent videos upload every 3 hours automatically
- Videos are uploaded in the order they appear in `input.txt`

### Video Information
Each video gets:
- **Title**: The filename without the .mp4 extension
- **Description**: Song name + Suno.com URL + "Songs made by Lamp"
- **Tags**: music, lamp, suno
- **Category**: Music

## File Structure

Your project should look like this:
```
project-folder/
├── youtube_uploader.py
├── input.txt
├── credentials.json
├── download.sh (Linux/Mac)
├── download.bat (Windows)
└── db/
    ├── Song1.mp4
    ├── Song2.mp4
    └── ...
```

## Troubleshooting

### "Authentication failed"
- Make sure `credentials.json` is in the correct location
- Verify YouTube Data API v3 is enabled
- Check that OAuth consent screen is configured

### "Video file not found"
- Run the download script first to get all videos
- Check that the `db/` folder exists and contains videos
- Verify filenames in `input.txt` match downloaded files

### "HTTP error occurred"
- Check your internet connection
- Verify your YouTube channel is set up properly
- Make sure you haven't exceeded API quotas

### "Permission denied" (Linux/Mac)
- Make sure download script is executable: `chmod +x download.sh`
- Run with proper permissions: `sudo python3 youtube_uploader.py` (if needed)

## Stopping the Uploader

To stop the uploader:
- Press `Ctrl+C` in the terminal
- The script will finish the current upload and then stop

## Notes

- The uploader will skip videos that don't exist in the `db/` folder
- Upload progress is saved - if you restart, it continues from where it left off
- Each video upload takes a few minutes depending on file size and internet speed
- YouTube has daily upload quotas - if you hit limits, wait 24 hours

## Security Tips

- Keep your `credentials.json` file secure and don't share it
- The `token.pickle` file contains your authentication tokens - keep it private
- Consider using a dedicated Google account for automation

## Support

If you encounter issues:
1. Check the error messages in the terminal
2. Verify all files are in the correct locations
3. Ensure your Google Cloud project is set up correctly
4. Check YouTube's terms of service for automated uploads