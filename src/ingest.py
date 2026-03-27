import cv2
import os
import json
import whisper
import re  

def process_lecture(video_path):
    raw_name = os.path.basename(video_path).split('.')[0]
    lecture_name = re.sub(r'[^a-zA-Z0-9._-]', '_', raw_name)
    lecture_name = lecture_name.strip('_')
    
    base_dir = os.path.join("data", lecture_name)
    keyframes_dir = os.path.join(base_dir, "keyframes")
    os.makedirs(keyframes_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / (fps if fps > 0 else 30)

    print(f"🎬 Extracting frames for {lecture_name}...")

    interval_sec = 5 
    current_sec = 0
    while current_sec < duration_sec:
        frame_id = int(fps * current_sec)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ret, frame = cap.read()
        if ret:
            frame_filename = f"frame_{int(current_sec)}s.jpg"
            save_path = os.path.join(keyframes_dir, frame_filename)
            cv2.imwrite(save_path, frame)
        current_sec += interval_sec
    cap.release()

    print("🎙️ Transcribing audio with Whisper...")
    model = whisper.load_model("base") 
    result = model.transcribe(video_path)
    
    segments = []
    for seg in result['segments']:
        timestamp = int(seg['start'])
        closest_frame_time = (timestamp // 5) * 5
        img_path = os.path.join(keyframes_dir, f"frame_{closest_frame_time}s.jpg")
        
        segments.append({
            "start": seg['start'],
            "end": seg['end'],
            "text": seg['text'],
            "image_path": img_path
        })

    transcript_path = os.path.join(base_dir, "transcript.json")
    with open(transcript_path, "w") as f:
        json.dump(segments, f, indent=4)

    print(f"✅ Processing complete! Saved to {base_dir}")
    return segments, lecture_name