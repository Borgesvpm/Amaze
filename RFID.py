# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:55:40 2020

@author: Administrator2
"""

import argparse
import serial
 
if __name__ == '__main__':
 
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', help='Serial port to read tags from', required=True)
    args = parser.parse_args()
 
    serial_port = args.port
    with serial.Serial(serial_port, 9600) as rfid_reader:
        while(True):
            tag = rfid_reader.readline().decode('UTF-8').strip()
            print(tag)