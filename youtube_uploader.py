import os
import time
import schedule
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import re

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

class YouTubeUploader:
    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.youtube = None
        self.current_index = 0
        self.video_info = []
        self.video_folder = "db"  # Change this to your video folder path
        self.info_file = "input.txt"  # Change this to your info file path
        
    def authenticate(self):
        """Authenticate with YouTube API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.youtube = build('youtube', 'v3', credentials=creds)
        print("YouTube API authenticated successfully!")
    
    def load_video_info(self):
        """Load video information from input.txt file"""
        if not os.path.exists(self.info_file):
            print(f"Info file {self.info_file} not found!")
            return False
        
        self.video_info = []
        with open(self.info_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 2:
                        filename = parts[0].strip()
                        song_url_raw = parts[1].strip()
                        
                        # Extract song name (everything before the file extension)
                        song_name = os.path.splitext(filename)[0]
                        
                        # Extract song ID from URL and create suno.com URL
                        song_id_match = re.search(r'([a-f0-9-]{36})', song_url_raw)
                        if song_id_match:
                            song_id = song_id_match.group(1)
                            song_url = f"https://suno.com/song/{song_id}"
                        else:
                            song_url = song_url_raw
                        
                        self.video_info.append({
                            'filename': filename,
                            'song_name': song_name,
                            'song_url': song_url
                        })
        
        print(f"Loaded {len(self.video_info)} video entries")
        return len(self.video_info) > 0
    
    def upload_video(self, video_path, title, description):
        """Upload a single video to YouTube"""
        if not self.youtube:
            print("YouTube API not authenticated!")
            return False
        
        try:
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': ['music', 'suno'],
                    'categoryId': '10',  # Music category channel ID if needed
                },
                'status': {
                    'privacyStatus': 'public'  # Change to 'private' or 'unlisted' if needed
                }
            }
            
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            print(f"Uploading video: {title}")
            response = request.execute()
            
            video_id = response['id']
            print(f"Video uploaded successfully! Video ID: {video_id}")
            print(f"Video URL: https://www.youtube.com/watch?v={video_id}")
            return True
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    
    def get_next_video(self):
        """Get the next video to upload"""
        if self.current_index >= len(self.video_info):
            print("No more videos to upload!")
            return None
        
        video_info = self.video_info[self.current_index]
        video_path = os.path.join(self.video_folder, video_info['filename'])
        
        if not os.path.exists(video_path):
            print(f"Video file not found: {video_path}")
            self.current_index += 1
            return self.get_next_video()  # Try next video
        
        return video_info, video_path
    
    def upload_next_video(self):
        """Upload the next video in sequence"""
        result = self.get_next_video()
        if not result:
            print("Upload sequence completed - no more videos to upload!")
            return False
        
        video_info, video_path = result
        
        # Create description
        description = f"{video_info['song_name']} - {video_info['song_url']}"
        
        # Upload video
        success = self.upload_video(
            video_path=video_path,
            title=video_info['song_name'],
            description=description
        )
        
        if success:
            self.current_index += 1
            print(f"Successfully uploaded video {self.current_index}/{len(self.video_info)}")
        else:
            print("Upload failed, will retry next time")
        
        return success
    
    def start_scheduler(self):
        """Start the upload scheduler"""
        print("Starting YouTube upload scheduler...")
        print("First upload will happen immediately, then every 3 hours")
        
        # Upload first video immediately
        self.upload_next_video()
        
        # Schedule uploads every 3 hours
        schedule.every(3).hours.do(self.upload_next_video)
        
        print("Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nScheduler stopped by user")

def main():
    uploader = YouTubeUploader()
    
    # Load video information
    if not uploader.load_video_info():
        print("Failed to load video information. Please check your input.txt file.")
        return
    
    # Authenticate with YouTube
    try:
        uploader.authenticate()
    except Exception as e:
        print(f"Authentication failed: {e}")
        print("Please make sure you have:")
        print("1. Created a YouTube API project in Google Cloud Console")
        print("2. Downloaded the credentials.json file")
        print("3. Enabled the YouTube Data API v3")
        return
    
    # Start the scheduler
    uploader.start_scheduler()

if __name__ == "__main__":
    main()
