from pathlib import Path
from typing import List

class FindValuableFiles:
    def __init__(self, items: List[Path]):
        self.items = items

    def find_files(self) -> List[Path]:
        return [item for item in self.items if item.is_file() and "password" in item.name]

    def run(self):
        valuable_files = self.find_files()
        print(f"🔑 Valuable files found: {valuable_files}")


if __name__ == "__main__":
    FindValuableFiles().run()