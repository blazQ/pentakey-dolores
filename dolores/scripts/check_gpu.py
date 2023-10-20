import subprocess
risultato = subprocess.run("nvidia-smi", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check GPU Availability
gpu_info = risultato.stdout  # Execute the nvidia-smi command to get GPU information
gpu_info = '\n'.join(gpu_info)  # Convert the GPU information into a string

# Check if GPU is available
if gpu_info.find('failed') >= 0:
    print('Select the Runtime → "Change runtime type" menu to enable a GPU accelerator, ')
    print('and then re-execute this cell.')
else:
    print("Success!")