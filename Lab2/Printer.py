import json
from enum import Enum
from typing import Dict, Tuple, List

class Color(Enum):
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RESET = '\033[0m'

class FontSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class Printer:
    _font_templates: Dict[str, Dict[str, List[str]]] = {}
    
    def __init__(self, color: Color, position: Tuple[int, int],
                 symbol: str = '*', font_size: FontSize = FontSize.MEDIUM):
        self.color = color
        self.position = position
        self.symbol = symbol
        self.font_size = font_size
    
    def __enter__(self):
        print('\033[s', end='')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(Color.RESET.value, end='')
        print('\033[u', end='', flush=True)
    
    @classmethod
    def load_font_templates(cls, filename: str = 'font_templates.json'):
        with open(filename, 'r', encoding='utf-8') as f:
            cls._font_templates = json.load(f)
    
    @staticmethod
    def _move_cursor(x: int, y: int):
        print(f'\033[{y};{x}H', end='')
    
    @classmethod
    def print(cls, text: str,
              color: Color,
              position: Tuple[int, int],
              symbol: str = '*',
              font_size: FontSize = FontSize.MEDIUM):
        text = text.upper()
        font_data = cls._font_templates[font_size.value]
        
        max_height = len(next(iter(font_data.values())))
        
        for row in range(max_height):
            cls._move_cursor(position[0], position[1] + row)
            print(color.value, end='')
            
            line = ''
            for char in text:
                if char in font_data:
                    template_line = font_data[char][row].replace('*', symbol)
                    line += template_line + ' '
                else:
                    line += ' ' * (max_height + 1)
            
            print(line, end='')
        
        print(Color.RESET.value, end='', flush=True)
    
    def print_text(self, text: str):
        self.__class__.print(text, self.color, self.position, self.symbol, self.font_size)

if __name__ == "__main__":
    Printer.load_font_templates()

    # Printer.print("HELLO world", Color.RED, (5, 3), '*', FontSize.SMALL)
    # Printer.print("Have a nice day", Color.YELLOW, (5, 8), '#')

    with Printer(Color.GREEN, (5, 5), '■', FontSize.LARGE) as printer:
        printer.print_text("Large text")