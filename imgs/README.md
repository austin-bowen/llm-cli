# How did I generate these files?

## `demo1.cast`
```bash
asciinema rec -q demo1.cast
```

## `demo1.gif`

```bash
# Install agg
cd tmp
git clone https://github.com/asciinema/agg
cd agg
sudo docker build -t agg .
cd ../..

# Generate gif
sudo docker run --rm -it -u $(id -u):$(id -g) -v $PWD:/data agg demo1.cast demo1.gif
```

# Problem

The gif doesn't support emojis and I'm tired of trying to get this to work.
