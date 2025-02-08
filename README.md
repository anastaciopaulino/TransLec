# TransLec

TransLec is a Python project that translates subtitle files (`.srt` and `.vtt`) into a specified target language using the [googletrans](https://pypi.org/project/googletrans/) library. The project supports batch translation, caching, and provides a console spinner for visual feedback during the translation process.

## Features

- **Batch Translation:** Translates multiple lines at once to improve performance.
- **Translation Cache:** Caches translations to avoid redundant API calls.
- **Console Spinner:** Displays an animated spinner during file processing.
- **Directory Translation:** Recursively translates all subtitle files in a directory.
- **Customizable Logging:** Filters out non-critical errors (e.g., batch translation errors) from being displayed.
- **Interactive Overwriting:** Prompts the user before overwriting existing translated files (with an option to override).

## Project Structure

```
project/
├── main.py
├── README.md
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── translator.py       # Contains the SubtitleTranslator class.
│   └── utils/
│       ├── __init__.py
│       ├── log_filter.py       # Contains the logging filter to ignore specific errors.
│       └── spinner.py          # Contains the Spinner class.
└── tests/
    ├── __init__.py
    └── test_translator.py      # Unit tests for the translator functionality.
```

## Requirements

- **Python:** 3.7 or higher
- **Dependencies:**  
  - [googletrans](https://pypi.org/project/googletrans/) (recommended version: `4.0.0-rc1`)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/subtitle-translator.git
   cd subtitle-translator
   ```

2. **Create a Virtual Environment (Optional, but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   If you have a `requirements.txt` file, install the dependencies with:

   ```bash
   pip install -r requirements.txt
   ```

   Otherwise, install the required package manually:

   ```bash
   pip install googletrans==4.0.0-rc1
   ```

## Usage

Run the application from the command line with:

```bash
python main.py <directory> <target_language>
```

For example, to translate subtitles in `/path/to/subtitles` to English:

```bash
python main.py /path/to/subtitles en
```

### Overwriting Existing Files

By default, the program prompts before overwriting an existing translated file. To automatically overwrite files, you can modify the call to `translate_directory` in `main.py` (or pass the `overwrite_existing=True` parameter programmatically).

## Testing

The project uses Python’s built-in `unittest` framework.

To run all tests, execute the following command from the project’s root directory:

```bash
python -m unittest discover tests
```

Alternatively, you can use [pytest](https://docs.pytest.org/):

1. **Install pytest:**

   ```bash
   pip install pytest
   ```

2. **Run pytest:**

   ```bash
   pytest
   ```

## Logging

- **Custom Logging Filter:** A custom filter (`IgnoreBatchTranslationErrorFilter`) is used to suppress non-critical batch translation errors.
- **Suppressing Internal Library Logs:** You can suppress logs from the `googletrans` library by adding:

  ```python
  import logging
  logging.getLogger("googletrans").setLevel(logging.CRITICAL)
  ```

  This ensures that only critical messages from the library are displayed.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.