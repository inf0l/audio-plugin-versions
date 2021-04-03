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
filename = input(
    'Enter a filename (leave blank for default "pluginlist.txt"): ')


def findVersion(format: str,
                plugDir: Path,
                extension,
                filename='pluginlist.txt'):
    with open(filename, 'a') as f:
        for pluginPath in list(plugDir.glob(f'**/*.{extension}')):
            if 'Pace_Eden' in str(pluginPath):
                continue
            plugin = str(pluginPath.stem)
            try:
                tree = ET.parse(f'{str(pluginPath)}/Contents/Info.plist')
                root = tree.getroot()
                elements = [elem.text for elem in root.iter()]
                version_tag = 'CFBundleShortVersionString'
                manufacturer_tag = 'CFBundleIdentifier'
                if version_tag in elements:
                    version_index = elements.index(version_tag)
                    version = elements[version_index + 1]
                    if version.startswith('0x'):
                        version = version.split()[-1]
                if manufacturer_tag in elements:
                    manufacturer_index = elements.index(manufacturer_tag)
                    manufacturer = elements[manufacturer_index + 1]
                else:
                    manufacturer_tag = ''
            except:
                version = 'not found'
            finally:
                if plugin.startswith('.') or version == 'not found':
                    continue
                print(
                    f'{format:15} {plugin:40} {version:40} {manufacturer:>60}',
                    file=f)


findVersion('AAX', AAXDIR, 'aaxplugin', filename) if filename else findVersion(
    'AAX', AAXDIR, 'aaxplugin')
findVersion('AAX (Unused)', AAX_UNUSEDDIR,
            'aaxplugin', filename) if filename else findVersion(
                'AAX (Unused)', AAX_UNUSEDDIR, 'aaxplugin')
findVersion('VST', VSTDIR, 'vst', filename) if filename else findVersion(
    'VST', VSTDIR, 'vst')
findVersion('VST3', VST3DIR, 'vst3', filename) if filename else findVersion(
    'VST3', VST3DIR, 'vst3')
findVersion('AU', AUDIR, 'component', filename) if filename else findVersion(
    'AU', AUDIR, 'component')
