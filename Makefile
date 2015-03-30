all:
	./venv/bin/pyinstaller --distpath=bin --workpath=pyinstaller -n vet --onedir --log-level DEBUG main.py -r sqlitedll/sqlite.dll -r sqlite.def
	rm -r pyinstaller
