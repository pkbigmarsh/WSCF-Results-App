from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont  
from Constants import *
from CSVReader import *
from kivy.logger import Logger

def printIndividual(myCanvas, left, top, filepath, num_trophy_winners, trophy_highlight):
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

    num_trophies = 0
    next = result.getNext()
    while(next != None):
        if (y < (.5 * INCH)):
            y = top
            myCanvas.showPage()

        if num_trophies < num_trophy_winners:
            num_trophies += 1
            myCanvas.setStrokeColorRGB(trophy_highlight[0], trophy_highlight[1], trophy_highlight[2])
            myCanvas.setFillColorRGB(trophy_highlight[0], trophy_highlight[1], trophy_highlight[2])
            myCanvas.rect(columns[0], y - 12, columns[6] - columns[6], 12, 1, 1)


            myCanvas.setStrokeColorRGB(0, 0, 0)
            myCanvas.setFillColorRGB(0, 0, 0)



        status = result.getItem("St", next)
        if(status != None and status != "Out"):
            for i in range(0, len(next)):
                myCanvas.drawString(columns[i], y, next[i])
            y -= 12 * POINT

        next = result.getNext()

def printTeamHeader(myCanvas, division):
    left = MARGIN_LEFT + INCH * 2
    top = MARGIN_TOP

    myCanvas.setFillColorRGB(0,0,0)
    myCanvas.setFont("Helvetica", 16 * POINT)
    myCanvas.drawString(left, top, division)

    left -= .5 * INCH
    top -= 17 * POINT
    myCanvas.setFontSize(12 * POINT)
    myCanvas.drawString(left, top, "Team Standings")

def printIndividualHeader(myCanvas, division):
    left = MARGIN_LEFT + INCH * 2
    top = MARGIN_TOP

    myCanvas.setFillColorRGB(0,0,0)
    myCanvas.setFont("Helvetica", 16 * POINT)
    myCanvas.drawString(left, top, division)

    left -= .5 * INCH
    top -= 17 * POINT
    myCanvas.setFontSize(12 * POINT)
    myCanvas.drawString(left, top, "Individual Standings")

def printTeamStandings(myCanvas, startTop, filepath, num_trophy_winners, trophy_highlight):
    myCanvas.setFont("Helvetica", 11 * POINT)

    y = startTop
    x = MARGIN_LEFT

    teamResult = CSVReader(filepath)

    columns = [
        x,
        x + INCH * .5,
        x + INCH * 6.25,
        x + INCH * 7.00,
        x + INCH * 7.75,
        x + INCH * 8.50,
        x + INCH * 9.25
    ]
    
    ignore          = 0
    playerCount     = 0

    for i in range(0, len(teamResult.headers)):
        if(teamResult.headers[i] not in IGNORE_TEAM):
            myCanvas.drawString(columns[i - ignore], y, teamResult.headers[i])
        else:
            ignore += 1

    y -= 12 * POINT

    ignore = 0

    line = teamResult.getNext()
    while(line != None):
        if(y < MARGIN_BOTTOM):
            y = MARGIN_TOP
            myCanvas.showPage()

        
        if(line[0] == ""):
            playerCount += 1
        else:
            playerCount = 0

        if(playerCount > 4):
            line = teamResult.getNext()
            continue

        ignore = 0
        for i in range(0, len(line)):
            if(teamResult.headers[i] in IGNORE_TEAM):
                ignore += 1
            else:
                myCanvas.drawString(columns[i - ignore], y, line[i])

        y -= 12 * POINT

        line = teamResult.getNext()


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

