"""Config"""
import json
from log import error
class Config:
    """Translator config."""
    def __init__(self, filename=None):
        self.data = {
            "class": {
                "return_at_the_end": False,
            },
            "luau": None,
        }

        if filename is not None:
            self.load(filename)

    def load(self, filename):
        """Load config from the file"""
        try:
            with open(filename, "r") as stream:
                data = json.load(stream)
                self.data.update(data)
        except FileNotFoundError:
            pass # Use a default config if the file not found
        except json.decoder.JSONDecodeError:
            error("Config file is not a valid JSON file.")

    def __getitem__(self, key):
        """Get data values"""
        return self.data[key]
