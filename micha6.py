#!/usr/bin/env python
import array
import time
from PIL import Image

class PixelKarte:

    def __init__(self, dateiBreite=None, hoehe=None):
        """ Erschafft eine neue PixelKarte. Entweder, dateiBreite enthält den Namen
        einer zu ladenen Datei. Oder, dateiBreite und hoehe sind Breite und Höhe in 
        Pixel einer leer anzulegenden PixelKarte. Hintergrund ist Schwarz. """
        self.width = 0
        self.height = 0
        self.pixdata = []
        if dateiBreite is not None and isinstance(dateiBreite, str):
            self.LadeBild(dateiBreite)
        elif dateiBreite is not None and hoehe is not None:
            self.Leer(dateiBreite, hoehe)

    def Leer(self, breite, hoehe):
        self.width = breite
        self.height = hoehe
        self.pixdata = []
        for _ in range(0, self.width * self.height):
            self.pixdata.append((0,0,0))

    def LadeBild(self, fn):
        # laden
        im = Image.open(fn, 'r')
        # RGB erzwingen
        self.image = im.convert('RGB')
        # Pixel Daten
        self.pixdata = list(self.image.getdata())
        # stats
        self.width = self.image.width
        self.height = self.image.height

    def SchreibeBild(self, fn):
        # data = list(self.pixdata)
        # data2 = [atom for tup in data for atom in tup]
        # im = Image.frombytes('RGB', (self.width, self.height), data2)
        im = Image.new('RGB', (self.width, self.height))
        im.putdata(self.pixdata)
        im.save(fn)

    def RgbDaten(self):
        res = array.array('B')
        i = 0
        while i<len(self.pixdata):
            res.append(self.pixdata[i][0])
            res.append(self.pixdata[i][1])
            res.append(self.pixdata[i][2])
            i+=1
        return res.tostring()

    def TeilBild(self,x0,y0,breite,hoehe):
        """ Mache ein Teilbild. """
        res = PixelKarte()
        res.width = breite
        res.height = hoehe
        for y in range(hoehe):
            for x in range(breite):
                if x0+x>= self.width or y0+y>=self.height:
                    continue
                i = (y0+y)*self.width + (x0+x)
                res.pixdata.append(self.pixdata[i])
        return res

    def SetzeEin(self,x0,y0,karte):
        """ Diese Funktion setzt eine kleine PixelKarte in eine grosse PixelKarte ein.
        Die Koordinaten x0,y0 sind 0-basiert. """
        for y in range(0,karte.height):
            for x in range(0,karte.width):
                if x0+x < self.width and y0+y < self.height:
                    self.pixdata[ (y0+y) * self.width + x0+x ] = karte.pixdata[ y*karte.width + x]

    def BaueAusKachelnAuf(self, kachelVerzeichnis, kachelZeichen, kachelBreite, kachelHoehe, x0=0, y0=0):
        """ Baut eine grosse Karte aus kleinen Kacheln anf.
        Der 1. Parameter ist ein Verzeichnis von Zeichen und PixkelKarten.
        Der 2. Parameter enthält ein Feld von Zeichenkette, die die einzelnen Zeichen enthalten.
        kachelBreite und kachelHoehe sind die zu verwendenen Vorschübe.
        getrennt. """
        for ri in range(0, len(kachelZeichen)):
            row = kachelZeichen[ri]
            for ci in range(0, len(row)):
                zei = row[ci]
                if not zei in kachelVerzeichnis:
                    continue
                x00 = x0 + ci*kachelBreite
                y00 = y0 + ri*kachelHoehe
                self.SetzeEin(x00, y00, kachelVerzeichnis[zei])

                # for y in range(0,karte.height):
                #     for x in range(0,karte.width):
                #         if x00+x < self.width and y00+y < self.height:
                #             self.pixdata[ (y00+y) * self.width + x00+x ] = karte.pixdata[ y*karte.width + x]



    def Breite(self):
        return self.width

    def Hoehe(self):
        return self.height    

