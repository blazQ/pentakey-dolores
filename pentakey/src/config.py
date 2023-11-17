import os

class DefaultConfig:
    RESULTS_PATH = os.path.abspath(os.path.join(os.path.join(os.getcwd(), "src"), "results"))
    INPUT_FOLDER = os.environ.get("INPUT_FOLDER", RESULTS_PATH)
    INPUT_FILE = os.environ.get("INPUT_FILE", "risultato.json")
    OUTPUT_FOLDER = os.environ.get("OUTPUT_FOLDER", RESULTS_PATH)
    OUTPUT_NORMALIZED_FILE = os.environ.get("OUTPUT_NORMALIZED_FILE", "risultato_normalizzato.json")


print(DefaultConfig.RESULTS_PATH)
print(DefaultConfig.OUTPUT_FOLDER)