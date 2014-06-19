import os
from CSVReader import *
from reportlab.pdfgen import canvas

TEXT = """%s    page %d of %d

a wonderful file
created with Sample_Code/makesimple.py"""

POINT = 1
INCH = 72
WIDTH = 11 * INCH
HEIGHT = 8.5 * INCH



individualFilePath = '../Info/tournamentresultsposting/individual_k12.TXT'
outputFileName = "test.pdf"

result = CSVReader(individualFilePath)

x = 1 * INCH
y = 8 * INCH

c = canvas.Canvas(outputFileName, pagesize=(WIDTH, HEIGHT))
c.setStrokeColorRGB(0,100,0)
c.setFillColorRGB(0,100,0)
c.rect(x,y,5 * INCH, 12 * POINT, fill=1)

c.setStrokeColorRGB(0,0,0)
c.setFillColorRGB(0,0,0)

c.setFont("Helvetica", 12 * POINT)

next = result.getNextAsString()
while(next != None):
    if (y < (.5 * INCH)):
        y = 8 * INCH
        c.showPage()

    c.drawString(x, y, next)
    y -= 12 * POINT

    next = result.getNextAsString()

c.save()

def make_pdf_file(output_filename, np):
    title = output_filename
    c = canvas.Canvas(output_filename, pagesize=(8.5 * inch, 11 * inch))
    c.setStrokeColorRGB(0,0,0)
    c.setFillColorRGB(0,0,0)
    c.setFont("Helvetica", 12 * point) 
    for pn in range(1, np + 1):
        v = 10 * inch
        for subtline in (TEXT % (output_filename, pn, np)).split( '\n' ):
            c.drawString( 1 * inch, v, subtline )
            v -= 12 * point
        c.showPage()
    c.save()

# make_pdf_file(outputFileName, 1)