import os
import logging
from googletrans import Translator
from src.utils.spinner import Spinner

# Cria um logger para este módulo
logger = logging.getLogger(__name__)

class SubtitleTranslator:
    """
    A class to handle subtitle file translations using googletrans.
    """
    def __init__(self, target_language: str):
        """
        Initializes the translator with the target language code.
        
        :param target_language: Language code (e.g., 'en' for English).
        """
        self.target_language = target_language
        self.translator = Translator()
        # Cache to avoid re-translating duplicate lines.
        self.translation_cache: dict[str, str] = {}

    def get_translated_file_path(self, file_path: str) -> str:
        """
        Generates the file path for the translated subtitle file.
        The translated file is stored in a subdirectory named after the target language.
        
        :param file_path: Original file path.
        :return: File path for the translated file.
        """
        directory, file_name = os.path.split(file_path)
        base, ext = os.path.splitext(file_name)
        output_dir = os.path.join(directory, self.target_language)
        translated_file_name = f"{base}_{self.target_language}{ext}"
        return os.path.join(output_dir, translated_file_name)

    def translate_text(self, text: str) -> str:
        """
        Translates a single line of text using googletrans.
        Checks the cache before performing a translation.
        
        :param text: Text to be translated.
        :return: Translated text, or the original text if translation fails.
        """
        if not text.strip():
            return text

        if text in self.translation_cache:
            return self.translation_cache[text]

        try:
            translation = self.translator.translate(text, dest=self.target_language)
            if translation is None or not hasattr(translation, 'text') or not translation.text:
                self.translation_cache[text] = text
                return text
            translated_text = translation.text
            self.translation_cache[text] = translated_text
            return translated_text
        except (AttributeError, TypeError):
            self.translation_cache[text] = text
            return text
        except Exception as e:
            logger.error(f"Error translating text: '{text}' - {str(e)}")
            self.translation_cache[text] = text
            return text

    def translate_file(self, file_path: str) -> str:
        """
        Translates the content of a subtitle file.
        Uses batch translation for improved performance.
        
        :param file_path: Path to the subtitle file.
        :return: Translated file content.
        :raises FileNotFoundError: If the file does not exist.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        is_vtt = file_path.lower().endswith('.vtt')
        translated_lines: list[str] = []
        # Indices for lines that require translation.
        indices_to_translate: list[int] = []
        # Original texts that need to be translated.
        texts_to_translate: list[str] = []

        # Preserve the "WEBVTT" header if this is a VTT file.
        start_index = 0
        if is_vtt and lines and lines[0].strip() == "WEBVTT":
            translated_lines.append("WEBVTT")
            start_index = 1

        # Process each line.
        for idx, line in enumerate(lines[start_index:], start=start_index):
            stripped_line = line.strip()
            # Translate only lines that are not indices or time markers.
            if stripped_line and not stripped_line.isdigit() and "-->" not in stripped_line:
                if stripped_line in self.translation_cache:
                    translated_lines.append(self.translation_cache[stripped_line])
                else:
                    indices_to_translate.append(len(translated_lines))
                    texts_to_translate.append(stripped_line)
                    translated_lines.append("")  # Placeholder
            else:
                translated_lines.append(stripped_line)

        # Batch translation if there are texts to translate.
        if texts_to_translate:
            try:
                translations = self.translator.translate(texts_to_translate, dest=self.target_language)
                if not isinstance(translations, list):
                    translations = [translations]
                for index, original_text, translation in zip(indices_to_translate, texts_to_translate, translations):
                    translated_text = (translation.text
                                       if translation and hasattr(translation, 'text') and translation.text
                                       else original_text)
                    self.translation_cache[original_text] = translated_text
                    translated_lines[index] = translated_text
            except Exception as e:
                logger.error(f"Batch translation error: {str(e)}. Falling back to individual translations.")
                # Fallback: traduz cada linha individualmente.
                for index, original_text in zip(indices_to_translate, texts_to_translate):
                    translated_text = self.translate_text(original_text)
                    translated_lines[index] = translated_text

        return "\n".join(translated_lines)

    def save_translated_file(self, translated_file_path: str, translated_content: str) -> str:
        """
        Saves the translated content to the specified file path.
        
        :param translated_file_path: Destination file path.
        :param translated_content: The translated subtitle content.
        :return: The path where the translated file was saved.
        """
        output_dir = os.path.dirname(translated_file_path)
        os.makedirs(output_dir, exist_ok=True)

        with open(translated_file_path, 'w', encoding='utf-8') as file:
            file.write(translated_content)

        return translated_file_path

    def translate_directory(self, directory_path: str, overwrite_existing: bool = False) -> None:
        """
        Translates all subtitle files (.srt, .vtt) in the given directory and its subdirectories.
        
        :param directory_path: The directory containing subtitle files.
        :param overwrite_existing: If True, existing translated files will be overwritten without prompting.
        :raises NotADirectoryError: If the directory does not exist.
        """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Directory not found: {directory_path}")

        for root, dirs, files in os.walk(directory_path):
            # Skip directories that match the target language.
            dirs[:] = [d for d in dirs if d != self.target_language]

            for file_name in files:
                if file_name.endswith(('.srt', '.vtt')):
                    file_path = os.path.join(root, file_name)
                    translated_file_path = self.get_translated_file_path(file_path)

                    if os.path.exists(translated_file_path):
                        if not overwrite_existing:
                            choice = input(
                                f"\nFile '{os.path.basename(translated_file_path)}' already exists. Overwrite? (y/n): "
                            ).strip().lower()
                            if choice != 'y':
                                logger.info(f"Skipping file: {file_name}")
                                continue
                        else:
                            logger.info(f"Overwriting existing file: {translated_file_path}")

                    spinner = Spinner(f"Translating {file_name}")
                    try:
                        spinner.start()
                        translated_content = self.translate_file(file_path)
                        self.save_translated_file(translated_file_path, translated_content)
                    except Exception as e:
                        spinner.stop()
                        logger.error(f"Error translating '{file_name}': {str(e)}")
                    else:
                        spinner.stop()
                        logger.info(f"✓ '{file_name}' translated -> {os.path.relpath(translated_file_path)}")
