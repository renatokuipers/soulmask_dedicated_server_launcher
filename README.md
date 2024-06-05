# Soulmask Dedicated Server Launcher

## Overview

This repository contains files necessary to set up and configure the Soulmask Dedicated Server. The provided files include configuration files and a launcher script that facilitates the installation and management of the server.

## Repository Contents

- `Engine.ini` - Predefined engine configuration.
- `config.json` - Predefined JSON configuration.
- `soulmask_dedicated_launcher.py` - Python script for launching and managing the server.
- `soulmask_dedicated_launcher.exe` - Executable file for the launcher.
- `translations.py` - Predefined translations for the server configuration.

## Setup Instructions

1. **Download and Extract Files:**
   Download the repository and extract all files into a single folder. It is recommended to place this folder on the `C:` drive for ease of access.

2. **Folder Structure:**
   Ensure the folder contains the following files:
   ```
   - Engine.ini
   - config.json
   - soulmask_dedicated_launcher.py
   - soulmask_dedicated_launcher.exe
   - translations.py
   ```

3. **Execute the Launcher:**
   Double-click the `soulmask_dedicated_launcher.exe` file to run the launcher. A GUI will appear on your screen.

4. **Check for Dedicated Server Installation:**
   The GUI will automatically check if the Soulmask Dedicated Server is installed at the following location:
   ```
   C:\steamcmd\steamapps\common\Soulmask Dedicated Server For Windows
   ```
   If the server is not found in this location, the GUI will prompt you to install the server.

5. **Install the Server:**
   If the server is not installed, click the "Install Server" button in the GUI. This will install the server in the default location mentioned above.

6. **Configure the Server:**
   The GUI allows you to edit and save the configuration files (`Engine.ini` and `config.json`). Note that as of now, the launcher GUI only supports editing and saving configuration files. The ability to run or stop the server is not yet implemented.
   As of right now, you can just edit the StartServer.bat file and start the server that way. (See https://soulmask.fandom.com/wiki/Private_Server for the current possible .bat implementation)

## Future Updates

- The launcher will soon include features to start and stop the dedicated server directly from the GUI.
- Additional configuration options and enhancements are planned for future releases.

## Contributing

If you wish to contribute to this project, please fork the repository and submit a pull request with your changes. Ensure that your contributions align with the overall project goals and coding standards.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
