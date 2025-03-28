import mne
import yasa
import numpy as np
import os
import argparse

# Import visbrain's hypnogram data read/write module
from visbrain.io import write_hypno


def generate_visbrain_hypnogram(edf_file, output_dir):
    """Generate visbrain-compatible hypnogram files from an EDF file.
    
    Parameters
    ----------
    edf_file : str
        Path to the EDF file containing EEG data
    output_dir : str
        Directory where output files will be saved
    
    Returns
    -------
    tuple
        Paths to the generated hypnogram and description files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract EDF filename (without extension)
    edf_basename = os.path.basename(edf_file)
    edf_name = os.path.splitext(edf_basename)[0]
    
    # Set output file paths
    hypno_output_path = os.path.join(output_dir, f"{edf_name}_hypo.txt")
    hypno_desc_output_path = os.path.join(output_dir, f"{edf_name}_hypo_description.txt")
    
    # Read EDF file
    raw = mne.io.read_raw_edf(edf_file, preload=True)
    print(f"EDF file loaded successfully. Duration: {raw.times[-1]:.2f} seconds")
    print(f"Sampling frequency: {raw.info['sfreq']} Hz")
    print(f"Number of data points: {len(raw.times)}")
    
    # Perform sleep staging analysis
    sls = yasa.SleepStaging(
        raw,
        eeg_name=raw.ch_names[0],
        metadata=dict(age=41, male=True)
    )
    
    # Predict sleep stages
    y_pred = sls.predict()
    print(f"Sleep staging completed. Number of epochs: {len(y_pred)}")
    
    # Define vigilance state labels and values
    hstates = ['W', 'N1', 'N2', 'N3', 'N4', 'REM', 'Art']
    hvalues = [5, 3, 2, 1, 0, 4, -1]
    
    # YASA to visbrain stage name conversion
    yasa_to_visbrain = {
        'W': 'W',
        'N1': 'N1',
        'N2': 'N2',
        'N3': 'N3',
        'R': 'REM'
    }
    
    # Convert YASA predictions to visbrain numeric format
    y_pred_visbrain = []
    for stage in y_pred:
        visbrain_stage = yasa_to_visbrain.get(stage, 'Art')
        stage_index = hstates.index(visbrain_stage)
        y_pred_visbrain.append(hvalues[stage_index])
    
    # Convert to numpy array
    hypno_array = np.array(y_pred_visbrain)
    print(f"Converted to visbrain format. Hypnogram array shape: {hypno_array.shape}")
    
    # Calculate time vector, each point corresponds to a sleep stage
    epoch_duration = 30  # Duration of each sleep stage epoch (seconds)
    time_vector = np.arange(0, len(hypno_array) * epoch_duration, epoch_duration)
    print(f"Time vector created. Length: {len(time_vector)}")
    
    # Use version='time' mode to save sleep stage data
    print("Writing hypnogram using 'time' version...")
    write_hypno(hypno_output_path, hypno_array, version='time', 
                window=epoch_duration, time=time_vector, 
                hstates=hstates, hvalues=hvalues)
    
    # Write description file, including time information and sleep stage correspondence
    with open(hypno_desc_output_path, 'w') as f:
        f.write(f"time {epoch_duration}\n")
        for state, value in zip(hstates, hvalues):
            f.write(f"{state} {value}\n")
    
    print("Hypnogram files created successfully")
    return hypno_output_path, hypno_desc_output_path


def main():
    # Default values
    default_edf_file = "D:/data/my_trails/tmp1/TGAM_sleepdata_sample.edf"
    default_output_dir = "D:/data/my_trails/tmp1/"
    
    # Get EDF file path from user
    edf_file = input(f"Enter EDF file path [default: {default_edf_file}]: ").strip()
    if not edf_file:
        edf_file = default_edf_file
        print(f"Using default EDF file: {default_edf_file}")
    
    # Get output directory from user
    output_dir = input(f"Enter output directory [default: {default_output_dir}]: ").strip()
    if not output_dir:
        output_dir = default_output_dir
        print(f"Using default output directory: {default_output_dir}")
    
    # Validate EDF file exists
    if not os.path.isfile(edf_file):
        print(f"Error: EDF file not found at {edf_file}")
        return
    
    # Generate hypnogram files
    try:
        hypno_file, desc_file = generate_visbrain_hypnogram(edf_file, output_dir)
        
        # Print output information
        print(f"\nFiles generated successfully:")
        print(f"1. {hypno_file}")
        print(f"2. {desc_file}")
    except Exception as e:
        print(f"Error generating hypnogram files: {str(e)}")
        # Capture and print detailed exception information
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
