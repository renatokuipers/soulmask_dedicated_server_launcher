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

You can run the dedicated server launcher in 2 ways:

4.1 **Execute the Launcher with the .exe file:**
Double-click the `soulmask_dedicated_launcher.exe` file to run the launcher. A GUI will appear on your screen.

4.2 **Execute the launcher with the .py file:**
Make sure you have Python 3.10 or higher installed.
Then in Studio Code or Pycharm or just in a Terminal/CMD window go to the directory where all the downloaded files are.
Then run the command:
```
python soulmask_dedicated_launcher.py
```
and press enter.


5. **Check for Dedicated Server Installation:**
The GUI will automatically check if the Soulmask Dedicated Server is installed at the following location:
```
C:\steamcmd\steamapps\common\Soulmask Dedicated Server For Windows
```

If the server is not found in this location, the GUI will prompt you to install the server.
(When you click on "Install Server" it will seem as if nothing is happening, but the full server will be downloaded through SteamCMD. This can take about 1-3 minutes depending on your internet speed, so please have patience.)
Once done, the Launcher will tell you that the server is installed correctly.

5. **Install the Server:**
If the server is not installed, click the "Install Server" button in the GUI. This will install the server in the default location mentioned above.

6. **Configure the Server:**
The GUI allows you to edit and save the configuration files (`Engine.ini` and `config.json`). Note that as of now, the launcher GUI only supports editing and saving configuration files.

7. **Starting and Stopping the Server:**
- To start the server, click the "Start Server" button in the GUI.
- To stop the server, click the "Stop Server" button in the GUI. 
  - **Important:** To stop the server properly, first activate the server window (which should be completely empty since the log will be in the GUI) and then click once, then press `Ctrl+C`. If nothing happens in the GUI log, press `Ctrl+C` again. **Do not close the server window directly** to avoid corrupted server files or rollbacks.

## Future Updates

- The launcher will soon include enhanced features for stopping the dedicated server directly from the GUI.

## Contributing

If you wish to contribute to this project, please fork the repository and submit a pull request with your changes. Ensure that your contributions align with the overall project goals and coding standards.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
