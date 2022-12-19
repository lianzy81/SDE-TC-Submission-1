"""Configuration file for the data preprocessing module.
"""
import os

INPUT_DATA_DIR = os.path.join(".","data","raw")
SUCCESS_DATA_DIR = os.path.join(".","outputs","successful")
FAIL_DATA_DIR = os.path.join(".","outputs","failed")
REF_DATE = "20220101"