#!/usr/bin/env python3
"""
Update all media URLs to point to Cloudflare R2 bucket
"""
import json
import re

R2_BASE_URL = "https://pub-8ccc93469bb64db4aff58fd83b517c9d.r2.dev"

def update_html(file_path):
    """Update media URLs in HTML file"""
    print(f"Updating {file_path}...")

    with open(file_path, 'r') as f:
        content = f.read()

    # Replace all local media paths with R2 URLs
    # Pattern: data-media="videos/..." or data-media="images/..." or data-media="audio/..."
    content = re.sub(
        r'data-media="((?:videos|images|audio)/[^"]+)"',
        rf'data-media="{R2_BASE_URL}/\1"',
        content
    )

    # Also handle src attributes for images, videos, audio
    content = re.sub(
        r'src="((?:videos|images|audio)/[^"]+)"',
        rf'src="{R2_BASE_URL}/\1"',
        content
    )

    with open(file_path, 'w') as f:
        f.write(content)

    print(f"✅ Updated {file_path}")

def update_json(file_path):
    """Update media paths in JSON file"""
    print(f"Updating {file_path}...")

    with open(file_path, 'r') as f:
        data = json.load(f)

    def update_path(path):
        """Add R2 base URL to a path"""
        if isinstance(path, str) and (
            path.startswith('images/') or
            path.startswith('videos/') or
            path.startswith('audio/')
        ):
            return f"{R2_BASE_URL}/{path}"
        return path

    def update_dict_values(obj):
        """Recursively update all media paths in a dict/list structure"""
        if isinstance(obj, dict):
            # Handle audio JSON structure with 'path' keys
            if 'path' in obj:
                obj['path'] = update_path(obj['path'])
            return {k: update_dict_values(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [update_path(item) if isinstance(item, str) else update_dict_values(item) for item in obj]
        return obj

    updated_data = update_dict_values(data)

    with open(file_path, 'w') as f:
        json.dump(updated_data, f, indent=2)

    print(f"✅ Updated {file_path}")

if __name__ == "__main__":
    print("🔄 Updating media URLs to use Cloudflare R2...")
    print(f"R2 Base URL: {R2_BASE_URL}\n")

    # Update HTML file
    update_html("index.html")

    # Update JSON files
    update_json("js/project-images.json")
    update_json("js/project-audio.json")

    print("\n✨ All media URLs updated!")
    print("\nNext steps:")
    print("1. Test the site locally")
    print("2. Add media directories to .gitignore")
    print("3. Deploy to Vercel")
