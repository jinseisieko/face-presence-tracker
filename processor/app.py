import cv2
import time
import json
import requests
import base64
import numpy as np
import logging
import argparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | processor | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("processor")

def main(url="http://analyzer:5000/frame"):
    ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processor") # imagine normal description to this
    parser.add_argument("serverurl", type=str, help='server URL to post status of face presence')
    args = parser.parse_args()
    main(args.serverurl)