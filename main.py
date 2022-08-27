from datetime import date
from playlist_savior import Savior, SMASH, MUSIC, FAVS

def salvar():
    savior = Savior()
    pls = [SMASH, MUSIC]
    if date.today().weekday() == 6:
        pls.append(FAVS)
    for pl in pls:
        savior.save_playlist(pl)


if __name__ == "__main__":
    salvar()
