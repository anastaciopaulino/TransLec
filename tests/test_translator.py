import os
import unittest
from unittest.mock import MagicMock
from src.core.translator import SubtitleTranslator

class TestSubtitleTranslator(unittest.TestCase):
    def setUp(self):
        # Inicializa o tradutor com idioma de destino 'pt'
        self.translator = SubtitleTranslator('pt')
        self.test_file = 'test_file.srt'
        # Cria um arquivo de legenda de teste
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("1\n00:00:01,000 --> 00:00:02,000\nHello, world!\n")
        
        # "Mocka" o método translate para evitar chamadas reais à API
        def fake_translate(text, dest):
            if isinstance(text, list):
                result = []
                for t in text:
                    if t.strip() == "Hello, world!":
                        result.append(MagicMock(text="Olá, mundo!"))
                    else:
                        result.append(MagicMock(text=f"Translated: {t}"))
                return result
            else:
                if text.strip() == "Hello, world!":
                    return MagicMock(text="Olá, mundo!")
                else:
                    return MagicMock(text=f"Translated: {text}")
        self.translator.translator.translate = fake_translate

    def tearDown(self):
        # Remove o arquivo de teste e arquivos gerados
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        translated_file = self.translator.get_translated_file_path(self.test_file)
        if os.path.exists(translated_file):
            os.remove(translated_file)
        # Remove o diretório do idioma se estiver vazio
        target_dir = os.path.dirname(self.translator.get_translated_file_path(self.test_file))
        if os.path.isdir(target_dir) and not os.listdir(target_dir):
            os.rmdir(target_dir)

    def test_translate_file(self):
        translated_content = self.translator.translate_file(self.test_file)
        self.assertIn("Olá, mundo!", translated_content)

    def test_save_translated_file(self):
        translated_content = "Olá, mundo!"
        translated_file_path = self.translator.get_translated_file_path(self.test_file)
        saved_file = self.translator.save_translated_file(translated_file_path, translated_content)
        self.assertTrue(os.path.exists(saved_file))

    def test_translate_directory(self):
        directory = os.path.abspath(os.path.dirname(self.test_file))
        self.translator.translate_directory(directory, overwrite_existing=True)
        translated_file = self.translator.get_translated_file_path(self.test_file)
        self.assertTrue(os.path.exists(translated_file))

if __name__ == '__main__':
    unittest.main()
