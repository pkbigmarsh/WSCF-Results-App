import os
from PDFGen import *

# font_varients = ("'Calibri Regular.ttf'", "'Calibri Bold.ttf'")
# folder = 'C:/Windows/Fonts/Calibri/'
# for varient in font_varients:
#     pdfmetrics.registerFont(TTFont(varient, os.path.join(folder, varient)))

individualFilePath = '../Info/tournamentresultsposting/individual_k12.TXT'
teamFilePath = '../Info/tournamentresultsposting/team_k5.TXT'
outputFileName = "test.pdf"

tournamentName = "Fond Du Lac Stem Academy"
tournamentDate = "1-Mar-14"
division = "K3"
headTournamentDirector = "Charles Windsor"
headTournamentHeader = "TD: "

numberOfParticipants = "77"
numOfParticipantsToDate = "2,535"

myCanvas = canvas.Canvas(outputFileName, pagesize=(WIDTH, HEIGHT))

printResultHeader(myCanvas, tournamentName, tournamentDate, numberOfParticipants,
    division, headTournamentDirector, numOfParticipantsToDate)

printIndividual(myCanvas, INCH, 6.5 * INCH, individualFilePath)

myCanvas.showPage()

printTeamHeader(myCanvas, "K5")
printTeamStandings(myCanvas, MARGIN_TOP - 32, teamFilePath)

myCanvas.save()
