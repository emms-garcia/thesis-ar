import zbar
import numpy

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

#Scan for qr codes in image, return first
def scan(image):
    if len(image.shape) is 3:
        height, width, _ = image.shape
    else:
        height, width = image.shape
    print width, height
    raw = image.tostring()
    image = zbar.Image(width, height, 'Y800', raw)
    # scan the image for barcodes
    scanner.scan(image)
    for symbol in image:
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        print symbol.location
    del image

#Scan for all qr codes in image
def scanAll(image):
    symbol = None
    return symbol

def main():
    if len(argv) < 2: exit(1)



    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image for barcodes
    scanner.scan(image)

    # extract results
    for symbol in image:
        # do something useful with results
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        print symbol.location

    # clean up
    del(image)


if __name__ == "__main__":
    main()
