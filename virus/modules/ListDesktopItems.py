from pathlib import Path
import os
from typing import List

class ListDesktopItems:
    def __init__(self):
        self.desktop_path = Path(os.path.expanduser("~/Desktop"))

    def list_items(self) -> List[Path]:
        if self.desktop_path.is_dir():
            return [item for item in self.desktop_path.iterdir()]
        else:
            raise Exception("Invalid Path provided")

    def run(self):
        items = self.list_items()
        print(f"📂 Found {len(items)} items on desktop: {items}")


if __name__ == "__main__":
    ListDesktopItems().run()