import logging 
import sys

logger = logging.getLogger("student_api")
logger.setLevel(logging.INFO)

if not logger.handlers:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)


format_template = logging.Formatter(fmt="%(asctime)s | %(name)s | [%(levelname)s] | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

stream_handler.setFormatter(format_template)

logger.addHandler(stream_handler)


    







