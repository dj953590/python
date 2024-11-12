from abc import ABC, abstractmethod
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from typing import List

class BaseTextSplitter(ABC):
    @abstractmethod
    def split_text(self, text: str) -> List[str]:
        """
        Abstract method to split text into chunks.
        """
        pass

class SimpleTextSplitter(BaseTextSplitter):
    def __init__(self, separator: str = " ", max_chunk_size: int = 1000):
        self.separator = separator
        self.max_chunk_size = max_chunk_size

    def split_text(self, text: str) -> List[str]:
        chunks = []
        current_chunk = []
        current_chunk_size = 0

        for word in text.split(self.separator):
            if current_chunk_size + len(word) + len(self.separator) > self.max_chunk_size:
                chunks.append(self.separator.join(current_chunk))
                current_chunk = [word]
                current_chunk_size = len(word)
            else:
                current_chunk.append(word)
                current_chunk_size += len(word) + len(self.separator)

        if current_chunk:
            chunks.append(self.separator.join(current_chunk))

        return chunks

class LangChainRecursiveCharacterTextSplitter(BaseTextSplitter):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def split_text(self, text: str) -> List[str]:
        return self.splitter.split_text(text)

class LangChainCharacterTextSplitter(BaseTextSplitter):
    def __init__(self, chunk_size: int = 1000):
        self.splitter = CharacterTextSplitter(chunk_size=chunk_size)

    def split_text(self, text: str) -> List[str]:
        return self.splitter.split_text(text)

class TextSplitterFactory:
    @staticmethod
    def get_splitter(splitter_type: str, **kwargs) -> BaseTextSplitter:
        if splitter_type == "simple":
            return SimpleTextSplitter(**kwargs)
        elif splitter_type == "recursive_character":
            return LangChainRecursiveCharacterTextSplitter(**kwargs)
        elif splitter_type == "character":
            return LangChainCharacterTextSplitter(**kwargs)
        else:
            raise ValueError(f"Unknown splitter type: {splitter_type}")

# Example usage:
text = "Your text data that needs to be split."

# Using SimpleTextSplitter
splitter = TextSplitterFactory.get_splitter("simple", separator=" ", max_chunk_size=50)
chunks = splitter.split_text(text)
print("SimpleTextSplitter chunks:", chunks)

# Using LangChain RecursiveCharacterTextSplitter
splitter = TextSplitterFactory.get_splitter("recursive_character", chunk_size=50, chunk_overlap=10)
chunks = splitter.split_text(text)
print("LangChainRecursiveCharacterTextSplitter chunks:", chunks)

# Using LangChain CharacterTextSplitter
splitter = TextSplitterFactory.get_splitter("character", chunk_size=50)
chunks = splitter.split_text(text)
print("LangChainCharacterTextSplitter chunks:", chunks)




