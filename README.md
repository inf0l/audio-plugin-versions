# audio-plugin-versions

Small utility that will scan /Library/ and subfolders
for audio plugins (VST(3), AU, AAX) and create a .csv file containing
plugin names and versions.

## Usage

Run `python3 plugver.py` and follow the instructions.

Directories are hardcoded so you can run it from any folder where you wish
to store the resulting CSV file.

## Requirements

Requires python3, but other than that relies on standard library modules.

Python3 can be installed via [Homebrew](https://brew.sh/) if it's not already installed.

Mac only (for the time being).

## Versions

#### 0.3

Now exports a .csv file instead. CFBundleIdentifier string is parsed to only show vendor id.

###### Known issues

From the plugins I personally own, only Native Instruments does not provide a proper CFBundleIdentifier (they list the plugin name instead of vendor name),
so I've hardcoded 'Native Instruments' to be the vendor id if CFBundleIdentifier is 'incorrect'. This might lead to some plugins falsely being labeled as 
NI plugins - let me know if you come across any plugins where this is the case.

#### 0.2.1:

Some plugins don't use 'CFBundleShortVersionString' so have included 'CFBundleVersion' as fallback.

#### 0.2:

Now includes CFBundleIdentifier (vendor info) and searches subfolders recursively.

#### 0.1

...
