from escpos.printer import Usb

""" Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
p = Usb(0x04b8, 0x0e02, 0)


def print_coupon(qr_string, text):
    p.set(align='center')
    p.image('logo.png')
    p.qr(qr_string, size=3, native=True)
    p.text(text)
    p.cut()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print "Printing demo coupon..."
        print_coupon('https://www.freiwurst.net/qr/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '#123')
    else:
        print_coupon(sys.argv[1], sys.argv[2])
