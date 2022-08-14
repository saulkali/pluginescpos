from escpos.printer import File
port = "/dev/usb/lp0"
printer = File(port)

printer.block_text("texto",font="a",columns=1)

printer.block_text("texto",font="a",columns=5)
printer.line_spacing(spacing=None,divisor= 180)
