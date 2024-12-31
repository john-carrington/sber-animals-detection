import os
from dataclasses import dataclass


@dataclass
class PageDescription:
    pass


root_dir: str = os.path.dirname(os.path.abspath(__file__))
markdown_files: list[str] = os.listdir(root_dir)

for file in markdown_files:
    if file.endswith('.md'):
        content = open(os.path.join(root_dir, file)).read()
        setattr(PageDescription, os.path.splitext(file)[0], content)
