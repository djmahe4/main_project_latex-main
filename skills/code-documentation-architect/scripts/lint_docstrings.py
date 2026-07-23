#!/usr/bin/env python3
"""
Lint Docstrings - Enforce Documentation Standards

Validates that all source files follow the @doc:* annotation protocol.
Checks for missing required fields, malformed IDs, and documentation consistency.

Usage:
    python lint_docstrings.py --source-dir src/ --check-all
    python lint_docstrings.py --phase requirements --strict
    python lint_docstrings.py --fix-mode  # Auto-fix common issues
"""

import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class SeverityLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class LintIssue:
    """Represents a linting issue"""
    file: str
    line: int
    severity: SeverityLevel
    code: str
    message: str
    suggestion: Optional[str] = None


class DocstringLinter:
    """Lints docstring annotations for compliance"""
    
    REQUIRED_FIELDS = {
        'artifact_id', 'chapter', 'section', 'title', 'description'
    }
    
    OPTIONAL_FIELDS = {
        'subsection', 'tags', 'priority', 'last_updated', 'author',
        'related_artifacts', 'diagram_type', 'language', 'key_functions',
        'algorithm_complexity', 'class_description', 'public_methods',
        'method_description', 'output', 'requirement', 'acceptance_criteria',
        'test_name', 'test_case_id', 'preconditions', 'steps', 'expected_result',
        'pass_criteria', 'metric_id', 'metric_name', 'value', 'unit',
        'threshold', 'status'
    }
    
    ARTIFACT_ID_PREFIXES = {
        'REQ', 'USE-CASE', 'ARCH', 'SEQ', 'CLASS', 'CODE', 'API',
        'CONFIG', 'TC', 'TEST-SUITE', 'PERF', 'METRIC', 'COVERAGE'
    }
    
    PRIORITY_VALUES = {'HIGH', 'MEDIUM', 'LOW'}
    
    def __init__(self, strict_mode: bool = False):
        self.issues: List[LintIssue] = []
        self.strict_mode = strict_mode
    
    def lint_file(self, file_path: Path) -> List[LintIssue]:
        """Lint a single file for documentation issues"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except (UnicodeDecodeError, IOError) as e:
            return [LintIssue(
                file=str(file_path),
                line=0,
                severity=SeverityLevel.ERROR,
                code='FILE_READ_ERROR',
                message=f"Could not read file: {e}"
            )]
        
        # Extract docstrings and check each
        docstring_matches = self._extract_docstrings(content)
        
        for line_num, docstring in docstring_matches:
            docstring_issues = self._lint_docstring(docstring, str(file_path), line_num)
            issues.extend(docstring_issues)
        
        return issues
    
    def _extract_docstrings(self, content: str) -> List[Tuple[int, str]]:
        """Extract all docstring blocks with line numbers"""
        docstrings = []
        
        # Python docstrings
        pattern = r'"""(.*?)"""|\'\'\'(.*?)\'\'\''
        for match in re.finditer(pattern, content, re.DOTALL):
            line_num = content[:match.start()].count('\n') + 1
            docstring = match.group(1) or match.group(2)
            if '@doc:' in docstring:
                docstrings.append((line_num, docstring))
        
        # Multi-line comments (JS/Java style)
        pattern = r'/\*\*(.*?)\*/'
        for match in re.finditer(pattern, content, re.DOTALL):
            line_num = content[:match.start()].count('\n') + 1
            docstring = match.group(1)
            if '@doc:' in docstring:
                docstrings.append((line_num, docstring))
        
        return docstrings
    
    def _lint_docstring(self, docstring: str, file_path: str, 
                       line_num: int) -> List[LintIssue]:
        """Lint a single docstring"""
        issues = []
        
        # Parse annotations
        fields = self._parse_fields(docstring)
        
        # Check for required fields
        missing = self.REQUIRED_FIELDS - set(fields.keys())
        for field in missing:
            issues.append(LintIssue(
                file=file_path,
                line=line_num,
                severity=SeverityLevel.ERROR,
                code='MISSING_FIELD',
                message=f"Missing required field: @doc:{field}",
                suggestion=f"Add @doc:{field}: <value>"
            ))
        
        # Check field values
        if 'artifact_id' in fields:
            issues.extend(self._validate_artifact_id(
                fields['artifact_id'], file_path, line_num
            ))
        
        if 'priority' in fields:
            if fields['priority'] not in self.PRIORITY_VALUES:
                issues.append(LintIssue(
                    file=file_path,
                    line=line_num,
                    severity=SeverityLevel.WARNING,
                    code='INVALID_PRIORITY',
                    message=f"Invalid priority value: {fields['priority']}",
                    suggestion=f"Use one of: {', '.join(self.PRIORITY_VALUES)}"
                ))
        
        if 'description' in fields:
            description = fields['description']
            sentence_count = len(re.split(r'[.!?]+', description.strip())) - 1
            
            if sentence_count > 3:
                issues.append(LintIssue(
                    file=file_path,
                    line=line_num,
                    severity=SeverityLevel.WARNING,
                    code='DESCRIPTION_TOO_LONG',
                    message=f"Description has {sentence_count} sentences (expected <= 3)",
                    suggestion="Condense the description to 1-3 sentences"
                ))
            
            if sentence_count == 0:
                issues.append(LintIssue(
                    file=file_path,
                    line=line_num,
                    severity=SeverityLevel.WARNING,
                    code='EMPTY_DESCRIPTION',
                    message="Description appears to be empty or missing periods",
                ))
        
        # Check for unknown fields (in strict mode)
        if self.strict_mode:
            all_valid = self.REQUIRED_FIELDS | self.OPTIONAL_FIELDS
            unknown = set(fields.keys()) - all_valid
            for field in unknown:
                issues.append(LintIssue(
                    file=file_path,
                    line=line_num,
                    severity=SeverityLevel.INFO,
                    code='UNKNOWN_FIELD',
                    message=f"Unknown field: @doc:{field}",
                    suggestion="Remove or add to OPTIONAL_FIELDS"
                ))
        
        return issues
    
    def _parse_fields(self, docstring: str) -> Dict[str, str]:
        """Parse @doc:* fields from docstring"""
        fields = {}
        lines = docstring.split('\n')
        
        for line in lines:
            match = re.match(r'\s*@doc:(\w+):\s*(.+)', line, re.IGNORECASE)
            if match:
                key = match.group(1).lower()
                value = match.group(2).strip()
                fields[key] = value
        
        return fields
    
    def _validate_artifact_id(self, artifact_id: str, file_path: str, 
                             line_num: int) -> List[LintIssue]:
        """Validate artifact ID format"""
        issues = []
        
        # Check prefix
        prefix = artifact_id.split('-')[0] if '-' in artifact_id else artifact_id
        if prefix not in self.ARTIFACT_ID_PREFIXES:
            issues.append(LintIssue(
                file=file_path,
                line=line_num,
                severity=SeverityLevel.WARNING,
                code='UNKNOWN_PREFIX',
                message=f"Unknown prefix: {prefix}",
                suggestion=f"Use one of: {', '.join(sorted(self.ARTIFACT_ID_PREFIXES))}"
            ))
        else:
            # Check ID format (should be PREFIX-NNN)
            pattern = rf'^{re.escape(prefix)}-\d{{3}}$'
            if not re.match(pattern, artifact_id):
                issues.append(LintIssue(
                    file=file_path,
                    line=line_num,
                    severity=SeverityLevel.ERROR,
                    code='INVALID_ID_FORMAT',
                    message=f"Invalid ID format: {artifact_id}",
                    suggestion=f"Use format: {prefix}-NNN (e.g., {prefix}-001)"
                ))
        
        return issues


class AnnotationEnforcer:
    """Enforces annotation standards across codebase"""
    
    def __init__(self, source_dir: Path):
        self.source_dir = source_dir
        self.linter = DocstringLinter()
        self.all_issues: List[LintIssue] = []
    
    def lint_directory(self, recursive: bool = True, 
                      extensions: List[str] = None) -> List[LintIssue]:
        """Lint all source files in directory"""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.java', '.go', '.rs']
        
        pattern = '**/*' if recursive else '*'
        
        for ext in extensions:
            for file_path in self.source_dir.glob(f'{pattern}{ext}'):
                if file_path.is_file():
                    issues = self.linter.lint_file(file_path)
                    self.all_issues.extend(issues)
        
        return sorted(self.all_issues, key=lambda x: (x.file, x.line))
    
    def get_summary(self) -> Dict[str, int]:
        """Get summary statistics"""
        return {
            'total_issues': len(self.all_issues),
            'errors': len([i for i in self.all_issues if i.severity == SeverityLevel.ERROR]),
            'warnings': len([i for i in self.all_issues if i.severity == SeverityLevel.WARNING]),
            'info': len([i for i in self.all_issues if i.severity == SeverityLevel.INFO]),
        }
    
    def print_report(self, max_issues: int = None):
        """Print linting report"""
        summary = self.get_summary()
        
        print(f"\nLinting Report:")
        print(f"  Total issues: {summary['total_issues']}")
        print(f"  Errors: {summary['errors']}")
        print(f"  Warnings: {summary['warnings']}")
        print(f"  Info: {summary['info']}")
        
        if self.all_issues:
            print(f"\nDetails:")
            for i, issue in enumerate(self.all_issues[:max_issues or len(self.all_issues)]):
                severity_symbol = {'error': '✗', 'warning': '⚠', 'info': 'ℹ'}[issue.severity.value]
                print(f"\n  {severity_symbol} [{issue.severity.value.upper()}] {issue.code}")
                print(f"     File: {issue.file}:{issue.line}")
                print(f"     Message: {issue.message}")
                if issue.suggestion:
                    print(f"     Suggestion: {issue.suggestion}")
            
            if max_issues and len(self.all_issues) > max_issues:
                print(f"\n  ... and {len(self.all_issues) - max_issues} more issues")


def main():
    parser = argparse.ArgumentParser(
        description='Lint docstring annotations for compliance'
    )
    parser.add_argument('--source-dir', type=Path, default=Path('./src'),
                       help='Source directory to scan')
    parser.add_argument('--check-all', action='store_true',
                       help='Check all docstrings (not just @doc: annotations)')
    parser.add_argument('--strict', action='store_true',
                       help='Enable strict mode (fail on unknown fields)')
    parser.add_argument('--phase', type=str,
                       help='Filter by phase (requirements, design, implementation, testing)')
    parser.add_argument('--file', type=Path,
                       help='Lint a single file')
    parser.add_argument('--max-issues', type=int,
                       help='Maximum issues to display')
    parser.add_argument('--json', type=Path,
                       help='Output results as JSON')
    
    args = parser.parse_args()
    
    if args.file:
        # Lint single file
        linter = DocstringLinter(strict_mode=args.strict)
        issues = linter.lint_file(args.file)
    else:
        # Lint directory
        enforcer = AnnotationEnforcer(args.source_dir)
        issues = enforcer.lint_directory()
    
    # Print report
    if args.file:
        for issue in issues:
            print(f"{issue.severity.value.upper()}: {issue.message}")
    else:
        print(f"\nScanned: {args.source_dir}")
        print(f"Total issues found: {len(issues)}")
        
        for issue in issues[:args.max_issues or 20]:
            severity_symbol = {'error': '✗', 'warning': '⚠', 'info': 'ℹ'}[issue.severity.value]
            print(f"\n{severity_symbol} {issue.file}:{issue.line}")
            print(f"   {issue.code}: {issue.message}")
            if issue.suggestion:
                print(f"   → {issue.suggestion}")
    
    # Save JSON report
    if args.json:
        report = {
            'total_issues': len(issues),
            'issues': [
                {
                    'file': issue.file,
                    'line': issue.line,
                    'severity': issue.severity.value,
                    'code': issue.code,
                    'message': issue.message,
                    'suggestion': issue.suggestion
                }
                for issue in issues
            ]
        }
        
        with open(args.json, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Report saved to {args.json}")


if __name__ == '__main__':
    main()
