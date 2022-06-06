import sys, ask_siri

def main():
	args = sys.argv

	if '-q' not in args:
		print('ERROR: Must provide query text (-q)', file=sys.stderr)
		sys.exit()

	query = args[args.index('-q') + 1]
	unique_id = None
	if '-id' in args:
		unique_id = args[args.index('-id') + 1]

	print(ask_siri.ask_siri(query, unique_id = unique_id))

if __name__ == '__main__':
	main()
