# Bash script for confirming that the CLI works

CMD="python3 app/pysmv.py"

# Run default help message
$CMD --help

# Run npfetch help
$CMD npfetch --help

# Run nvefetch
$CMD nvefetch --help

# Run info
$CMD info --help

# Run unique
$CMD unique --help