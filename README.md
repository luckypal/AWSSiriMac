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


# Siri HTTP API server.

## 1. Environment

```
DEVICE_NAME=m1
HOST=localhost
PORT=8080
```

## 2. Check server status

[GET] /

This shows the current server status and device name.

For example.
```
Device: m1
Status: Running
```

## 3. Start Process

```
[POST] /start
{
    "url": "LAMBDA_SERVER_URL",
    "excelId": "EXCEL_ID"
}
```

After get this request, server add the excelId to queue and ask tasks to process siri using below api.

## 4. Ask next task

Lambda instance has this api.

```
[GET] /getSiriTask?excelId=EXCEL_ID&deviceId=MY_DEVICE_ID
```

This api returns below data
```
{
    "success": "TRUE / FALSE",
    "excelId": "EXCEL_ID",
    "key": "EXCEL_KEY. ex: A1, A2, ...",
    "query": "What time is it?"
}
```

If `success` is false, the siri processing of the excel is all done. then remove the `excelId` from the Excel queue.

Server process query and get results from Siri of Mac. After process the query, siri server calls below API.

```
[POST] /uploadSiriResult
{
    "excelId": "EXCEL_ID",
    "key": "EXCEL_KEY. ex: A1, A2, ...",
    "text": "SIRI RESPONSE"
}
[FILE] "imageFile" [image/jpg]
```

After upload siri result to server, delete the image file from directory.

