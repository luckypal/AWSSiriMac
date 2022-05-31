You must have Homebrew installed to follow these instructions:

1. Install NodeJS and npm<br>
    `brew install node`<br><br>

2. Install Python 3.8 or greater<br>
    `brew install python3`<br><br>

3. Install keyboard and applescript using Pip3<br>
    `pip3 install keyboard applescript`<br><br>

4. Enable "Type to Siri"<br>
    `System Preferences > Accessibility > Siri > Enable Type to Siri`<br><br>

5. Disable Siri "Voice Feedback"<br>
    `System Preferences > Siri > Voice Feedback`<br><br>

6. Add items to Accessibility security preferences:<br><br>
    Enable Terminal accessibility<br>
    `System Preferences > Security & Privacy > Privacy > Accessibility > Terminal`<br><br>
    Enable Automator accessibility<br>
    `System Preferences > Security & Privacy > Privacy > Accessibility > Automator`<br><br>
    Enable VSCode accessibility<br>
    `System Preferences > Security & Privacy > Privacy > Accessibility > VSCode`<br><br>
    **Note**: You may need to add additional terminal apps here, such as iTerm2 or AppleScript Editor.<br><br>

7. Clone the repository and open the folder in VSCode<br><br>

8. Install VSCode Python extension<br><br>

9. Select Python 3.8 interpreter in VSCode<br><br>

10. Add Configuration for VSCode Python Debugger<br><br>

11. Invoke from the command line:<br>
`python3 ask_siri -q "What is Eylea?"`<br><br>

Or import as a Python module:<br>
    `import ask_siri`<br><br>