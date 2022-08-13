from urllib import request
from fastapi import FastAPI,Request
from escpos.printer import File 
import multiprocessing
import uvicorn
app = FastAPI()
portPath = "/dev/usb/"

@app.get("/printers")
def getPrinters():
    '''return all printer lp'''
    listPrinters = []
    for indexPort in range(0,40):
        try:
            printer = File(f"{portPath}lp{indexPort}")
            port = portPath+"lp"+indexPort.__str__()
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
        data = await request.json()

        for item in data["listData"]:
            if(item["type"] == "text"):
                print(item["data"])
            elif(item["type"] == "qr"):
                print(item["data"])
    except:
        response["status"] = "ERROR"
        response["error"] = "Impresora no encontrada"

    return response


def main(host="127.0.0.1",port = 5656):
    uvicorn.run("main:app",host = host, port = port,reload=True)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    print("running instance uvicorn")
    main()