import os
import sys
import argparse
from visbrain.gui import Sleep

# Import the hypnogram generation function
import importlib.util
import sys

# Dynamically import the function from the file with hyphen in name
spec = importlib.util.spec_from_file_location(
    "yasa_hypno_module", 
    os.path.join(os.path.dirname(__file__), "yasa-hypno_to_visbrain-txt.py")
)
yasa_hypno_module = importlib.util.module_from_spec(spec)
sys.modules["yasa_hypno_module"] = yasa_hypno_module
spec.loader.exec_module(yasa_hypno_module)
generate_visbrain_hypnogram = yasa_hypno_module.generate_visbrain_hypnogram

def main():
    """
    Command-line interface for sleep EEG analysis.
    Offers options to generate hypnograms and visualize EEG data.
    """
    # Default values
    default_dir_path = "D:/data/my_trails/"
    default_filename = "TGAM_sleepdata_sample.edf"
    default_output_dir = "D:/data/my_trails/tmp1/"
    
    # Ask user for directory path
    print(f"Enter directory path [default: {default_dir_path}]: ", end="")
    dir_path = input().strip()
    if not dir_path:
        dir_path = default_dir_path
        print(f"Using default directory path: {default_dir_path}")
    
    # Ensure directory path ends with a slash
    if not dir_path.endswith('/'):
        dir_path += '/'
    
    # Ask user for filename
    print(f"Enter EDF filename [default: {default_filename}]: ", end="")
    filename = input().strip()
    if not filename:
        filename = default_filename
        print(f"Using default filename: {default_filename}")
    
    # Combine path and filename
    edf_file = os.path.join(dir_path, filename)
    print(f"Using EDF file: {edf_file}")
    
    # Validate EDF file exists
    if not os.path.isfile(edf_file):
        print(f"Error: EDF file not found at {edf_file}")
        return
    
    # Ask user for output directory
    print(f"Enter output directory [default: {default_output_dir}]: ", end="")
    output_dir = input().strip()
    if not output_dir:
        output_dir = default_output_dir
        print(f"Using default output directory: {default_output_dir}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Ask user for processing option
    print("\nSelect an option:")
    print("1. Generate hypnogram only (using YASA) [default]")
    print("2. Generate hypnogram and display in Visbrain")
    print("Enter your choice (default is 2): ", end="")
    
    choice = input().strip()
    if not choice:
        choice = "2"
        print("Using default option: 2. Generate hypnogram and display in Visbrain")
    
    try:
        # Generate hypnogram files
        hypno_file, desc_file = generate_visbrain_hypnogram(edf_file, output_dir)
        
        # Print output information
        print(f"\nFiles generated successfully:")
        print(f"1. {hypno_file}")
        print(f"2. {desc_file}")
        
        # Display in Visbrain if option 2 was selected
        if choice == "2":
            print("\nLaunching Visbrain Sleep GUI...")
            Sleep(data=edf_file, hypno=hypno_file).show()
        
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
