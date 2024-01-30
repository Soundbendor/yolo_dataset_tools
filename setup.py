
from setuptools import setup 

setup(
  name="yolo_dataset_tools",
  version="0.1",
  author="Joey Stenbeck",
  py_modules=["yolo_dataset_tools"],
  install_requires=["bidict", "tqdm", "numpy", "Pillow", "scikit-image", "Shapely"],
)
