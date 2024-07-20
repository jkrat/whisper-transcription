import os
import time
import logging
from typing import Optional
from pathlib import Path
from .pattern_matching import match_file_type
from .transcription_service import transcribe_audio

class File_Watcher:

    def __init__(
            self, 
            patterns: list[str] = None, 
            logger: Optional[logging.Logger] = None
        ) -> None:

        self._patterns = patterns
        self.logger = logger or logging.root
        self.logger.info("File watcher initialized")
        self.wait_new_files(self.directory)

    @property
    def directory(self) -> Optional[str]:
        """
        (Read-only)
        Path to monitor for file changes.
        """
        return os.getenv('INCOMING_DIR', "/home/containeruser/src/incomingFiles")
    
    @property
    def new_base_path(self):
        """
        (Read-only)
        path to save transcribed files.
        """
        return os.getenv('NEXT_DIR', "/home/containeruser/src/nextFiles")
    
    @property
    def patterns(self):
        """
        (Read-only)
        Patterns to allow matching file paths.
        """
        return self._patterns
    
    def wait_new_files(self, directory: str) -> None: 
        previous_files = self.get_file_list(directory)
        while True:
            time.sleep(5)
            try:
                current_files = self.get_file_list(directory)
                new_files = list(set(current_files) - set(previous_files))
                for new_file in new_files:
                    file_path = Path(os.path.join(directory, new_file))
                    self.access_file(file_path)
                previous_files = current_files
            except Exception as e:
                self.logger.error(f"Error while monitoring directory: {e}")

    def get_file_list(self, directory: str) -> list[str]: 
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and match_file_type(f, included_patterns=self.patterns)]

    def access_file(self, file_path: Path) -> None:
        try:
            result = transcribe_audio(str(file_path)) 
        except Exception as e:
            self.logger.error(f"Error while transcribing file: {e}")  
            return
        try:
            new_file_path = self.get_new_file_path(file_path)
            self.write_file(new_file_path, result)
            self.delete_file(file_path)
        except Exception as e:
            # need to handle files that were written by not deleted, and how that is handled
            self.logger.error(f"Error while deleting file: {e}")
    
    def get_new_file_path(self, file_path: Path) -> str:
        path_without_extension = file_path.with_suffix('')
        file_name = path_without_extension.name
        return os.path.join(self.new_base_path, f"{file_name}.txt")
    
    def write_file(self, file_path: str, file_content: str) -> None:
        if not os.path.exists(file_path):
            with open(file_path, "x") as file:
                file.write(file_content)
                self.logger.info("file saved: %s", file_path)

    def delete_file(self, path: str) -> None:
        if os.path.exists(path):
            self.logger.info("file deleted: %s", path)
            os.remove(path)
        else:
            self.logger.info("path for deletion does not exist: %s", path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    File_Watcher(patterns=["*.wav"]) 
    