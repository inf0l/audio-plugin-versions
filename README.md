# audio-plugin-versions

Small utility that will scan /Library/Application Support/ subfolders
for audio plugins (VST(3), AU, AAX) and create a .txt file containing
plugin names and versions.

#### Update 2:

Some plugins don't use 'CFBundleShortVersionString' so have included 'CFBundleVersion' as fallback.

#### Update:

Now includes CFBundleIdentifier (vendor info) and searches subfolders recursively.

## Usage

Directories are hardcoded so you can run it from any folder where you wish
to store the resulting text file.

## Requirements

Requires python3, but other than that relies on standard library modules.

Mac only (for the time being).
