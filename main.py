from fastapi import FastAPI,Request
from PIL import Image
from escpos.printer import File 
import multiprocessing
import uvicorn
import requests
from fastapi.middleware.cors import CORSMiddleware

#++++ discomment this code if you have the next error with pyinstaller (fixed issaty error pyinstaller) ++++#

#import sys
#if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
#    class NullOutput(object):
#        def write(self, string):
#            pass

#        def isatty(self):
#            return False
#    sys.stdout = NullOutput()
#    sys.stderr = NullOutput()

app = FastAPI()
portPath = "/dev/usb/"

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origin,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/printers")
def getPrinters():
    '''return all printer lp'''
    listPrinters = []
    for indexPort in range(0,40):
        try:
            printer = File(f"{portPath}lp{indexPort}")
            printer.close()
            port = "lp"+indexPort.__str__()
            listPrinters.append(port)
        except:
            continue
    return {
        "status":"OK",
        "listPrinter":listPrinters
    }
@app.post("/command/{printerName}")
async def printTicket(request:Request,printerName:str):
    response = {
        "status":"ERROR",
        "error":"se produjo un error "
    }

    try:
        printer = File(portPath+printerName)        
        response["status"] = "OK"
        response["error"] = ""
        listData = await request.json()
        for data in listData:
            if data["type"] == "text":
                printer.text(data["data"])
            elif data["type"] == "qr":
                printer.qr(data["data"],size=9)
            elif data["type"] == "img":
                image = requests.get(data["data"])
                if image.status_code == 200:
                    with open("image.png","wb") as img:
                        img.write(image.content)
                        imageTemplate = Image.open("image.png")
                        imageResize = imageTemplate.resize((data["width"],data["height"]))
                        printer.image(imageResize)
                else:
                    imageTemplate = Image.open(data["data"])
                    imageResize = imageTemplate.resize((data["width"],data["height"]))
                    printer.image(imageResize)   
            elif data["type"] == "configure":
                printer.set(
                    align = data["align"],
                    font = data["typeFont"],
                    bold = data["bold"]
                )
            elif data["type"] == "barcode":
                printer.barcode(data["data"],data["typeCode"],64,3,'','A')
            elif data["type"] == "open":
                pins = [27,112,48,0,6]
                for pin in pins:
                    try:
                        printer.cashdraw(pins)
                        break
                    except:
                        continue
            elif data["type"] == "openpartial":
                pins = [27,112,0,25,255]
                for pin in pins:
                    try:
                        printer.cashdraw(pin)
                        break
                    except:
                        continue
        printer.set(align="center",bold=True)
        printer.text("---------------------\n")
        printer.text("SAUL BURCIAGA HERNANDEZ\n")
        printer.text("www.saultech.herokuapp.com\n")
        printer.text("---------------------\n")
        printer.cut()
        printer.close()
    except Exception as e:
        response["status"] = "ERROR"
        response["error"] = e.__str__()

    return response


def main(host="127.0.0.1",port = 5656):
    uvicorn.run(app,host = host, port = port,log_level='critical')


if __name__ == '__main__':
    multiprocessing.freeze_support()
    print("running printering :)")
    main()
