from PiPongBasis import ZeichenKarte, PixelKarte, SpielBasis

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

    def SpielBerechneEinBild(self):

        if False:
            self.MaleBlock(self.x,0,self.x+5,63, self.FarbeBlauIntensiv)
            self.x = self.x + 1
            if self.x > 58:
                self.x = 0

        if True:
            self.MaleSprite(0,0,self.WeltKarte)

# Haupt-Funktion
if __name__ == "__main__":
    spiel = Pacman()
    if (not spiel.process()):
        pass
