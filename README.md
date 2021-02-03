# MaxTime-2.0 Software-In-The-Loop (SIL)

The purpose of this script is to simplify the use of MaxTime 2.0 SIL for VISSIM. At the time of this writing (Sept 2020), MaxTime 2.0 is unable to automatically launch and close the signal controllers for each simulation run. This leads to increased analyst time to start and stop the controller for each run. Apparently version 1.9 was able to do this, but I was unable to get it to work for multiple intersections and from what I could tell testing with a single intersection it didn't seem to stop the signal controller at the end of the simulation, it simply started a new one which could cause issues.  It is very possible I was doing something wrong, but I couldn't figure it out and using the newer version was preferable.

# Set up to Run

There are a few steps that need to be taken to run this.

1. Install MaxTime 2.0 Windows Emulator. This can be installed from the Intelight website.
2. Add Maxtime.dll, Maxtime.wtt, and STDSC_GUI.dll to the PTV Program files folder (For example: C:\Program Files\PTV Vision\PTV Vissim 2020\Exe). Make sure it is the version of VISSIM you are using. You may need admin access for this step. These files can be copied from the Intelight website.
3. At this point you should be able to run files set up using this script.


# Set up a File
1. It is assumed you have a VISSIM File already set up with 1 or more signals and a MaxTime database file for each signal.
2. Set up each Signal Controller in VISSIM.
  - The Type should be set to external
  - The Program file should be set to the MaxTime.dll copied to the program files previously.
  - The Dialog DLL file should be set to the STDSC_GUI.dll copied to the program files previously.
  - WTT files should only have Maxtime.wtt that was copied to the program files previously.
  - Click on Edit Signal Control 
     - The computer name should be set to 127.0.0.1
    - The port should be set to a number unique for the project (We started at 9931 and counted up for each intersection)
    - Each phase being simulated should be set up on the signal control page.
  - Open up the start_script.py file in Notepad or Notepad++, near the top look for the block starting with `SCs = [`
  - In this block you will have one line for each signal controller you need. It will look like this:

```python
  SCs = [
    (1, "Intersection 1", "127.0.0.1", 9931, 81, 1010),
    (2, "Intersection 2", "127.0.0.1", 9932, 82, 1020),
    (3, "Intersection 3", "127.0.0.1", 9933, 83, 1030),
]
```

  - The values are as follows:
    - The first number is the SC id from VISSIM. 
    - The second value is the database file name (if in a different folder, use forward slashes ie `"folder/database_file_name"`. 
    - The third value is the IP address set in the previous step. 
    - The fourth value is the port number set in the previous step.
    - The fifth value is the web port number you can use to access the maxtime display
    - The sixth value is an additional port number used internally, but not accesible to you. This can be any open port value and should be unique.
  - Next go back to VISSIM and go to the Event Driven Scripts menu. You want to have 2 scripts set up:
    - Script 1: Run before simulation start, scope: Simulation Run, script file: start_script.py, FuncName: start
    - Script 2 Run after simulation end, scope: Simulation Run, script file: start_script.py, FuncName: end
  - You should now be able to run the simulation model. No additional windows will pop up, but the simulation will start with the signal controllers running. If you want to see the Maxtime view, go to 127.0.0.1:WebPort/maxtime where WebPort is the second to last value in the input list above for the signal you want to view. For example, 81 for intersection ID 1 above.
  - If you get a message that states it can't create something that already exists, go to "%LOCALAPPDATA%\Programs\MAXTIME\resources\app\res\node_modules\\@intelight\maxtime-windows\Release\maxtime\tmpDatabases" and delete all the folders in there. Restart the simulation.


# Scenario Manager
If using scenario manager, place the py and bat files in the scenario folder with the scprops and database file. Use a modification file to correctly set the script launcher to the scenario folder `#scenario#`. This will allow the script to automatically pull the database file for the active scenario.
