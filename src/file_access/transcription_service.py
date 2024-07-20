import os
import whisper
import logging

def transcribe_audio(file: str, model_name: str = 'tiny.pt') -> str:
    # Set the model directory from the environment variable
    model_dir = os.getenv('WHISPER_MODEL_DIR', '/root/.cache/whisper')
    model_path = os.path.join(model_dir, model_name)
    logging.info(f"Loading file {file}")

    # Load the model from the specified directory
    try:
        model = whisper.load_model(model_path, device='cpu')
    except Exception as e:
        logging.error(f"Error while loading model: {e}")
    # model = whisper.load_model(model_path, device='cpu')
    # model = whisper.load_model("medium", device='cpu')
    try:
        result = model.transcribe(file)
    except Exception as e:
        logging.error(f"Error transcribing model: {e}")
    return result['text']