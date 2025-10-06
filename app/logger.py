import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logger = logging.getLogger("cyberthreat")
logger.setLevel(logging.INFO)

fh = RotatingFileHandler(os.path.join(LOG_DIR, "app.log"), maxBytes=2_000_000, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
