#!/usr/local/bin/python3.4
 
import os, sys, logging, json, argparse, time, datetime, requests, uuid
from concurrent.futures import ThreadPoolExecutor

def init_logging():
    global logger
    global logger_kpi
    
    # Create a custom logger
    logger = logging.getLogger('SNS4SSLA')
    logger.setLevel(logging.DEBUG)
    logger_kpi = logging.getLogger('E2E_SLICER-KPI')
    logger_kpi.setLevel(logging.INFO)

    # Create handlers
    date = datetime.date.today()
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('log_SNS4SSLA'+str(date)+'.log')
    kpi_handler = logging.FileHandler('log_KPI_InitialTime'+str(date)+'.log')
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.INFO)
    kpi_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    kpi_format = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    kpi_handler.setFormatter(kpi_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    logger_kpi.addHandler(kpi_handler)

def init_environment():
    with open('config_files/config_settings.env') as f:
        for line in f:
            if 'export' not in line:
                continue
            if line.startswith('#'):
                continue
            # Remove leading `export `
            # then, split name / value pair
            key, value = line.replace('export ', '', 1).strip().split('=', 1)
            os.environ[key] = value

def init_thread_pool(workers):
    global executor
    executor = ThreadPoolExecutor(max_workers=workers)