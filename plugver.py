#!/usr/bin/env python3
"""
plugver.py  v0.3
Utility for checking audio plugin versions.

Requires python3

By Linus Bergman, 2021
"""

from pathlib import Path
import xml.etree.ElementTree as ET
import csv

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
      and save a list with plugin names and versions in 'pluginlist.csv'.

      If you run the utility multiple times without specifying a new filename, plugins will be appended
      to the end of the list meaning you will have duplicates. Either specify a new file name or delete 
      any previous versions of 'pluginlist.csv'.

      """)
filename = input(
    'Enter a filename (leave blank for default "pluginlist.csv"): ')


def findVersion(filename='pluginlist.csv'):
    with open(filename, mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Type', 'Plugin Name', 'Version', 'Vendor', 'Get Info String'])

        def typeList(format: str, plugDir: Path, extension):
            for pluginPath in list(plugDir.glob(f'**/*.{extension}')):
                plugin = str(pluginPath.stem)
                try:
                    tree = ET.parse(f'{str(pluginPath)}/Contents/Info.plist')
                    root = tree.getroot()
                    elements = [elem.text for elem in root.iter()]
                    version_tag = 'CFBundleShortVersionString'
                    long_version_tag = 'CFBundleVersion'
                    manufacturer_tag = 'CFBundleIdentifier'
                    get_info_tag = 'CFBundleGetInfoString'
                    if version_tag in elements:
                        version_index = elements.index(version_tag)
                        version = elements[version_index + 1]
                    elif long_version_tag in elements:
                        version_index = elements.index(long_version_tag)
                        version = elements[version_index + 1]
                    else:
                        version = 'not found'

                    if get_info_tag in elements:
                        info_string = elements[elements.index(get_info_tag) +1 ]
                    else:
                        info_string = 'not found'

                    if version.startswith('0x'):
                        version = version.split()[-1]
                    if manufacturer_tag in elements:
                        manufacturer_index = elements.index(manufacturer_tag)
                        manufacturer_string = elements[manufacturer_index +
                                                       1].split('.')
                        if manufacturer_string[0].startswith('c'):
                            manufacturer = manufacturer_string[1]
                        elif manufacturer_string[0] == 'uvi':
                            manufacturer = manufacturer_string[0]
                        else:
                            # NI doesn't seem to include a vendor string
                            manufacturer = 'Native Instruments'
                    else:
                        manufacturer = 'not found'
                except:
                    version = ''
                finally:
                    if plugin.startswith('.') or version == '':
                        continue
                    writer.writerow([format, plugin, version, manufacturer, info_string])

        for extension in EXTENSIONS:
            typeList(*extension)


if filename:
    findVersion(filename)
else:
    findVersion()
