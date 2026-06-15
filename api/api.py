import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
while script_dir in sys.path:
    sys.path.remove(script_dir)

project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Self-Learning AI Ecosystem"
)

app.include_router(router)
