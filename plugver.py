#!/usr/bin/env python3
"""
Utility for checking audio plugin versions.

Requires python3

By Linus Bergman, 2021
"""

from pathlib import Path
import xml.etree.ElementTree as ET

EXTENSIONS = [
    [
        'AAX',
        Path('/Library/Application Support/Avid/Audio/Plug-Ins'), 'aaxplugin'
    ],
    [
        'AAX (Unused)',
        Path('/Library/Application Support/Avid/Audio/Plug-Ins (Unused)'),
        'aaxplugin'
    ], ['VST', Path('/Library/Audio/Plug-Ins/VST'), 'vst'],
    ['VST3', Path('/Library/Audio/Plug-Ins/VST3'), 'vst3'],
    ['AU', Path('/Library/Audio/Plug-Ins/Components'), 'component']
]

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
            plugin = str(pluginPath.stem)
            try:
                tree = ET.parse(f'{str(pluginPath)}/Contents/Info.plist')
                root = tree.getroot()
                elements = [elem.text for elem in root.iter()]
                version_tag = 'CFBundleShortVersionString'
                long_version_tag = 'CFBundleVersion'
                manufacturer_tag = 'CFBundleIdentifier'
                if version_tag in elements:
                    version_index = elements.index(version_tag)
                    version = elements[version_index + 1]
                elif long_version_tag in elements:
                    version_index = elements.index(long_version_tag)
                    version = elements[version_index + 1]
                else:
                    version = 'not found'
                if version.startswith('0x'):
                    version = version.split()[-1]
                if manufacturer_tag in elements:
                    manufacturer_index = elements.index(manufacturer_tag)
                    manufacturer = elements[manufacturer_index + 1]
                else:
                    manufacturer = 'not found'
            except:
                version = ''
            finally:
                if plugin.startswith('.') or version == '':
                    continue
                print(
                    f'{format:15} {plugin:40} {version:40} {manufacturer:>60}',
                    file=f)


for extension in EXTENSIONS:
    if filename:
        findVersion(*extension, filename)
    else:
        findVersion(*extension)
