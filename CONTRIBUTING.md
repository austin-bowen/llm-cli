# Setup

```bash
uv python pin 3.10
uv venv
uv sync --dev
```

# Upgrading Dependencies

```bash
uv lock --upgrade && uv sync
```

# Linting and Formatting

```bash
./bin/format
```

# Bumping version

```bash
uv version --bump <major|minor|patch>
```
