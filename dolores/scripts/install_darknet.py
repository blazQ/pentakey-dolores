import subprocess

# Cambia la directory di lavoro in /content
subprocess.run("cd /content", shell=True)

# Rimuovi la directory darknet se esiste
subprocess.run("rm -r darknet", shell=True)

# Clona il repository Darknet
subprocess.run("git clone https://github.com/AlexeyAB/darknet", shell=True)

# Aggiorna il sistema
subprocess.run("apt-get update", shell=True)

# Esegui l'aggiornamento del sistema
subprocess.run("apt-get upgrade", shell=True)

# Installa build-essential
subprocess.run("apt-get install build-essential", shell=True)

# Installa altre dipendenze
subprocess.run("apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev", shell=True)
subprocess.run("apt-get install libavcodec-dev libavformat-dev libswscale-dev", shell=True)
subprocess.run("apt-get install libopencv-dev", shell=True)

# Cambia la directory in darknet
subprocess.run("cd darknet", shell=True)

# Modifica il Makefile per abilitare le configurazioni desiderate
subprocess.run("sed -i 's/OPENCV=0/OPENCV=1/' Makefile", shell=True)
subprocess.run("sed -i 's/GPU=0/GPU=1/' Makefile", shell=True)
subprocess.run("sed -i 's/CUDNN=0/CUDNN=1/' Makefile", shell=True)
subprocess.run("sed -i 's/CUDNN_HALF=0/CUDNN_HALF=1/' Makefile", shell=True)

# Compila Darknet
subprocess.run("make", shell=True)

# Esegui Darknet
subprocess.run("./darknet", shell=True)
