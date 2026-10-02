# entropy-peek

Estimate whole-file Shannon byte entropy and a few content-shape statistics without printing file bytes. Input is streamed in 64 KiB blocks, kept only as a fixed 256-entry counter, and limited to 512 MiB.

## Use

Requires Python 3.8+; no packages to install.

```sh
python entropy_peek.py archive.bin
```

The report includes file size, distinct byte values, entropy in bits per byte, printable ASCII share, and the most common byte's share without identifying that byte. These whole-file statistics can hide local patterns and cannot prove that data is encrypted, compressed, safe, or malicious. Exit status is 0 for a readable file (including an empty file), 1 for unsupported input, and 2 for unreadable input.

## License

MIT
