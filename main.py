#!/usr/bin/env python3
"""
Main entry point for the Subtitle Translator application.
Usage: python main.py <directory> <target_language>
Example: python main.py /path/to/subtitles en
"""
import sys
import os
import logging
from src.core.translator import SubtitleTranslator
from src.utils.log_filter import IgnoreBatchTranslationErrorFilter

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <directory> <target_language>")
        print("Example: python main.py /path/to/subtitles en")
        sys.exit(1)

    # Converte o diretório para o caminho absoluto
    directory_path = os.path.abspath(sys.argv[1])
    target_language = sys.argv[2]

    if not os.path.isdir(directory_path):
        print(f"Directory not found: {directory_path}")
        sys.exit(1)

    # Configuração do logging global
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.addFilter(IgnoreBatchTranslationErrorFilter())

    translator = SubtitleTranslator(target_language)
    translator.translate_directory(directory_path)
    print("Translation completed.")

if __name__ == "__main__":
    main()
