from PiPongBasis import ZeichenKarte, PixelKarte, SpielBasis, Spieler

class Geist(Spieler):

    def Start(self):
        self.SetzeGroesse(5,5)
        self.SetzePosition(32,32)
        self.SetzeGeschwidigkeit(0.09,0.11)
        self.SetzeLeitplanken(0, 63, 0, 63)
        self.ModusFrei()
        self.kachel = None

    def Male(self,x,y):
        print(x,y)
        # self.basis.MaleBlock(x,y,x+4,y+4, self.basis.FarbeBlauIntensiv)
        self.basis.MaleSprite(x,y,self.kachel)

class Pacman(SpielBasis):

    def SpielStart(self):
        pmk = PixelKarte("pacman-kacheln5x5v2.bmp")
        pmkInit = "QWERTZUJabcd.* -|OLKIYXCV+~"
        pacmanKacheln = {}
        for i in range(len(pmkInit)):
            pacmanKacheln[pmkInit[i]] = pmk.TeilBild(6*i,0, 5,5)
        welt = ZeichenKarte(11,13, [ 
            "I-----------O", 
            "|...........|", 
            "|.I-O.-----.|", 
            "|.K-L.......|", 
            "|.....I---O.|", 
            "|.I---X---L.|", 
            "|.|.........|", 
            "|.|.I--O...-Y", 
            "|.|.K--L.|ab|", 
            "|........|cd|", 
            "K--------X--L"
            ])
        self.WeltKarte = PixelKarte(64,64)
        self.WeltKarte.BaueVonZeichenKarte(pacmanKacheln, welt, 5,5)
        self.WeltKarte.SchreibeBild("e.bmp")

        self.x = 0

        blinky = Geist()
        blinky.kachel = pacmanKacheln['a']
        self.AddiereSpieler(blinky)

    def SpielBerechneEinBild(self):

        if False:
            self.MaleBlock(self.x,0,self.x+5,63, self.FarbeBlauIntensiv)
            self.x = self.x + 1
            if self.x > 58:
                self.x = 0

        if False:
            self.MaleSprite(0,0,self.WeltKarte)

# Haupt-Funktion
if __name__ == "__main__":
    spiel = Pacman()
    if (not spiel.process()):
        pass
