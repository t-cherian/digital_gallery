import os
import shutil
import sys
from PIL import Image
from mutagen import File
from datetime import datetime

def get_file_metadata(file_path):
    """Get the creation date of the file."""
    try:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            img = Image.open(file_path)
            exif_data = img._getexif()
            if exif_data is not None:
                for tag, value in exif_data.items():
                    if tag == 36867:  # DateTimeOriginal
                        return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
        elif file_path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            audio = File(file_path)
            # Use "creation_time" or "date" for video files
            if audio is not None:
                if 'creation_time' in audio:
                    return datetime.fromtimestamp(audio['creation_time'].get(0))
                elif 'date' in audio:
                    return datetime.fromtimestamp(int(audio['date']))
        # Fallback to file modification time if no metadata is found
        return datetime.fromtimestamp(os.path.getmtime(file_path))
    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")
    return None

def copy_files(src_folder, dest_folder, log_file):
    """Scan the folder recursively and copy files with metadata."""
    with open(log_file, 'w') as log:
        for root, _, files in os.walk(src_folder):
            for file in files:
                file_path = os.path.join(root, file)
                metadata_date = get_file_metadata(file_path)

                if metadata_date:
                    year = str(metadata_date.year)
                    month = f"{metadata_date.month:02d}"

                    # Create year/month directory structure
                    dest_dir = os.path.join(dest_folder, year, month)
                    os.makedirs(dest_dir, exist_ok=True)

                    dest_file_path = os.path.join(dest_dir, file)

                    # Handle file naming conflicts
                    if os.path.exists(dest_file_path):
                        base, extension = os.path.splitext(file)
                        counter = 1
                        while os.path.exists(dest_file_path):
                            dest_file_path = os.path.join(dest_dir, f"{base}_{counter}{extension}")
                            counter += 1

                    # Copy the file
                    shutil.copy2(file_path, dest_file_path)
                    print(f"Copied: {file_path} to {dest_file_path}")
                else:
                    # Log skipped files due to missing metadata
                    log.write(f"Skipped (no valid metadata): {file_path}\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <source_folder> <destination_folder> <log_file>")
        sys.exit(1)

    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]
    log_file = sys.argv[3]

    if not os.path.exists(source_folder):
        print(f"Source folder does not exist: {source_folder}")
        sys.exit(1)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    copy_files(source_folder, destination_folder, log_file)
