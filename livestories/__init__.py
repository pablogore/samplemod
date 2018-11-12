import os
from os.path import isfile
from pathlib import Path
from configparser import ConfigParser

from pyspark.sql import SparkSession

parser = ConfigParser()
parser.read("settings.ini")

BASE    = parser['url']['base_url']
YEARS   = parser['years']['process_years']


