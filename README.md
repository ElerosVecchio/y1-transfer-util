# Y1 Transfer Utility

[![Version](https://img.shields.io/badge/version-v1.1.0-blue)](https://github.com/ElerosVecchio/y1-transfer-util/releases/tag/v1.1.0)
[![License](https://img.shields.io/badge/license-MIT%20License-lightgrey)](https://github.com/ElerosVecchio/y1-transfer-util/blob/main/LICENSE)
[![Support](https://img.shields.io/badge/support-Kofi-orange?logo=kofi)](https://ko-fi.com/roguespassage)

A simple utility to convert and/or transfer music files and album art.

---

### Installation

1. ***REQUIRED!*** Download and install [ffmpeg](https://ffmpeg.org/download.html)
2. Either:
	- **Windows Only**: download the [latest release](https://github.com/ElerosVecchio/y1-transfer-util/releases/latest) and run the executable
 	- Any platform:
		1. Install the [latest Python version](https://www.python.org/downloads/)
		2. Install [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
		3. Download this repository and run `main.py`

> Note: This project relies on Tkinter. This is usually installed alongside Python, but if not you may need to install it separately.

---

### How To Use

1. Enter or Browse for your existing music library (Input Folder)
2. Enter or Browse for the destination (Output Folder)
3. Check the checkbox to export music files as 320kbps MP3
> Leaving this unchecked will directly copy the source music files. Conversion to MP3 keeps metadata intact.
>
> Note: Non-embedded album artwork will ***always*** be converted to 500x500px BMP for compatibility with Rockbox
4. Click Start!

---

### Supported Formats

**Images (Album Art)**
- JPEG
- PNG
- WEBP
- GIF
- TIFF
- BMP

**Audio**
- AAC
- ALAC
- AIFF
- DSD
- FLAC
- MP3
- OGG
- WAV

> My library is almost entirely FLAC files so that is what I'm easily able to test.
> If the program crashes or skips your files, open a new [issue](https://github.com/ElerosVecchio/y1-transfer-util/issues)

---

### Roadmap

- Smart bitrate conversion
- Exclude list
- More conversion settings

---

##### This project uses [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) which is licensed under the Apache 2.0 Software License
