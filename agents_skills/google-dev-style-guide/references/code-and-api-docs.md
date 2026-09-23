# Code Samples, Technical Elements, and API References (Google Developer Docs Style Guide)

## 1. Inline Code Formatting
- Use code font (backticks `` `code` ``) for:
  - Filenames, file extensions, and directory paths (`config.json`, `.png`, `/usr/local/bin`).
  - Class names, interface names, method names, function names, and properties (`HttpClient`, `parse_json()`, `length`).
  - Variables, parameters, and arguments (`user_id`, `--verbose`, `null`, `true`).
  - HTTP methods, headers, and status codes (`GET`, `Authorization`, `404 Not Found`).
  - Commands, flags, and CLI parameters (`git checkout -b`, `--output=json`).

## 2. Code Block Guidelines
- **Specify Language Tags:** Every code snippet must specify a syntax-highlighting language tag (e.g., ```python, ```bash, ```json).
- **Clean CLI Commands:**
  - Omit shell prompt symbols (`$` or `#`) from code blocks intended for copy-pasting.
  - *Incorrect:*
    ```bash
    $ npm install express
    ```
  - *Correct:*
    ```bash
    npm install express
    ```
  - Exception: Use `$` or `#` only when illustrating interactive terminal output where input and output must be explicitly distinguished.

- **Runnable & Minimal Examples:** Code snippets should be complete enough to run or adapt directly. Provide necessary imports and context.
- **No Hardcoded Credentials:** Never include real API keys, tokens, passwords, or personal endpoints. Use standard placeholders like `YOUR_API_KEY`, `example.com`, or `user@example.com`.

## 3. Parameter & Property Tables
When documenting functions, methods, API endpoints, or configurations, structure parameter descriptions consistently:

| Parameter | Type | Required / Optional | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `api_key` | `string` | **Required** | N/A | The API authentication key issued by the developer console. |
| `timeout` | `integer` | Optional | `30` | Request timeout duration in seconds. |

## 4. Error Messages & Troubleshooting
- Document exact error messages in code font.
- Explain **why** the error occurs and provide concrete steps to **resolve** it.
- State prerequisites before procedural steps, not after an error occurs.
