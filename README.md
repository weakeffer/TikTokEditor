# TikTokEditor
A GUI application for splitting videos into segments with automatic vertical (9:16) format adaptation for TikTok
![image](https://github.com/user-attachments/assets/478aef07-4422-4186-bc0c-1e9dedaa5fef)

✨ Key Features
Video segmentation:

By number of segments

By segment duration (in seconds)

Automatic vertical format adaptation (1080x1920)

Progress bar with real-time status updates

Supported formats: MP4, AVI, MOV

🛠 Tech Stack
Python 3.10+

Tkinter (GUI interface)

FFmpeg (video processing)

Threading (background processing)

⚙️ Installation
1. Ensure FFmpeg is installed and added to PATH

2. Clone the repository:

git clone https://github.com/weakeffer/TikTokEditor.git

cd TikTokEditor

4. Install dependencies:
   
pip install -r requirements.txt

🚀 How to Use
Launch the application:

python main.py

2. Interface workflow:

Select input video file

Choose output directory

Select segmentation mode:

"By number of segments" - divides into X equal parts

"By length of segments" - divides by time duration (seconds)

Click "Start processing"
