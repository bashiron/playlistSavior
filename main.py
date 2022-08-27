from playlist_savior import SMASH, MUSIC, FAVS, Savior

def diarias():
    savior = Savior()
    savior.save_playlist(SMASH)
    savior.save_playlist(MUSIC)

def semanales():
    savior = Savior()
    savior.save_playlist(FAVS)


if __name__ == "__main__":
    diarias()
