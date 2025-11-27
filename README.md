# Linkomanija-Search

VERSION: 1.0  
AUTHORS: [rmux](https://github.com/rmuxv2)

---

## Overview

**Linkomanija-Search** is an **unofficial search plugin for [qBittorrent](https://www.qbittorrent.org/)**.  
It enables torrent search and direct download from [linkomanija.net](https://www.linkomanija.net) via web scraping.  
*This is not an official Linkomanija or qBittorrent project.*

---

## Features

- Works as a search engine plugin for qBittorrent.
- Search for torrents by keyword and category.
- Download `.torrent` files instantly from results.
- Parses and prints torrent metadata (name, size, seeds, leeches, etc).
- Supports categories: Movies, TV, Music, Games, Anime, Software.

---

## Configuration

To use this tool, you must provide your Linkomanija credentials in a configuration file:

1. Create a file named `linkomanija_config.json` in **one** of the following locations:
    - The same directory as the plugin script
    - `~/linkomanija_config.json`
    - `~/Documents/linkomanija_config.json`

2. The file must contain the following JSON structure:

    ```json
    {
        "login": "your_username",
        "phpsessid": "your_session_id",
        "track_key": "meowmeow"
    }
    ```

- `login`: Your username (browser cookies)
- `phpsessid`: Your PHPSESSID value (browser cookies)
- `track_key`: Extracted from your tracker announce URL:
  If your announce URL is `http://tracker.linkomanija.net:PORT/meowmeow/announce`, then your `track_key` is `meowmeow`.

### How to Find Credentials

- Use a browser cookie editor extension to extract `login` and `phpsessid` from your cookies.
- Get `track_key` from your announce URL (the segment between port and `/announce`).

---

## Usage

Copy the plugin file (`linkomanija.py`) to qBittorrent's search engine directories.
Activate it in qBittorrent's **Search** tab.

You can use the search interface in qBittorrent to query for torrents.  
Supported categories:  
- all
- movies
- tv
- music
- games
- anime
- software

Results can be filtered and torrents downloaded directly from qBittorrent.

---

## Supported Categories

| Category | Code  |
|----------|-------|
| All      | all   |
| Movies   | 29    |
| TV       | 30    |
| Music    | 37    |
| Games    | 45    |
| Anime    | 38    |
| Software | 32    |

---

## Requirements

- Python 3.x
- Internet access
- User credentials for linkomanija.net (**membership required**)
- qBittorrent (with Python search plugin system enabled)

---

## Security Warning

Your credentials (login, PHPSESSID, track_key) **must be kept secure**.  
Do not share them publicly.  
Set file permissions to prevent unwanted access.

---

## Disclaimer

This is an **unofficial** plugin for qBittorrent and Linkomanija.net.  
The script is provided for **educational purposes only**.  
Use it responsibly and in accordance with all applicable laws and tracker rules.

---

## License

MIT License
