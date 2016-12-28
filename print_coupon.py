#!/usr/bin/env python3

import argparse
import datetime

from escpos.printer import Usb
from WurstDB.wurstApiClient import DbClient

# argparse definitions
parser = argparse.ArgumentParser(description='Print Freiwurst coupons.')
parser.add_argument('-c', '--count', type=int, default=1,
                    help='number of coupons to print')
parser.add_argument('-v', '--volume', type=int, default=1,
                    help='number of wursts you get with the coupon')
parser.add_argument('-f', '--flavour', type=str, default='Get a Freiwurst at our assembly!\nTAKE THIS WITH YOU!',
                    help='flavour text to print below the QR code')
parser.add_argument('--method', type=str, default='coupon',
                    help='method of the wurst code, used inside the WurstDB')
parser.add_argument('--url', type=str, default='https://www.freiwurst.net/qr/',
                    help='string to prepend the QR code with -- can be an URL for example')
parser.add_argument('-s', '--server', type=str, default='http://localhost:5000',
                    help='address of the database REST API')
parser.add_argument('--usbvendor', type=int, default=0x04b8,
                    help='vendor ID of the used usb printer')
parser.add_argument('--usbproduct', type=int, default=0x0e02,
                    help='product ID of the used usb printer')


def print_coupon(printer, qr_string, text, volume):
    # set printing style to a defined state
    printer.set(align='center')

    # print image at the top
    printer.image('logo.png')

    # print a QR code natively on the printer, this looks better than software QR codes
    printer.qr(qr_string, size=3, native=True)

    # print the text
    printer.text(text + '\n\n')

    # print the date and the volume
    # maximum print width is 42 characters with default text size
    printer.text('{:<37s}{:>5s}'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M:%S'), str(args.volume)))

    # cut off the receipt
    printer.cut()

if __name__ == "__main__":
    args = parser.parse_args()

    # connect to the database
    db = DbClient(args.method, args.server)

    # add and enable method
    db.addPubMethod(args.method)
    db.enablePubMethod(args.method)

    # connect to EPSON TM-T88IV
    printer = Usb(args.usbvendor, args.usbproduct, 0)

    for i in range(args.count):
        # register a coupon code
        code = db.getCode(args.volume)

        # print the coupon
        print_coupon(printer, args.url + code, args.flavour, args.volume)
