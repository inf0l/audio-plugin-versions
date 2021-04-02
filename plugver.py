#!/usr/bin/env python3
"""
Utility for checking audio plugin versions.

Requires python3

By Linus Bergman, 2021
"""

from pathlib import Path
import xml.etree.ElementTree as ET

AAXDIR = Path('/Library/Application Support/Avid/Audio/Plug-Ins')
AAX_UNUSEDDIR = Path(
    '/Library/Application Support/Avid/Audio/Plug-Ins (Unused)')
VSTDIR = Path('/Library/Audio/Plug-Ins/VST')
VST3DIR = Path('/Library/Audio/Plug-Ins/VST3')
AUDIR = Path('/Library/Audio/Plug-Ins/Components')

print("""
      Usage: By default, this utility will scan the default locations for AAX, VST, VST3 and AU plugins
      and save a list with plugin names and versions in 'pluginlist.txt'.

      If you run the utility multiple times without specifying a new filename, plugins will be appended
      to the end of the list meaning you will have duplicates. Either specify a new file name or delete 
      any previous versions of 'pluginlist.txt'.

      """)
FILENAME = input(
    'Enter a filename (leave blank for default "pluginlist.txt"): ')


def findVersion(format: str, plugDir: Path, FILENAME='pluginlist.txt'):
    with open(FILENAME, 'a') as f:
        for pluginPath in list(plugDir.glob('*.*')):
            plugin = str(pluginPath.stem)
            try:
                tree = ET.parse(f'{str(pluginPath)}/Contents/Info.plist')
                root = tree.getroot()
                elements = [elem.text for elem in root.iter()]
                tag = 'CFBundleShortVersionString'
                if tag in elements:
                    index = elements.index(tag)
                    version = elements[index + 1]
                    if version.startswith('0x'):
                        version = version.split()[-1]
            except:
                version = 'Info.plist not found'
            finally:
                if plugin.startswith('.'):
                    continue
                print(f'{format:15} {plugin:40} {version}', file=f)


findVersion('AAX', AAXDIR, FILENAME)
findVersion('AAX (Unused)', AAX_UNUSEDDIR, FILENAME)
findVersion('VST', VSTDIR, FILENAME)
findVersion('VST3', VST3DIR, FILENAME)
findVersion('AU', AUDIR, FILENAME)
