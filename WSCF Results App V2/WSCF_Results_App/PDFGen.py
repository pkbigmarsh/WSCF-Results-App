from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont  
from kivy.logger import Logger
from Constants import *
from CSVReader import *
from PlayerIdenfication import *
import copy
import math

def printIndividual(myCanvas, left, top, filepath, num_trophy_winners, trophy_highlight, player_identification):
    player_ident = copy.copy(player_identification)
    base_left = .20 * INCH
    base_right = 10.30 * INCH
    space = base_right - base_left
    lengths = []
    total_characters = 0

    result = CSVReader(filepath)

    buff = 3

    for head in result.headers:
        if head.lower() == "name".lower():
            buff = 8
        else:
            buff = 3

        length = result.getLongest(head) + buff
        lengths.append(length)
        total_characters += length

    increment = math.floor(space / total_characters)

    columns = [base_left]

    for i in range(0, len(lengths) - 1):
        columns.append(
            columns[i] + increment * lengths[i])

    myCanvas.setFont("Helvetica", 12 * POINT)

    y = top
    
    for i in range(0, len(result.headers)):
        myCanvas.drawString(columns[i], y, result.headers[i])

    y -= LINE

    highlights = []
    descriptions = []

    if int(num_trophy_winners) > 0:
        highlights.append(trophy_highlight)
        descriptions.append("Trophy Winners")

    num_trophies = 0
    next = result.getNext()
    new_page = False
    highlight_width = columns[6] - columns[0]

    while(next != None):
        if (y < (.5 * INCH)):
            new_page = True

        if (num_trophies < int(num_trophy_winners)) == True:
            num_trophies += 1

            highlight(myCanvas, columns[0], y, highlight_width, trophy_highlight)

        status = result.getItem("St", next)
        name = result.getItem("Name", next)
        if(status != "Out"):
            if new_page == True:
                draw_highlight_key(myCanvas, highlights, descriptions)

                highlights = []
                descriptions = []
                y = top
                myCanvas.showPage()
                new_page = False

            for player in player_ident:
                if player.name == name:

                    if player.description in descriptions:
                        player.col = highlights[descriptions.index(player.description)]
                    else:
                        highlights.append(player.col)
                        descriptions.append(player.description)

                    highlight(myCanvas, columns[0], y, highlight_width, player.col)

                    player_ident.remove(player)

            for i in range(0, len(next)):
                myCanvas.drawString(columns[i], y, next[i])
            y -= LINE

        next = result.getNext()

    if len(highlights) > 0:
        draw_highlight_key(myCanvas, highlights, descriptions)

def highlight(canvas, x, y, width, color):
    canvas.setStrokeColorRGB(color[0], color[1], color[2])
    canvas.setFillColorRGB(color[0], color[1], color[2])

    canvas.rect(x - 3, y - 3, width - 2, LINE + 1, 1, 1)

    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setFillColorRGB(0, 0, 0)

def draw_highlight_key(myCanvas, colors, descriptions):
    if len(colors) == 0 or len(descriptions) == 0:
        return
        
    y = .5 * INCH - LINE
    x = .3 * INCH
    next = (WIDTH - INCH) / len(descriptions)
    for i in range(0, len(descriptions)):
        highlight(myCanvas, x, y, LINE, colors[i])
        myCanvas.drawString(x + LINE + 2, y, descriptions[i])
        x += next

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

    y -= LINE

    ignore = 0
    num_trophies = 0
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

        if (num_trophies < int(num_trophy_winners)) and (playerCount == 0):
            num_trophies += 1

            myCanvas.setStrokeColorRGB(trophy_highlight[0], trophy_highlight[1], trophy_highlight[2])
            myCanvas.setFillColorRGB(trophy_highlight[0], trophy_highlight[1], trophy_highlight[2])


            myCanvas.rect(columns[0] - 3, y - 3, columns[3] - columns[0] - 2, LINE + 1, 1, 1)

            myCanvas.setStrokeColorRGB(0, 0, 0)
            myCanvas.setFillColorRGB(0, 0, 0)

        ignore = 0
        for i in range(0, len(line)):
            if(teamResult.headers[i] in IGNORE_TEAM):
                ignore += 1
            else:
                myCanvas.drawString(columns[i - ignore], y, line[i])

        y -= LINE

        line = teamResult.getNext()

    highlights = [trophy_highlight]
    descriptions = ["Trophy Winners"]

    if len(highlights) > 0:
        draw_highlight_key(myCanvas, highlights, descriptions)


def printResultHeader(myCanvas, tournyName, tournyDate, numParticipants, division, tournyDirector, numParticipantsToDate):
    myCanvas.setFillColorRGB(0,0,0)

    header = [.5 * INCH, HEIGHT - (.5 * INCH)]

    # Header information
    myCanvas.setFont("Helvetica", 24 * POINT)
    myCanvas.drawString(header[0], header[1], tournyName)

    myCanvas.setFont("Helvetica", 16 * POINT)
    header[0] += .5 * INCH
    header[1] -= 24 * POINT

    myCanvas.drawString(header[0], header[1], tournyDate)

    header[1] -= 20 * POINT

    myCanvas.drawString(header[0], header[1], "TD: " + tournyDirector)

    header[0] = WIDTH - INCH * 2

    myCanvas.drawRightString(header[0], header[1], PARTICIPANTS_STR)

    header[0] += INCH
    myCanvas.drawRightString(header[0], header[1], numParticipants)

    header[0] = INCH
    header[1] -= 24 * POINT

    myCanvas.drawString(header[0], header[1], division)

    header[0] += INCH

    header[0] = WIDTH - INCH * 2

    myCanvas.drawRightString(header[0], header[1], PARTICIPANTS_TO_DATE_STR)

    header[0] += INCH

    myCanvas.drawRightString(header[0], header[1], numParticipantsToDate)

