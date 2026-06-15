import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from train import train_all_models
from predict import run_predictions

if __name__ == "__main__":
    print("Starting Self-Learning AI Decision Support Ecosystem")
    train_all_models()
    run_predictions()
