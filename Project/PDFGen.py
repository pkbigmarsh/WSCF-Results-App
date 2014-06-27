from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont  
from Constants import *
from CSVReader import *

def printIndividual(myCanvas, left, top, filepath):
    columns = [
    .20 * INCH,
    .5 * INCH,
    2.5 * INCH,
    30.0 * INCH,
    3.00 * INCH,
    3.5 * INCH,
    4.0 * INCH,
    5.00 * INCH,
    5.75 * INCH,
    6.50 * INCH,
    7.25 * INCH,
    8.00 * INCH,
    8.75 * INCH,
    9.50 * INCH,
    10.25 * INCH]
    myCanvas.setFont("Helvetica", 12 * POINT)

    y = top

    result = CSVReader(filepath)
    for i in range(0, len(result.headers)):
        myCanvas.drawString(columns[i], y, result.headers[i])

    y -= 12 * POINT

    next = result.getNext()
    while(next != None):
        if (y < (.5 * INCH)):
            y = top
            myCanvas.showPage()

        status = result.getItem("St", next)
        if(status != None and status != "Out"):
            for i in range(0, len(next)):
                myCanvas.drawString(columns[i], y, next[i])
            y -= 12 * POINT

        next = result.getNext()

def printResultHeader(myCanvas, tournyName, tournyDate, numParticipants, division, tournyDirector, numParticipantsToDate):
    myCanvas.setFillColorRGB(0,0,0)

    header = [.5 * INCH, HEIGHT - (1 * INCH)]

    # Header information
    myCanvas.setFont("Helvetica", 24 * POINT)
    myCanvas.drawString(header[0], header[1], tournyName)

    myCanvas.setFont("Helvetica", 16 * POINT)
    header[0] += .5 * INCH
    header[1] -= 24 * POINT

    myCanvas.drawString(header[0], header[1], tournyDate)

    header[0] = WIDTH - INCH * 2

    myCanvas.drawRightString(header[0], header[1], PARTICIPANTS_STR)

    header[0] += INCH

    myCanvas.drawRightString(header[0], header[1], numParticipants)

    header[0] = INCH
    header[1] -= 24 * POINT

    myCanvas.drawString(header[0], header[1], division)

    header[0] += INCH

    myCanvas.drawString(header[0], header[1], "TD: " + tournyDirector)

    header[0] = WIDTH - INCH * 2

    myCanvas.drawRightString(header[0], header[1], PARTICIPANTS_TO_DATE_STR)

    header[0] += INCH

    myCanvas.drawRightString(header[0], header[1], numParticipantsToDate)

