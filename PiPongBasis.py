import array
import time
from PIL import Image
from samplebase import SampleBase
from rgbmatrix import graphics
import pigpio
import pigpio_encoder

""" Diese Klasse haelt alle Werkzeuge zur Entwicklung von PiPong-Spielen bereit. """

class ZeichenKarte:
    """ Diese Karte haelt Zeichen in Zeilen und Spalten. Sie ist dafuer geeignet,
    Spielwelten die aus regelmaessigen Kacheln bestehen, zu verwalten. """

    def __init__(self, hoehe=None, breite=None, zeilen=None):
        """ Erzeugt eine neue Zeichenkarte mit "hoehe" Zeilen und jeweils "breite" Spalten. 
        "zeilen" gibt ein Feld von Zeichketten an, die bei Bedarf gleich gelesen werden.
        Reihenfolge hohe, breite beachten! """
        self.rows = 0
        self.cols = 0
        self.lines = []
        if hoehe is not None and breite is not None:
            self.rows = hoehe
            self.cols = breite
            for _ in range(0, self.rows):
                self.lines.append(" " * self.cols)
            if zeilen is not None:
                self.Lade(zeilen)

    def Breite(self):
        return self.cols

    def Hoehe(self):
        return self.rows    

    def Lade(self, zeilen):
        for r in range(0,len(zeilen)):
            l = zeilen[r]
            if len(l) > self.cols:
                l = l[:self.cols]
            if len(l) < self.cols:
                l = l + " " * (self.cols - len(l))
            if r < self.rows:
                self.lines[r] = l

    def SetzeZeichen(self, zeile, spalte, zeichen):
        """ Setzt genau ein Zeichen in "zeile"/ "spalte". Die Koordinaten sind 0-basiert! 
        Reihefolge zeile, spalte beachten! """
        if zeile<self.rows and spalte<self.cols:
            l = self.lines[zeile]
            self.lines[zeile] = l[:spalte] + zeichen + l[spalte+1:] 

    def HoleZeichen(self, zeile, spalte):
        """ Gibt genau ein Zeichen in "zeile"/ "spalte" zurueck. Die Koordinaten sind 0-basiert! 
        Reihefolge zeile, spalte beachten! """
        if zeile<self.rows and spalte<self.cols:
            return self.lines[zeile][spalte] 

class PixelKarte:
    """ Diese Karte haelt Pixel-Daten, das heisst, Punkte mit RGB-Farbinformationen. 
    Die Karte kann Grafiken laden und speichern.
    Geladene Karten koennen als Sammlung von Kacheln betrachtet werden, um damit
    mit Hilfe von ZeichenKarte Spielwelten zu erzeugen. """

    def __init__(self, dateiBreite=None, hoehe=None):
        """ Erschafft eine neue PixelKarte. Entweder, dateiBreite enthaelt den Namen
        einer zu ladenen Datei. Oder, dateiBreite und hoehe sind Breite und Hoehe in 
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
        Der 2. Parameter enthaelt ein Feld von Zeichenkette, die die einzelnen Zeichen enthalten.
        kachelBreite und kachelHoehe sind die zu verwendenen Vorschuebe.
        """
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

    def BaueVonZeichenKarte(self, kachelVerzeichnis, zeichenKarte, kachelBreite, kachelHoehe, x0=0, y0=0):
        """ Baut eine grosse Karte aus kleinen Kacheln anf.
        Als Basis wird eine "zeichenKarte" genommen; von dieser wird auch die Breite/ Hoehe verwendet.
        kachelBreite und kachelHoehe sind die zu verwendenen Vorschuebe.
        "x0", "y0" geben eine Anfangskoordinate (Verschiebung) vor.
        """
        for ri in range(0, zeichenKarte.Hoehe()):
            for ci in range(0, zeichenKarte.Breite()):
                zei = zeichenKarte.HoleZeichen(ri,ci)
                if not zei in kachelVerzeichnis:
                    continue
                x00 = x0 + ci*kachelBreite
                y00 = y0 + ri*kachelHoehe
                self.SetzeEin(x00, y00, kachelVerzeichnis[zei])

    def Breite(self):
        return self.width

    def Hoehe(self):
        return self.height    

