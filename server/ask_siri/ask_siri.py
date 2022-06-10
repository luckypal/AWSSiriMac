#!/usr/bin/env python

from os import mkdir, unlink
from shutil import move
import sys, subprocess, keyboard, time, re
import os.path
import os
from pathlib import Path
from PIL import Image

if sys.platform == "darwin":
	from AppKit import NSWorkspace
	from Quartz import (
		CGWindowListCopyWindowInfo,
		kCGWindowListOptionOnScreenOnly,
		kCGNullWindowID
	)

error_flag = '~*ERROR*~'
end_of_string_flag = '~*INTOUCH*~'
apple_ui_value_blacklist = [ 'missing value, ', '…, ' ]
siri_utterance_value_blacklist = [ 'App Store', 'Location Services' ]

maxHeight = 1260 # int(os.getenv('MAX_HEIGHT'))

applescripts = {
	'ask_siri': '''
		on run {s}	
			-- find Type to Siri prompt and enter text
			activate application "NotificationCenter"
			tell application "System Events" to tell the process "NotificationCenter"
				set notifyWindows to every window
				repeat with notifyWindow in notifyWindows
					if description of notifyWindow is "system dialog" then
						set elements to entire contents of notifyWindow
						tell (first text field of first group of first UI element of first scroll area of notifyWindow)
							set focused to true
							set value to s
							set siriWindow to notifyWindow
							perform action "AXConfirm"
							
							
						end tell
						exit repeat
					end if
				end repeat

				delay 3

				-- catch Siri crashing
				if exists (siriWindow) then
					-- get response as soon as it's ready
					set dataResponse to {}
					set utteranceResponse to {}
					set i to 0
					repeat while dataResponse is {} and i < 100
						try
							delay 0.05
							set i to (i + 1)
							set utteranceResponse to (get value of (every static text whose value of attribute "AXIdentifier" is "SiriServerUtterance") of group 1 of scroll area 1 of siriWindow)
							-- exit early if Siri needs your location
							if "Location Services" is in (utteranceResponse as string) then
								set dataResponse to "none"
							-- exit early if Siri didn't understand the query
							else if "App Store" is in (utteranceResponse as string) then
								set dataResponse to "none"
							else if "didn’t catch that" is in (utteranceResponse as string) then
								set dataResponse to "none"
							else if "didn’t find anything" is in (utteranceResponse as string) then
								set dataResponse to "none"
							-- exit early if Siri didn't understand the query
							else if "didn’t get that" is in (utteranceResponse as string) then
								set dataResponse to "none"
							-- don't accept responses with ellipsis
							else if "…" is not in (utteranceResponse as string) then
								-- wait for answer to load after utterance is updated
								delay 1
								set dataResponse to (get value of (UI elements) of group 1 of group 1 of scroll area 1 of siriWindow)
							end if
						end try
					end repeat
				else
					set utteranceResponse to "~*ERROR*~"
				end if

			end tell

			return utteranceResponse
		end run
	''',
	'close_siri': '''
		-- dismiss Type to Siri prompt
		activate application "NotificationCenter"
		tell application "System Events" to tell the process "NotificationCenter"
		set notifyWindows to every window
		repeat with notifyWindow in notifyWindows
			if description of notifyWindow is "system dialog" then
				set elements to entire contents of notifyWindow
				tell (first text field of first group of first UI element of first scroll area of notifyWindow)
					set focused to true
					-- set value to "What is Eylea?"
					set value to "Close Siri"
					perform action "AXConfirm"
				end tell
				exit repeat
			end if
		end repeat
	end tell
	''',
	'focus_siri': '''
		tell application "System Events" to tell process "Siri"
			-- make Type to Siri prompt the active (focused) window
			set frontmost to true
			delay 1
		end tell
	''',
	'recursively_scrape_siri_ui': '''
		activate application "NotificationCenter"
		tell application "System Events" to tell the process "NotificationCenter"
			set notifyWindows to every window
			repeat with notifyWindow in notifyWindows
				if description of notifyWindow is "system dialog" then
					set elements to entire contents of notifyWindow
					tell (first text field of first group of first UI element of first scroll area of notifyWindow)
						set siriWindow to notifyWindow
					end tell
					exit repeat
				end if
			end repeat
			tell siriWindow
				set response to my RecursivelyGetContent(UI elements, {})
			end tell
		end tell

		on RecursivelyGetContent(elements, results)
			using terms from application "System Events"
				repeat with element in elements
					tell element
						if UI elements is not {} then
							set end of results to my RecursivelyGetContent(UI elements, results)
						else
							set elementValue to (get value of element)
							if elementValue is not missing value then
								set end of results to elementValue & "~*INTOUCH*~"
							end if
						end if
					end tell
				end repeat
				return results
			end using terms from
		end RecursivelyGetContent

		return response
	''',
}

def open_siri():
	keyboard.press("command+space")
	time.sleep(0.3) # Hold command+space to trigger Siri
	keyboard.release("command+space")

def run_osascript(script, args = []):
	process = subprocess.Popen(["osascript", "-"] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	(output, error) = process.communicate(script)
	print(error, file=sys.stderr)
	return output

def get_active_window_id():
	current_app = NSWorkspace.sharedWorkspace().frontmostApplication()
	current_process_id = NSWorkspace.sharedWorkspace().activeApplication()["NSApplicationProcessIdentifier"]
	current_app_name = current_app.localizedName()
	options = kCGWindowListOptionOnScreenOnly
	window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)

	for window in window_list:
		process_id = window["kCGWindowOwnerPID"]
		window_number = window["kCGWindowNumber"]

		if current_process_id == process_id:
			return window_number

def screenshot_window(window_id, filename):
	subprocess.call(["screencapture", "-xl " + str(window_id), filename])

def parse_siri_output(output_list, query):
	data_list = re.sub(re.escape(query), '', output_list)
	data_list = re.sub(re.escape(end_of_string_flag + '\n'), '', data_list)
	for string in apple_ui_value_blacklist:
		data_list = re.sub(re.escape(string), '', data_list)
	deduped_list = []
	for item in data_list.split(end_of_string_flag + ','):
		trimmed_item = item.lstrip()
		if trimmed_item not in deduped_list:
			deduped_list.append(trimmed_item)
	result = ''
	for string in deduped_list:
		result += string + '\n'
	return result

def ask_siri(query, unique_id=None, image_filepath='images/'):
	open_siri()
	siri_utterance = run_osascript(applescripts['ask_siri'], [ query ])

	image_filename = None
	if unique_id != None:
		if Path(image_filepath).is_dir() == False:
			mkdir(image_filepath)
		image_filename = image_filepath + unique_id + '.jpg'
		screenshot_window(get_active_window_id(), image_filename)
		crop_image(image_filename)

	if error_flag in siri_utterance:
		response = 'ERROR'
		return response, image_filename

	for value in siri_utterance_value_blacklist:
		if value in siri_utterance:
			response = siri_utterance
			return response, image_filename

	scraped_data = run_osascript(applescripts['recursively_scrape_siri_ui'])
	run_osascript(applescripts['close_siri'])
	response = parse_siri_output(scraped_data, query)
	return response, image_filename

def crop_image(imageFilePath):
	img = Image.open(imageFilePath)
	if (img.height < maxHeight):
		return imageFilePath

	newImageFilePath = imageFilePath + '.cropped.png'
	newImg = img.crop((0, 0, img.width, maxHeight))
	newImg.save(newImageFilePath)
	unlink(imageFilePath)
	move(newImageFilePath, imageFilePath)
	return imageFilePath