# x = PixelKarte("b.bmp")
# y = x.RgbDaten()
# z = x.TeilBild(0,0,2,2)
# z.SchreibeBild("c.bmp")
# g = PixelKarte(100,50)
# d = { '1' : z, '2' : z }
# g.BaueAusKachelnAuf(d, [ "1212", "2121" ], 8, 8)
# g.SchreibeBild("d.bmp")
# pass

# pmk = PixelKarte("pacman-kacheln.bmp")
# pacmanKacheln = {
#     'A' : pmk.TeilBild( 0, 0, 8, 8),
#     'B' : pmk.TeilBild( 8, 0, 8, 8),
#     'C' : pmk.TeilBild(16, 0, 8, 8),
#     'D' : pmk.TeilBild(24, 0, 8, 8),
#     '-' : pmk.TeilBild(32, 0, 8, 8),
#     '|' : pmk.TeilBild(40, 0, 8, 8),
#     '1' : pmk.TeilBild(48, 0, 8, 8)
# }
# g = PixelKarte(100,50)
# g.BaueAusKachelnAuf(pacmanKacheln, [ 
#     "|------1", 
#     "| ABCD |", 
#     "|------|" 
#     ], 8, 8)
# g.SchreibeBild("d.bmp")
# x = pacmanKacheln['A']
# x.pixdata[0] = (255,255,255)
# x.pixdata[1] = (255,255,255)
# x.pixdata[2] = (255,255,255)
# x.SchreibeBild("e.bmp")

pmk = PixelKarte("pacman-kacheln5x5v2.bmp")
pmkInit = "QWERTZUJabcd.* -|OLKIYXCV+~"
pacmanKacheln = {}
for i in range(len(pmkInit)):
    pacmanKacheln[pmkInit[i]] = pmk.TeilBild(6*i,0, 5,5)
g = PixelKarte(96,128)
g.BaueAusKachelnAuf(pacmanKacheln, [ 
    "I-----------------O", 
    "|.................|", 
    "|.IO.I-O.I------O.|", 
    "|.||.| |.|      |.|", 
    "|.KL.K-L.K------L.|", 
    "|.................|", 
    "|.IO.I-------O.IO.|", 
    "|.KL.K-------L.KL.|", 
    "|.................|", 
    "K--O.I--O.I--O.I--L", 
    "   |.| IL.KO |.|   ", 
    "---L.| |a.b| |.K---", 
    ".....| |...| |.....", 
    "---O.| |c.d| |.I---", 
    "   |.| KO.IL |.|   ", 
    "I--L.K--L.K--L.K--O", 
    "|.................|", 
    "|.IO.I--O.I--O.IO.|", 
    "|.||.C--L.C--L.||.|", 
    "|.KL.|....|....||.|", 
    "|....|.---L.I--L|.|", 
    "|.IO.|......|   |.|", 
    "|.KL.K-- ---X---L.|", 
    "|.................|", 
    "K-----------------L"
    ], 5,5)
g.SchreibeBild("d.bmp")
pass    

pmk = PixelKarte("pacman-kacheln5x5v2.bmp")
pmkInit = "QWERTZUJabcd.* -|OLKIYXCV+~"
pacmanKacheln = {}
for i in range(len(pmkInit)):
    pacmanKacheln[pmkInit[i]] = pmk.TeilBild(6*i,0, 5,5)
g = PixelKarte(64,64)
g.BaueAusKachelnAuf(pacmanKacheln, [ 
    "I-----------O", 
    "|...........|", 
    "|.I-O.-----.|", 
    "|.K-L.......|", 
    "|.....I---O.|", 
    "|.I---X---L.|", 
    "|.|.........|", 
    "|.|.I--O...-Y", 
    "|.|.K--L |ab|", 
    "|........|cd|", 
    "K--------X--L"
    ], 5,5)
g.SchreibeBild("e.bmp")
pass    

