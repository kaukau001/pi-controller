import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CURRENT_DIR, '..', 'data')

XLSX_PATH = os.path.join(DATA_DIR, 'experiment_data.xlsx')
CSV_PATH = os.path.join(DATA_DIR, 'oscilloscope_data.csv')
ARMOR_VOLTAGE = 'Tensão'
TACOMETER_VOLTAGE = 'Tacômetro'
ENGINE_SPEED = 'Rotação'
POLY_DEGREE = 7
