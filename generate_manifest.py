import os
import json

def generate_manifest():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate media manifest (images + videos)
    media_manifest = {}
    image_base_dir = os.path.join(script_dir, "images/projects")
    video_base_dir = os.path.join(script_dir, "videos/projects")

    # Collect images
    for root, dirs, files in os.walk(image_base_dir):
        if root == image_base_dir:
            continue

        folder_name = os.path.relpath(root, image_base_dir)
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]

        if image_files:
            paths = [os.path.join("images/projects", folder_name, f) for f in image_files]
            paths.sort()
            media_manifest[folder_name] = paths

    # Collect videos and merge with images
    if os.path.exists(video_base_dir):
        for root, dirs, files in os.walk(video_base_dir):
            if root == video_base_dir:
                continue

            folder_name = os.path.relpath(root, video_base_dir)
            video_files = [f for f in files if f.lower().endswith(('.mp4', '.webm', '.ogg'))]  # Exclude .mov (source files)

            if video_files:
                video_paths = [os.path.join("videos/projects", folder_name, f) for f in video_files]
                video_paths.sort()
                # Add videos at the beginning of the gallery (or create new entry)
                if folder_name in media_manifest:
                    media_manifest[folder_name] = video_paths + media_manifest[folder_name]
                else:
                    media_manifest[folder_name] = video_paths

    image_output_path = os.path.join(script_dir, 'js/project-images.json')
    with open(image_output_path, 'w') as f:
        json.dump(media_manifest, f, indent=2)
    print(f"Image manifest generated at {image_output_path}")

    # Generate audio manifest
    audio_manifest = {}
    audio_base_dir = os.path.join(script_dir, "audio")

    if os.path.exists(audio_base_dir):
        for root, dirs, files in os.walk(audio_base_dir):
            if root == audio_base_dir:
                continue

            folder_name = os.path.relpath(root, audio_base_dir)
            # Map folder names to project IDs
            folder_to_project = {
                "solo-piano": "my-music/solo-piano",
                "electronic": "my-music/electronic",
                "ambient-electroacustic": "my-music/ambient-electroacoustic"
            }
            project_id = folder_to_project.get(folder_name, f"my-music/{folder_name}")

            audio_files = [f for f in files if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a'))]

            if audio_files:
                tracks = []
                for f in audio_files:
                    # Extract track name from filename
                    name = os.path.splitext(f)[0]
                    # Clean up common patterns
                    name = name.replace('---', ' - ').replace('-', ' ').replace('_', ' ')
                    tracks.append({
                        "name": name,
                        "path": os.path.join("audio", folder_name, f)
                    })
                tracks.sort(key=lambda x: x["name"])
                audio_manifest[project_id] = tracks

    audio_output_path = os.path.join(script_dir, 'js/project-audio.json')
    with open(audio_output_path, 'w') as f:
        json.dump(audio_manifest, f, indent=2)
    print(f"Audio manifest generated at {audio_output_path}")

if __name__ == "__main__":
    generate_manifest()
