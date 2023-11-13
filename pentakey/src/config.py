import os

class DefaultConfig:
    INPUT_FOLDER = os.environ.get("INPUT_FOLDER", "/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/results")
    INPUT_FILE = os.environ.get("INPUT_FILE", "risultato.json")
    OUTPUT_FOLDER = os.environ.get("OUTPUT_FOLDER", "/home/musimathicslab/Scrivania/CacciaNegriRapa/pentakey/src/results")
    OUTPUT_NORMALIZED_FILE = os.environ.get("OUTPUT_NORMALIZED_FILE", "risultato_normalizzato.json")