#! /usr/bin/python2

import gtk
import sys
import argparse
import platform


root = gtk.gdk.get_default_root_window()

def find_gtk_window(xid):
	xid = int(xid, 16)
	for id in root.property_get('_NET_CLIENT_LIST')[2]:
		gtk_window = gtk.gdk.window_foreign_new(id)
        if gtk_window.xid == xid:
            return gtk_window

def list(geometry, wmClass, decimal):
	for id in root.property_get('_NET_CLIENT_LIST')[2]:
		wnd = gtk.gdk.window_foreign_new(id)
		if wnd:
			if wnd.property_get('WM_NAME'):
				title = wnd.property_get('WM_NAME')[2]
				wndStr = str("0x%x"%wnd.xid if not decimal else wnd.xid)
				wndStr += "\t-desktop-id-"
				if geometry:
					width, height = wnd.get_size()
					x, y = wnd.get_position()
					wndStr += "\t{}\t{}\t{}\t{}".format(x, y, x+width, y+height)
				if wmClass:
					wndStr += "\t" + wnd.property_get('WM_CLASS')[2] #FIXME: value lacks dot in the middle
				wndStr += "\t" + platform.node() + "\t" + title
				print wndStr

def manager_info():
	print "Name: " + "N/A" + "\nClass: " + "N/A" + "\nPID: " + "N/A" + "\nWindow manager's \"showing the desktop\" mode: " + "N/A"

def change_state(wnd, action, properties, mode):
	wnd = (find_gtk_window() if mode == 'id' or mode == 'integer' else None)
	if not wnd:
		print "Specified window not found."
		return
	properties = properties.split(',')
	for prop in properties:
		if prop == "above":
			wnd.set_keep_above(True if action == "add" else False)
		elif prop == "below":
			wnd.set_keep_below(True if action == "add" else False)
		else:
			print "Unknown property '{}'".format(prop)
	print "Done!"


def main():
	parser = argparse.ArgumentParser(prog="pywmctrl", description='wmctrl replacement coded in python')
	# Actions
	parser.add_argument('-m', '--manager', 	help='Show information about the window manager and about the environment.', 	action='store_true')
	parser.add_argument('-l', '--list', 	help='List windows managed by the window manager.', 							action='store_true')
	parser.add_argument('-d', '--desktops', help='List desktops. The current desktop is marked with an asterisk.', 			action='store_true')
	parser.add_argument('-r', 				help='This argument specifies the window. By default it\'s interpreted as a case-insensitive string.', type=str, dest='_win_')
	parser.add_argument('-b', 				help='Change the state of the _WIN_ window. Using this option it\'s possible for example to make the window maximized,'
												 ' minimized or fullscreen.', type=str, dest='_starg_')
	# Options
	parser.add_argument('-i', '--integer',	help='Interpret _WIN_ as a numerical window ID or list window ids as decimal numbers.',  action='store_true')
	parser.add_argument('-G', '--geometry', help='Include geometry in the window list.',										 	 action='store_true')
	parser.add_argument('-x', 				help='Include WM_CLASS in the window list or interpret <WIN> as the WM_CLASS name.', 	 action='store_true', dest='wmclass')

	args = parser.parse_args()

	if len(sys.argv) <= 1:
		parser.print_help()
		print "\nAuthor: Chlorek <chlorek@protonmail.com>\nLicense: GNU General Public License v2\nCopyright 2015-2017"
		return

	if args.list:
		list(args.geometry, args.wmclass, args.integer)
	elif args.manager:
		manager_info()
	elif args._starg_:
		if args._win_ == None:
			print "Argument -b requires -r _WIN_ to complete an action."
			return
		action_params = args._starg_.split(',', 2)
		if len(action_params) < 2:
			print "Invalid _STARG_ syntax."
			return
		change_state(args._win_, action_params[0], action_params[1], 'string' if not args.integer else 'id')

if __name__ == "__main__":
    main()
