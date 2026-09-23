---
name: magika
description: >-
  Detect and determine file content types, MIME types, and binary file formats using Google's Magika
  deep-learning model. Use when identifying unknown files, verifying binary formats, checking file signatures,
  or inspecting uploaded assets, scripts, documents, archives, or datasets without relying solely on file extensions.
---

# Magika: Deep Learning File Content-Type Detector

[Magika](https://github.com/google/magika) is Google's AI-powered file type detection tool. It uses a custom, highly-optimized deep learning model (ONNX runtime) to accurately detect file formats in milliseconds, even for files without extensions or with deceptive extensions.

## CLI Usage

Magika is installed globally via `uv tool`:

```bash
# Basic file identification
magika <path-to-file>

# Recursive directory scan
magika -r <directory>

# Output MIME type only
magika -i <path-to-file>

# Output label only (e.g. 'python', 'pdf', 'elf', 'png')
magika -l <path-to-file>

# Output score / confidence along with content type
magika -s <path-to-file>

# Output structured JSON
magika --json <path-to-file>

# Output structured JSON Lines (great for streaming / batch processing)
magika --jsonl <path-to-file-or-dir>

# Read from stdin
cat sample.bin | magika -
```

## Python API Usage

Magika is also available as a Python package (`magika`):

```python
from magika import Magika

m = Magika()

# Identify from path
result = m.identify_path("data/sample.unknown")
print(result.output.ct_label)      # e.g., 'pdf'
print(result.output.mime_type)     # e.g., 'application/pdf'
print(result.output.score)         # e.g., 0.99
print(result.output.description)   # e.g., 'PDF document'

# Identify from in-memory bytes
with open("data/sample.unknown", "rb") as f:
    content = f.read()
result = m.identify_bytes(content)
print(result.output.ct_label)
```

## Supported Formats & Capabilities

- **100+ File Types**: Executables (`elf`, `pe`, `macho`), documents (`pdf`, `docx`, `odt`, `epub`), archives (`zip`, `tar`, `gzip`, `7z`), source code (`python`, `javascript`, `c`, `rust`, `html`, `json`), and media (`png`, `jpeg`, `webp`, `mp3`, `mp4`).
- **Deceptive Extension Detection**: Detects executable payloads or scripts disguised as images or text files.
- **Microsecond Inference**: Powered by an ONNX runtime architecture executing in <5ms per file.
