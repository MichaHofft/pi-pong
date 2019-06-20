from PiPongBasis import ZeichenKarte, PixelKarte

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
    "|.|.K--L |ab|", 
    "|........|cd|", 
    "K--------X--L"
    ])
g = PixelKarte(64,64)
g.BaueVonZeichenKarte(pacmanKacheln, welt, 5,5)
g.SchreibeBild("e.bmp")
pass 