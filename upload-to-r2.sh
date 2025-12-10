#!/bin/bash

# Upload images
echo "Uploading images..."
wrangler r2 object put portfolio-media/images --file=images --recursive

# Upload videos
echo "Uploading videos..."
wrangler r2 object put portfolio-media/videos --file=videos --recursive

# Upload audio
echo "Uploading audio..."
wrangler r2 object put portfolio-media/audio --file=audio --recursive

echo "Upload complete!"
