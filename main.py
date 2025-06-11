import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import math
import subprocess
import threading
import re

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
    return file_path

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    return folder_path

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_video_duration(input_path):
    try:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        return duration
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
        messagebox.showerror("Error", f"Unable to determine video duration: {e}")
        return 0

def cut_video_ffmpeg(input_path, output_folder, mode, param, progress_var, status_label):
    try:
        if not check_ffmpeg():
            messagebox.showerror("Error", "FFmpeg is not installed or added to PATH")
            return

        if not os.path.isfile(input_path):
            messagebox.showerror("Error", "The specified video file is not exist")
            return

        duration = get_video_duration(input_path)
        if duration == 0:
            messagebox.showerror("Error", "Unable to determine video duration")
            return

        if mode == "count":
            num_segments = int(param)
            segment_duration = duration / num_segments
        else:
            segment_duration = float(param)
            num_segments = math.ceil(duration / segment_duration)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_pattern = os.path.join(output_folder, f"{base_name}_part%03d.mp4")

        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-r", "30",
            "-f", "segment",
            "-segment_time", str(segment_duration),
            "-reset_timestamps", "1",
            "-map", "0",
            output_pattern
        ]

        status_label.config(text="Start proccesing...")
        process = subprocess.run(cmd, capture_output=True, text=True)
        if process.returncode != 0:
            error_msg = process.stderr
            messagebox.showerror("Error", f"FFmpeg error: {error_msg}")
            return

        for i in range(num_segments):
            output_file = os.path.join(output_folder, f"{base_name}_part{i:03d}.mp4")
            if os.path.exists(output_file):
                progress_var.set(((i + 1) / num_segments) * 100)
                status_label.config(text=f"Processing: {i+1}/{num_segments} segment")
                root.update()
            else:
                messagebox.showwarning("Warning", f"Segment {i+1} not created")

        progress_var.set(100)
        status_label.config(text="Complete!")
        messagebox.showinfo("Success", "Video has successfully cut and adopted to TikTok!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        status_label.config(text="Proccessing error")
        progress_var.set(0)

def start_processing(input_path, output_folder, mode, param, progress_var, status_label):
    if not input_path or not os.path.exists(input_path):
        messagebox.showerror("Error", "Choose video")
        return
    if not output_folder:
        messagebox.showerror("Error", "Select a folder to save")
        return
    try:
        param_value = float(param)
        if param_value <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Enter a valid parameter value (positive number)")
        return

    status_label.config(text="Preparation...")
    thread = threading.Thread(target=cut_video_ffmpeg, args=(input_path, output_folder, mode, param, progress_var, status_label))
    thread.start()

def main():
    global root
    root = tk.Tk()

    root.title("Quick editor for TikTok (FFmpeg)")
    root.geometry("600x600")

    tk.Label(root, text="Select a video").pack(pady=5)
    video_path_var = tk.StringVar()
    tk.Entry(root, textvariable=video_path_var, width=40).pack()
    tk.Button(root, text="Select", command=lambda: video_path_var.set(select_file())).pack()

    tk.Label(root, text="Select a folder to save").pack(pady=5)
    folder_path_var = tk.StringVar()
    tk.Entry(root, textvariable=folder_path_var, width=40).pack()
    tk.Button(root, text="Select", command=lambda: folder_path_var.set(select_folder())).pack()

    tk.Label(root, text="Cutting mode").pack(pady=5)
    mode_var = tk.StringVar(value="count")
    tk.Radiobutton(root, text="By number of segments", variable=mode_var, value="count").pack()
    tk.Radiobutton(root, text="By length of segments (sec)", variable=mode_var, value="length").pack()

    tk.Label(root, text="Enter parameter (number or sec)").pack(pady=5)
    param_var = tk.StringVar()
    tk.Entry(root, textvariable=param_var).pack()

    progress_var = tk.DoubleVar(value=0.0)
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.pack(fill=tk.X, padx=20, pady=10)

    status_label = tk.Label(root, text="Ready to go")
    status_label.pack(pady=5)

    tk.Button(root, text="Start processing",
              command=lambda: start_processing(
                  video_path_var.get(),
                  folder_path_var.get(),
                  mode_var.get(),
                  param_var.get(),
                  progress_var,
                  status_label
              )).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()