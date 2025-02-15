"""
Script para transcrever o áudio de um vídeo e gerar um arquivo de legenda (SRT ou VTT)
utilizando o modelo Whisper da OpenAI.

Requisitos:
    - Python 3.x
    - openai-whisper (pip install openai-whisper)
    - FFmpeg instalado (necessário para processar o áudio/vídeo)

Uso:
    python gerar_legenda.py caminho/do/video.mp4 --format srt
    python gerar_legenda.py caminho/do/video.mp4 --format vtt

Se o parâmetro --output não for informado, o script usará o nome do vídeo com a extensão adequada.
Você também pode especificar qual modelo do Whisper utilizar via --model (ex: tiny, base, small, medium, large).
"""

import argparse
import os
import sys
import logging
from typing import List, Dict, Any
import whisper

# Configuração básica do logging para exibir mensagens informativas
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def format_timestamp(seconds: float, fmt: str = "srt") -> str:
    """
    Converte um tempo (em segundos) para o formato de legenda.

    Args:
        seconds (float): Tempo em segundos.
        fmt (str): Formato desejado ("srt" ou "vtt"). Padrão: "srt".

    Returns:
        str: Tempo formatado:
            - SRT: "HH:MM:SS,mmm"
            - VTT: "HH:MM:SS.mmm"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    # Calcula os milissegundos
    msecs = int(round((seconds - int(seconds)) * 1000))
    
    if fmt.lower() == "srt":
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{msecs:03d}"
    else:  # formato VTT
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{msecs:03d}"

def write_srt(segments: List[Dict[str, Any]], output_file: str) -> None:
    """
    Gera um arquivo de legenda no formato SRT a partir dos segmentos transcritos.

    Args:
        segments (list): Lista de segmentos com chaves "start", "end" e "text".
        output_file (str): Caminho para o arquivo de saída.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        for index, segment in enumerate(segments, start=1):
            start_time = format_timestamp(segment["start"], fmt="srt")
            end_time = format_timestamp(segment["end"], fmt="srt")
            text = segment["text"].strip()
            # Escreve o número do segmento, os tempos e o texto da legenda
            f.write(f"{index}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def write_vtt(segments: List[Dict[str, Any]], output_file: str) -> None:
    """
    Gera um arquivo de legenda no formato VTT a partir dos segmentos transcritos.

    Args:
        segments (list): Lista de segmentos com chaves "start", "end" e "text".
        output_file (str): Caminho para o arquivo de saída.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        # Cabeçalho obrigatório para arquivos VTT
        f.write("WEBVTT\n\n")
        for segment in segments:
            start_time = format_timestamp(segment["start"], fmt="vtt")
            end_time = format_timestamp(segment["end"], fmt="vtt")
            text = segment["text"].strip()
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def transcribe_video(video_path: str, model_name: str = "base") -> List[Dict[str, Any]]:
    """
    Realiza a transcrição do vídeo utilizando o modelo Whisper.

    Args:
        video_path (str): Caminho para o arquivo de vídeo.
        model_name (str): Nome do modelo Whisper a ser utilizado. Padrão: "base".

    Returns:
        list: Lista de segmentos transcritos contendo "start", "end" e "text".
    """
    logging.info("Carregando o modelo Whisper '%s'...", model_name)
    model = whisper.load_model(model_name)

    logging.info("Iniciando a transcrição do vídeo: %s", video_path)
    result = model.transcribe(video_path)
    
    segments = result.get("segments", [])
    if not segments:
        logging.warning("Nenhum segmento de áudio foi identificado no vídeo.")
    return segments

def parse_arguments() -> argparse.Namespace:
    """
    Configura e retorna os argumentos de linha de comando.

    Returns:
        argparse.Namespace: Objeto contendo os argumentos.
    """
    parser = argparse.ArgumentParser(
        description="Transcreve um vídeo e gera um arquivo de legenda (SRT ou VTT) utilizando o modelo Whisper."
    )
    parser.add_argument("video", help="Caminho para o arquivo de vídeo")
    parser.add_argument(
        "--format",
        choices=["srt", "vtt"],
        default="srt",
        help="Formato da legenda (padrão: srt)"
    )
    parser.add_argument(
        "--output",
        help="Caminho do arquivo de saída. Se não especificado, será usado o nome do vídeo com a extensão apropriada."
    )
    parser.add_argument(
        "--model",
        default="base",
        help="Nome do modelo Whisper a ser utilizado (ex: tiny, base, small, medium, large). Padrão: base"
    )
    return parser.parse_args()

def main():
    """
    Função principal que processa os argumentos, realiza a transcrição do vídeo
    e gera o arquivo de legenda no formato especificado.
    """
    args = parse_arguments()

    video_path = args.video
    output_format = args.format.lower()
    model_name = args.model

    # Verifica se o arquivo de vídeo existe
    if not os.path.exists(video_path):
        logging.error("O arquivo de vídeo '%s' não foi encontrado.", video_path)
        sys.exit(1)

    # Define o caminho do arquivo de saída
    if args.output:
        output_path = args.output
    else:
        base_name, _ = os.path.splitext(video_path)
        output_path = f"{base_name}.{output_format}"

    try:
        # Realiza a transcrição do vídeo
        segments = transcribe_video(video_path, model_name=model_name)
        if not segments:
            logging.error("Nenhum segmento de transcrição foi gerado. Verifique o vídeo ou o modelo utilizado.")
            sys.exit(1)
    except Exception as e:
        logging.error("Erro durante a transcrição: %s", e)
        sys.exit(1)

    try:
        # Gera o arquivo de legenda com base no formato escolhido
        if output_format == "srt":
            write_srt(segments, output_path)
        elif output_format == "vtt":
            write_vtt(segments, output_path)
        else:
            logging.error("Formato de legenda não suportado: %s", output_format)
            sys.exit(1)
    except Exception as e:
        logging.error("Erro ao gerar o arquivo de legenda: %s", e)
        sys.exit(1)

    logging.info("Legenda gerada com sucesso: %s", output_path)

if __name__ == "__main__":
    main()
