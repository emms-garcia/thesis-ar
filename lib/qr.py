#!/usr/bin/python
# -*- coding: utf-8
import os

# Fix para windows
zbar_path = os.path.join(os.environ['ProgramFiles'], 'zbar', 'bin')
os.environ['PATH'] = "{0};{1}".format(os.environ['PATH'], zbar_path)

import zbar

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

#Scan for qr codes in image, return first
def scan(image):
  height, width = image.shape
  raw = image.tostring()
  image = zbar.Image(width, height, 'Y800', raw)
  scanner.scan(image)
  for symbol in image:
    return symbol
  return None

#Scan for all qr codes in image
def scanAll(image):
  height, width = image.shape
  raw = image.tostring()
  image = zbar.Image(width, height, 'Y800', raw)
  scanner.scan(image)
  symbols = []
  for symbol in image:
    symbols.append(symbol)
  if len(symbols) > 0:
    return symbols
  else:
    return None

def main():
  pass

if __name__ == "__main__":
  main()