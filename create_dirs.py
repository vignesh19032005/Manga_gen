import os

# Create media directories
media_path = os.path.join(os.path.dirname(__file__), 'media')
panels_path = os.path.join(media_path, 'panels')

os.makedirs(panels_path, exist_ok=True)
print(f"Created directories:\n{media_path}\n{panels_path}")
