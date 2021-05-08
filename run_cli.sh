# Bash script for confirming that the CLI works

CMD="python3 app/pysmv.py"

# Run default help message
$CMD --help

# Run npfetch help
$CMD npfetch --help

$CMD npfetch npdata_test.csv
rm npdata_test.csv

# Run nvefetch
$CMD nvefetch --help

$CMD nvefetch https://nvebiapi.nve.no/api/Magasinstatistikk/HentOffentligData nvedata_test.csv
rm nvedata_test.csv