class Spieler:
    """ Steht fuer ein unabhaenging bewegbares Objekt, welches auf der SpielBasis frei positioniert werden kann """
    def __init__(self):
        """ Erschafft einen neuen Spieler. Fuer diesen sollten mit `SetzeGroesse` eine Groesse vorgegeben werden und
        mit `SetzePosition` eine Ausgangsposition. """
        self.basis = None
        self.width = 1
        self.height = 1
        self.SetzeLeitplanken(-1,-1,-1,-1)
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.mode = 0  
        self.Start()

    def SetzeGroesse(self, spielerHoehe, spielerBreite):
        """ Bestimmt den Platz mit ``spielerHoehe`` x ``spielerBreite``, den der Spieler einnimmt. Diese
        Abmessung sind wichtig fuer die Kollisionserkennung. """ 
        self.width = spielerBreite
        self.height = spielerHoehe

    def SetzePosition(self, x, y):
        """ Setzt eine neue Position fuer den Spieler. """
        self.x = x
        self.y = y

    def SetzeGeschwidigkeit(self, vx, vy):
        """ Setzt eine neue Geschwindigkeit fuer den Spieler, jeweils ``vx`` fuer die horizontale, ``vy`` fuer die vertikale Komponente. 
        Geschwindigkeit 1 bedeutet 1 Pixel pro Bildzyklus. """
        self.vx = vx
        self.vy = vy

    def SetzeLeitplanken(self, oben, unten, links, rechts):
        """ Setzt oder loescht die Leitplanken, an denen der Spieler automatisch abprallt.
        Positive Angaben sind 0-basierte Pixel-Positionen.
        -1 schaltet die Funktion fuer die jeweilige Richtung ab. """
        self.railTop = oben
        self.railBottom = unten
        self.railLeft = links
        self.railRight = rechts

    def ModusStop(self):
        """ Spieler bewegt sich nicht automatisch. """
        self.mode = 0

    def ModusFrei(self):
        """ Spieler bewegt sich mit einer vorgebenen Geschwidigkeit und prallt evtl. an den Leitplanken ab. """
        self.mode = 1

    def Start(self):
        """ Diese Funktion wird einmal am Start des Spielers aufgerufen, um zum Beispiel Variablen richtig zu
        initialisieren. Du musst diese Funktion 'ueberladen'. """
        pass

    def Male(self, x, y):
        """ Diese Funktion wird einmal in jeder Spielrunde aufgerufen. Hier kannst Du den Spieler auf dem Spielfeld
        malen. ``x`` und ``y`` sind die 0-basierten Positionen fuer die linke/ obere Ecke des Spielers.
        Du musst diese Funktion 'ueberladen'. """
        pass

    def Cycle(self):
        """ Intern. Musst Du nicht aufrufen. """
        if self.basis is None:
            return

        if self.mode == 1:
            self.x += self.vx
            self.y += self.vy

            if self.railLeft >= 0 and self.x <= self.railLeft:
                self.x = self.railLeft
                self.vx = abs(self.vx)

            if self.railTop >= 0 and self.y <= self.railTop:
                self.y = self.railTop
                self.vy = abs(self.vy)

            if self.railRight >= 0 and self.x + self.width - 1 > self.railRight:
                self.x = self.railRight - self.width + 1
                self.vx = -abs(self.vx)

            if self.railBottom >= 0 and self.y + self.height - 1 > self.railBottom:
                self.y = self.railBottom - self.height + 1
                self.vy = -abs(self.vy)

        self.Male(int(self.x), int(self.y))

class SpielBasis(SampleBase):
    """ Hauptprogramm fuer das Spiel """
    def __init__(self, *args, **kwargs):
        super(SpielBasis, self).__init__(*args, **kwargs)
        self.FarbeSchwarz = graphics.Color(0, 64, 0)
        self.FarbeRotIntensiv = graphics.Color(255, 0, 0)
        self.FarbeGruenIntensiv = graphics.Color(0, 255, 0)
        self.FarbeBlauIntensiv = graphics.Color(0, 0, 255)
        self.players = [] 
        self.SpielStart()

    def SpielStart(self):
        pass

    def SpielBerechneEinBild(self):
        pass

    def AddiereSpieler(self, spieler):
        """ Beruecksichtigt einen neuen Spieler im Spiel. """
        if not isinstance(spieler, Spieler):
            return
        spieler.basis = self
        self.players.append(spieler)

    def LoescheSpieler(self, spieler):
        """ Loescht einen Spieler aus dem Spiel. """
        if not isinstance(spieler, Spieler):
            return
        if spieler in self.players:
            self.players.remove(spieler)

    def MaleBlock(self, x1, y1, x2, y2, farbe):
        """ Malt einen rechteckigen Block zwischen den Koordinaten (x1,y1) und (x2,y2).
        Die Koordinaten sind 0-basiert. """

        # for y in range(y1,y2+1):
        #     graphics.DrawLine(self.double_buffer, x1, y, x2, y, farbe)
        graphics.DrawBlock(self.double_buffer, x1, y1, x2, y2, farbe)

    def MaleSprite(self, x1, y1, sprite):
        graphics.DrawSprite(self.double_buffer, x1, y1, x1+sprite.width-1, y1+sprite.height-1, sprite.RgbDaten())
    
    def run(self):
        self.double_buffer = self.matrix.CreateFrameCanvas()
        while True:
            self.MaleBlock(0,0,63,63, self.FarbeSchwarz)

            self.SpielBerechneEinBild()

            for sp in self.players:
                sp.Cycle()

            self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
            time.sleep(0.01)
