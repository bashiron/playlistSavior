# playlistSavior: Playlist Preservation Program
Ever clicked into your Youtube playlist to find out (or worse, not find out) some videos were randomly removed with no heads up whatsoever? Or maybe your favorites list had an obscure, hard to track down video that you loved?

playlistSavior provides a way to schedule a backup of your personal playlists so if/when they are tampered with you can ask it to remind you of the most relevant and unique data about it so you can then go look for a copy.

**[Features](#features) | [Quickstart](#quickstart) | [Commands](#available-commands)**

## features
- Backup current state of playlists by fetching [relevant fields](#stored properties) and storing them locally
- Scan for dead videos and retrieve their stored data
- (WIP) Categorize music videos by artist, vibe, genre, etc; so you can later get the urls of a specific category
- Soundtrack enthusiasts can also define OST-specific fields to better organize the playlist

## quickstart
...

## available commands
- `setup` - perform initial setup, you will be asked to provide a Youtube API's dev key and then you can choose to immediately start adding playlists to the list of "to-be-saved"
- `add-playlist` - add a singular playlist to the list
- `multi-add-playlist` - add multiple playlists to the list
- `save` - fetch data on videos from every stored playlist, recommended to schedule this command using tools like [cron](https://man7.org/linux/man-pages/man5/crontab.5.html) in Linux or the [task scheduler](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10) in Windows

## stored properties
- video title
- video description (crucial for later recovery)
- (WIP) video thumbnail
- channel name
- and more
