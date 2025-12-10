#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

BUCKET_NAME = "portfolio-media"
MEDIA_DIRS = ["images", "videos", "audio"]

def upload_directory(local_dir):
    """Upload all files from a directory to R2 bucket"""
    print(f"\n🚀 Uploading {local_dir}/...")

    for root, dirs, files in os.walk(local_dir):
        # Skip .DS_Store files
        files = [f for f in files if not f.startswith('.')]

        for file in files:
            local_path = os.path.join(root, file)
            # R2 key is the relative path from project root
            r2_key = local_path

            print(f"  Uploading {local_path}...")

            cmd = [
                "wrangler", "r2", "object", "put",
                f"{BUCKET_NAME}/{r2_key}",
                f"--file={local_path}"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"  ❌ Error uploading {local_path}: {result.stderr}")
            else:
                print(f"  ✅ Uploaded {r2_key}")

if __name__ == "__main__":
    print("📦 Starting upload to Cloudflare R2...")
    print(f"Bucket: {BUCKET_NAME}\n")

    for media_dir in MEDIA_DIRS:
        if os.path.exists(media_dir):
            upload_directory(media_dir)
        else:
            print(f"⚠️  Directory {media_dir} not found, skipping...")

    print("\n✨ Upload complete!")
