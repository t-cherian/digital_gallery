import os
import random
import shutil
import argparse

def copy_random_files(input_dir, output_dir, percentage=10):
    """
    Recursively selects a percentage of files in each folder and copies them
    to the output folder while maintaining the folder structure.

    :param input_dir: Path to the input folder.
    :param output_dir: Path to the output folder.
    :param percentage: Percentage of files to select in each folder.
    """
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return
    
    for root, dirs, files in os.walk(input_dir):
        if not files:
            continue

        # Calculate the number of files to select
        num_files_to_select = max(1, len(files) * percentage // 100)
        selected_files = random.sample(files, num_files_to_select)
        
        # Construct the corresponding output directory
        relative_path = os.path.relpath(root, input_dir)
        target_dir = os.path.join(output_dir, relative_path)
        os.makedirs(target_dir, exist_ok=True)
        
        # Copy the selected files
        for file_name in selected_files:
            src_path = os.path.join(root, file_name)
            dest_path = os.path.join(target_dir, file_name)
            shutil.copy2(src_path, dest_path)
            print(f"Copied: {src_path} -> {dest_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy random 10% of files from input to output directory while maintaining folder structure.")
    parser.add_argument("input_dir", help="Path to the input directory.")
    parser.add_argument("output_dir", help="Path to the output directory.")
    parser.add_argument("--percentage", type=int, default=10, help="Percentage of files to select in each folder (default: 10%).")
    args = parser.parse_args()

    copy_random_files(args.input_dir, args.output_dir, args.percentage)
