from typing import TypeVar, Generic, List
from abc import ABC, abstractmethod

# ============== ПОЛИМОРФНЫЙ ВЫЗОВ ==============

class File(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def open(self) -> str:
        pass
    
    @abstractmethod
    def get_size(self) -> str:
        pass

class TextFile(File):
    def open(self) -> str:
        return f"Открываю текстовый файл {self.name} в блокноте"
    
    def get_size(self) -> str:
        return f"{self.name}: 15 KB"

class ImageFile(File):
    def open(self) -> str:
        return f"Открываю изображение {self.name} в просмотрщике"
    
    def get_size(self) -> str:
        return f"{self.name}: 2.5 MB"

class VideoFile(File):
    def open(self) -> str:
        return f"Открываю видео {self.name} в плеере"
    
    def get_size(self) -> str:
        return f"{self.name}: 150 MB"

# Полиморфная функция - работает с любым типом файла
def process_files(files):
    for file in files:
        # ПОЛИМОРФНЫЙ ВЫЗОВ - один синтаксис, разная реализация
        print(file.open())      # Полиморфный вызов
        print(file.get_size())  # Полиморфный вызов
        print("-" * 30)

# ============== КОВАРИАНТНЫЙ ВЫЗОВ ==============

T = TypeVar('T', bound=File)

class FileStorage(Generic[T]):
    def __init__(self):
        self.files: List[T] = []
    
    def add_file(self, file: T):
        """КОВАРИАНТНЫЙ МЕТОД - тип T определяется при создании"""
        self.files.append(file)
    
    def get_files(self) -> List[T]:
        """КОВАРИАНТНЫЙ ВОЗВРАТ - возвращает List[T]"""
        return self.files
    
    def count_files(self) -> int:
        """КОВАРИАНТНЫЙ МЕТОД - работает с типом T"""
        return len(self.files)

# ============== ДЕМОНСТРАЦИЯ ==============

def main():
    print("=== ПОЛИМОРФНЫЙ ВЫЗОВ ===")
    
    # Создаем файлы разных типов
    files = [
        TextFile("документ.txt"),
        ImageFile("фото.jpg"), 
        VideoFile("фильм.mp4")
    ]
    
    # Полиморфная обработка - один код для всех типов
    process_files(files)
    
    print("\n=== КОВАРИАНТНЫЙ ВЫЗОВ ===")
    
    # Создаем хранилища для конкретных типов файлов
    text_storage = FileStorage[TextFile]()    # T = TextFile
    image_storage = FileStorage[ImageFile]()  # T = ImageFile
    
    # КОВАРИАНТНЫЕ ВЫЗОВЫ - добавление файлов
    text_storage.add_file(TextFile("статья.txt"))     # T = TextFile
    text_storage.add_file(TextFile("заметки.txt"))    # T = TextFile
    
    image_storage.add_file(ImageFile("картинка1.png")) # T = ImageFile
    image_storage.add_file(ImageFile("картинка2.jpg")) # T = ImageFile
    
    # КОВАРИАНТНЫЕ ВЫЗОВЫ - получение файлов
    texts: List[TextFile] = text_storage.get_files()    # Возвращает List[TextFile]
    images: List[ImageFile] = image_storage.get_files() # Возвращает List[ImageFile]
    
    print(f"Текстовых файлов: {text_storage.count_files()}")  # КОВАРИАНТНЫЙ ВЫЗОВ
    print(f"Файлов изображений: {image_storage.count_files()}") # КОВАРИАНТНЫЙ ВЫЗОВ
    
    print("\nТекстовые файлы:")
    for text in texts:
        print(f"- {text.name}")
    
    print("\nФайлы изображений:")
    for image in images:
        print(f"- {image.name}")

if __name__ == "__main__":
    main()
