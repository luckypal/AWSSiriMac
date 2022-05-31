import sys, ask_siri

def main():
	args = sys.argv

	if '-q' not in args:
		print('ERROR: Must provide query text (-q)', file=sys.stderr)
		sys.exit()

	query = args[args.index('-q') + 1]

	print(ask_siri.ask_siri(query))

if __name__ == '__main__':
	main()
