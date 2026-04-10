#!/usr/bin/env python3
"""
Extract Code Documentation Annotations

Scans source files for @doc:* annotations in docstrings and extracts structured metadata.
Outputs JSON file containing all extracted artifacts for downstream processing.

Usage:
    python extract_code_docs.py --source-dir <path> --output <file.json> [--lang python,javascript]
    python extract_code_docs.py --config config.json
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Artifact:
    """Represents a single documentation artifact"""
    artifact_id: str
    title: str
    chapter: str
    section: str
    description: str
    file_path: str
    line_number: int
    language: str
    doc_tags: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)


class DocstringParser:
    """Parses @doc:* annotations from docstrings"""
    
    @staticmethod
    def extract_docstring(text: str, language: str = "python") -> Optional[str]:
        """Extract docstring from source code based on language"""
        if language == "python":
            # Match triple-quoted strings
            match = re.search(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'', text, re.DOTALL)
            if match:
                return match.group(1) or match.group(2)
        elif language in ["javascript", "ts", "typescript"]:
            # Match /** */ comments
            match = re.search(r'/\*\*(.*?)\*/', text, re.DOTALL)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def parse_annotations(docstring: str) -> Dict[str, Any]:
        """Parse @doc:* annotations from docstring"""
        tags = {}
        lines = docstring.split('\n')
        
        for line in lines:
            # Match @doc:key: value or @doc:key value
            match = re.search(r'@doc:(\w+):\s*(.+?)(?=@doc:|$)', line, re.IGNORECASE)
            if match:
                key, value = match.group(1), match.group(2).strip()
                tags[key.lower()] = value
                continue
            
            # Match @doc:key followed by indented values (for lists)
            match = re.match(r'\s*@doc:(\w+):\s*(.+)', line, re.IGNORECASE)
            if match:
                key, value = match.group(1).lower(), match.group(2).strip()
                if key in tags and isinstance(tags[key], list):
                    tags[key].append(value)
                elif key in tags:
                    tags[key] = [tags[key], value]
                else:
                    tags[key] = value
        
        return tags
    
    @staticmethod
    def parse_structured_list(text: str, key: str) -> List[str]:
        """Parse structured list values like acceptance_criteria"""
        pattern = rf'@doc:{key}:(.*?)(?=@doc:|$)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            items = re.findall(r'-\s+(.+)', match.group(1))
            return items
        return []


class CodeScanner:
    """Scans source files for documentation artifacts"""
    
    LANGUAGE_EXTENSIONS = {
        'python': ['.py'],
        'javascript': ['.js'],
        'typescript': ['.ts'],
        'java': ['.java'],
        'csharp': ['.cs'],
        'cpp': ['.cpp', '.cc', '.h', '.hpp'],
        'go': ['.go'],
        'rust': ['.rs'],
    }
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize scanner with optional configuration"""
        self.config = config or {}
        self.languages = self.config.get('languages', ['python'])
        self.artifacts: List[Artifact] = []
        self.parser = DocstringParser()
    
    def get_extensions_for_languages(self) -> List[str]:
        """Get file extensions for configured languages"""
        extensions = []
        for lang in self.languages:
            extensions.extend(self.LANGUAGE_EXTENSIONS.get(lang, []))
        return extensions
    
    def scan_directory(self, source_dir: Path, recursive: bool = True) -> List[Artifact]:
        """Scan directory for source files and extract artifacts"""
        self.artifacts = []
        extensions = self.get_extensions_for_languages()
        
        pattern = '**/*' if recursive else '*'
        
        for ext in extensions:
            for file_path in source_dir.glob(f'{pattern}{ext}'):
                if file_path.is_file():
                    self._scan_file(file_path)
        
        return sorted(self.artifacts, key=lambda x: x.artifact_id)
    
    def _scan_file(self, file_path: Path) -> None:
        """Scan a single file for documentation artifacts"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, IOError) as e:
            print(f"Warning: Could not read {file_path}: {e}")
            return
        
        # Determine language from extension
        language = self._detect_language(file_path)
        
        # Extract all docstrings
        docstring_blocks = self._extract_all_docstrings(content, language)
        
        for line_num, docstring in docstring_blocks:
            tags = self.parser.parse_annotations(docstring)
            
            # Check if this docstring contains @doc: annotations
            if tags and 'artifact_id' in tags:
                artifact = self._create_artifact(
                    tags, file_path, line_num, language
                )
                if artifact:
                    self.artifacts.append(artifact)
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        ext = file_path.suffix.lower()
        for lang, exts in self.LANGUAGE_EXTENSIONS.items():
            if ext in exts:
                return lang
        return 'unknown'
    
    def _extract_all_docstrings(self, content: str, language: str) -> List[tuple]:
        """Extract all docstring blocks with line numbers"""
        docstrings = []
        lines = content.split('\n')
        
        if language == 'python':
            # Find triple-quoted strings
            pattern = r'"""(.*?)"""|\'\'\'(.*?)\'\'\''
            for match in re.finditer(pattern, content, re.DOTALL):
                line_num = content[:match.start()].count('\n') + 1
                docstring = match.group(1) or match.group(2)
                docstrings.append((line_num, docstring))
        
        elif language in ['javascript', 'typescript']:
            # Find /** */ comments
            pattern = r'/\*\*(.*?)\*/'
            for match in re.finditer(pattern, content, re.DOTALL):
                line_num = content[:match.start()].count('\n') + 1
                docstring = match.group(1)
                docstrings.append((line_num, docstring))
        
        elif language == 'java':
            # Find /** */ comments (same as JS/TS)
            pattern = r'/\*\*(.*?)\*/'
            for match in re.finditer(pattern, content, re.DOTALL):
                line_num = content[:match.start()].count('\n') + 1
                docstring = match.group(1)
                docstrings.append((line_num, docstring))
        
        return docstrings
    
    def _create_artifact(self, tags: Dict[str, Any], file_path: Path, 
                        line_num: int, language: str) -> Optional[Artifact]:
        """Create an Artifact object from parsed tags"""
        required_fields = ['artifact_id', 'chapter', 'section', 'title', 'description']
        
        # Check for required fields
        missing = [f for f in required_fields if f not in tags]
        if missing:
            print(f"Warning: {file_path}:{line_num} missing fields: {missing}")
            return None
        
        try:
            artifact = Artifact(
                artifact_id=tags['artifact_id'],
                title=tags['title'],
                chapter=tags['chapter'],
                section=tags['section'],
                description=tags['description'],
                file_path=str(file_path),
                line_number=line_num,
                language=language,
                doc_tags=tags
            )
            return artifact
        except (KeyError, ValueError) as e:
            print(f"Warning: Error creating artifact from {file_path}:{line_num}: {e}")
            return None


class AnnotationValidator:
    """Validates extracted artifacts against rules"""
    
    ARTIFACT_ID_PATTERNS = {
        'REQ': r'^REQ-\d{3}$',
        'USE-CASE': r'^USE-CASE-\d{3}$',
        'ARCH': r'^ARCH-\d{3}$',
        'SEQ': r'^SEQ-\d{3}$',
        'CLASS': r'^CLASS-\d{3}$',
        'CODE': r'^CODE-\d{3}$',
        'API': r'^API-\d{3}$',
        'CONFIG': r'^CONFIG-\d{3}$',
        'TC': r'^TC-\d{3}$',
        'TEST-SUITE': r'^TEST-SUITE-\d{3}$',
        'PERF': r'^PERF-\d{3}$',
        'METRIC': r'^METRIC-\d{3}$',
        'COVERAGE': r'^COVERAGE-\d{3}$',
    }
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_artifacts(self, artifacts: List[Artifact]) -> bool:
        """Validate a list of artifacts"""
        self.errors = []
        self.warnings = []
        
        # Check for duplicate IDs
        ids = [a.artifact_id for a in artifacts]
        duplicates = [id for id in ids if ids.count(id) > 1]
        if duplicates:
            self.errors.append(f"Duplicate artifact IDs found: {set(duplicates)}")
        
        # Validate each artifact
        for artifact in artifacts:
            self._validate_artifact_id(artifact.artifact_id)
            self._validate_description_length(artifact)
        
        return len(self.errors) == 0
    
    def _validate_artifact_id(self, artifact_id: str) -> None:
        """Validate artifact ID format"""
        prefix = artifact_id.split('-')[0]
        pattern = self.ARTIFACT_ID_PATTERNS.get(prefix)
        
        if not pattern:
            self.warnings.append(f"Unknown artifact ID prefix: {prefix}")
        elif not re.match(pattern, artifact_id):
            self.errors.append(f"Invalid artifact ID format: {artifact_id} (expected {pattern})")
    
    def _validate_description_length(self, artifact: Artifact) -> None:
        """Validate description length (should be 1-3 sentences)"""
        sentences = len(re.split(r'[.!?]+', artifact.description.strip()))
        if sentences > 4:
            self.warnings.append(
                f"{artifact.artifact_id}: Description too long ({sentences} sentences, expected 1-3)"
            )


def main():
    parser = argparse.ArgumentParser(
        description='Extract @doc:* annotations from source code'
    )
    parser.add_argument('--source-dir', type=Path, default=Path('./src'),
                       help='Source directory to scan (default: ./src)')
    parser.add_argument('--output', type=Path, default=Path('./docs/code_metadata.json'),
                       help='Output JSON file (default: ./docs/code_metadata.json)')
    parser.add_argument('--lang', type=str, default='python',
                       help='Languages to scan (comma-separated: python,javascript,java)')
    parser.add_argument('--recursive', action='store_true', default=True,
                       help='Recursively scan subdirectories (default: True)')
    parser.add_argument('--validate', action='store_true',
                       help='Validate annotations after extraction')
    parser.add_argument('--config', type=Path,
                       help='Configuration file (JSON)')
    
    args = parser.parse_args()
    
    # Load configuration
    config = {}
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
    else:
        config['languages'] = args.lang.split(',')
    
    # Scan directory
    print(f"Scanning {args.source_dir} for @doc:* annotations...")
    scanner = CodeScanner(config)
    artifacts = scanner.scan_directory(args.source_dir, args.recursive)
    
    print(f"Found {len(artifacts)} artifacts")
    
    # Validate if requested
    if args.validate:
        print("Validating artifacts...")
        validator = AnnotationValidator()
        validator.validate_artifacts(artifacts)
        
        if validator.errors:
            print(f"Errors ({len(validator.errors)}):")
            for error in validator.errors:
                print(f"  ✗ {error}")
        
        if validator.warnings:
            print(f"Warnings ({len(validator.warnings)}):")
            for warning in validator.warnings:
                print(f"  ⚠ {warning}")
    
    # Create output directory
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to JSON
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'source_dir': str(args.source_dir),
        'total_artifacts': len(artifacts),
        'artifacts': [a.to_dict() for a in artifacts]
    }
    
    with open(args.output, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"✓ Extracted metadata saved to {args.output}")


if __name__ == '__main__':
    main()
