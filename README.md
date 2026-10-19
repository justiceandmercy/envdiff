# envdiff

Compare `.env` files in a project and report key mismatches: missing keys, keys
present in only one file, empty values, and duplicate keys.

## Features

- Auto-discovers `.env*` files in a directory
- Compares any number of env files at once
- Reports keys missing from one file but present in another
- Flags keys that exist in only one file
- Detects empty values and duplicate keys
- Zero dependencies, pure standard library
- Exit code `1` when issues are found (CI-friendly)

## Install

No installation required. Clone and run with Python 3.9+:

```sh
git clone https://github.com/yourname/envdiff
cd envdiff
python3 envdiff.py
```

Or copy `envdiff.py` and `core.py` into your project.

## Usage

Auto-discover env files in the current directory:

```sh
python3 envdiff.py
```

Compare specific files:

```sh
python3 envdiff.py .env .env.example .env.local
```

Scan a different directory:

```sh
python3 envdiff.py --dir path/to/project
```

Example output:

```
Comparing 2 env files:
  - .env
  - .env.example
Total unique keys: 4

Missing keys (present in another file but not here):
  .env.example:
    - DATABASE_URL
    - SECRET_KEY

Keys present in only one file:
  .env: DEBUG

Empty values:
  .env: API_KEY

All env files are in parity. No issues found.
```

## License

MIT
