import aiofiles
from pathlib import Path
from typing import Dict
from pypdf import PdfReader
from loguru import logger
from pydantic import BaseModel, Field

# SOTA Data Structure for Documents
class ParsedDocument(BaseModel):
    filename: str
    content: str
    metadata: Dict[str, str] = Field(default_factory=dict)
    char_count: int

class RequirementParser:
    """
    Async Parser for Requirement Documents (PDF/TXT/MD).
    Implements secure file handling and metadata extraction.
    """

    SUPPORTED_EXTENSIONS = {'.pdf', '.txt', '.md'}

    @staticmethod
    def _validate_path(file_path: str) -> Path:
        path = Path(file_path)
        if not path.exists():
            logger.error(f"File not found: {path}")
            raise FileNotFoundError(f"File not found: {path}")
        if path.suffix.lower() not in RequirementParser.SUPPORTED_EXTENSIONS:
            logger.error(f"Unsupported file type: {path.suffix}")
            raise ValueError(f"Unsupported file type. Allowed: {RequirementParser.SUPPORTED_EXTENSIONS}")
        return path

    @staticmethod
    async def parse(file_path: str) -> ParsedDocument:
        """
        Asynchronously parses a file and returns a structured Document object.
        """
        path = RequirementParser._validate_path(file_path)
        logger.info(f"Parsing file: {path.name}")

        try:
            if path.suffix.lower() == '.pdf':
                return await RequirementParser._parse_pdf(path)
            else:
                return await RequirementParser._parse_text(path)
        except Exception as e:
            logger.exception(f"Failed to parse {path.name}")
            raise RuntimeError(f"Parsing failed: {str(e)}")

    @staticmethod
    async def _parse_text(path: Path) -> ParsedDocument:
        async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
            content = await f.read()
        
        return ParsedDocument(
            filename=path.name,
            content=content,
            metadata={"type": "text/markdown"},
            char_count=len(content)
        )

    @staticmethod
    async def _parse_pdf(path: Path) -> ParsedDocument:
        try:
            reader = PdfReader(str(path))
            text = []
            for page in reader.pages:
                text.append(page.extract_text() or "")
            
            full_text = "\n".join(text)
            
            return ParsedDocument(
                filename=path.name,
                content=full_text,
                metadata={"pages": str(len(reader.pages))},
                char_count=len(full_text)
            )
        except Exception as e:
            raise ValueError(f"Corrupt or unreadable PDF: {str(e)}")
