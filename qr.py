from sys import argv
import zbar
import Image

#Scan for qr codes in image, return first
def scan(image):
    #zbar results
    symbol = None
    return symbol

#Scan for all qr codes in image
def scanAll(image):
    symbol = None
    return symbol



def main():
    if len(argv) < 2: exit(1)

    # create a reader
    scanner = zbar.ImageScanner()

    # configure the reader
    scanner.parse_config('enable')

    # obtain image data
    pil = Image.open(argv[1]).convert('L')
    width, height = pil.size
    raw = pil.tostring()

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
