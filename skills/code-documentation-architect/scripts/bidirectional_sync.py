#!/usr/bin/env python3
"""
Bidirectional Sync - Full Documentation Sync Pipeline

Orchestrates the complete extraction, validation, and synchronization workflow.
Runs all scripts in sequence to maintain code-documentation consistency.

Usage:
    python bidirectional_sync.py --full-sync
    python bidirectional_sync.py --extract --validate --generate
"""

import subprocess
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class SyncPipeline:
    """Orchestrates the full sync pipeline"""
    
    def __init__(self, config_file: Optional[Path] = None):
        """Initialize pipeline with optional config file"""
        self.config: Dict = {}
        self.results: Dict = {}
        self.errors: List[str] = []
        
        if config_file and config_file.exists():
            with open(config_file) as f:
                self.config = json.load(f)
        
        # Set defaults
        self.config.setdefault('source_dir', './src')
        self.config.setdefault('latex_dir', './Chapters')
        self.config.setdefault('output_dir', './docs')
        self.config.setdefault('media_dir', './media')
        self.config.setdefault('languages', ['python'])
    
    def extract(self) -> bool:
        """Step 1: Extract code documentation annotations"""
        print("\n" + "="*60)
        print("STEP 1: Extracting Code Documentation")
        print("="*60)
        
        cmd = [
            'python', 'extract_code_docs.py',
            '--source-dir', self.config['source_dir'],
            '--output', f"{self.config['output_dir']}/code_metadata.json",
            '--lang', ','.join(self.config['languages']),
            '--validate'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
            self.results['extract'] = {'status': 'OK', 'output': result.stdout}
            return True
        except subprocess.CalledProcessError as e:
            error = f"Extraction failed: {e.stderr}"
            print(f"✗ {error}")
            self.errors.append(error)
            return False
    
    def lint(self) -> bool:
        """Step 2: Lint all docstrings for compliance"""
        print("\n" + "="*60)
        print("STEP 2: Linting Documentation Standards")
        print("="*60)
        
        cmd = [
            'python', 'lint_docstrings.py',
            '--source-dir', self.config['source_dir'],
            '--json', f"{self.config['output_dir']}/lint_report.json"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            print(result.stdout)
            self.results['lint'] = {'status': 'OK', 'output': result.stdout}
            
            # Check for errors in lint report
            lint_report_file = Path(self.config['output_dir']) / 'lint_report.json'
            if lint_report_file.exists():
                with open(lint_report_file) as f:
                    lint_data = json.load(f)
                    if lint_data.get('total_issues', 0) > 0:
                        print(f"⚠ Found {lint_data['total_issues']} linting issues")
            
            return True
        except Exception as e:
            error = f"Linting failed: {e}"
            print(f"✗ {error}")
            self.errors.append(error)
            return False
    
    def validate(self) -> bool:
        """Step 3: Validate code-to-docs mappings"""
        print("\n" + "="*60)
        print("STEP 3: Validating Code-Documentation Mappings")
        print("="*60)
        
        cmd = [
            'python', 'validate_mappings.py',
            '--metadata', f"{self.config['output_dir']}/code_metadata.json",
            '--latex-dir', self.config['latex_dir'],
            '--output', f"{self.config['output_dir']}/validation_report.json"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            print(result.stdout)
            self.results['validate'] = {'status': 'OK', 'output': result.stdout}
            return True
        except Exception as e:
            error = f"Validation failed: {e}"
            print(f"✗ {error}")
            self.errors.append(error)
            return False
    
    def generate_tables(self) -> bool:
        """Step 4: Generate LaTeX tables from artifacts"""
        print("\n" + "="*60)
        print("STEP 4: Generating LaTeX Tables")
        print("="*60)
        
        output_tables = Path(self.config['media_dir']) / 'tables'
        
        cmd = [
            'python', 'generate_tables.py',
            '--metadata', f"{self.config['output_dir']}/code_metadata.json",
            '--output-dir', str(output_tables),
            '--single-file'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            print(result.stdout)
            self.results['generate'] = {'status': 'OK', 'output': result.stdout}
            return True
        except Exception as e:
            error = f"Table generation failed: {e}"
            print(f"✗ {error}")
            self.errors.append(error)
            return False
    
    def coverage(self) -> bool:
        """Step 5: Analyze documentation coverage"""
        print("\n" + "="*60)
        print("STEP 5: Analyzing Documentation Coverage")
        print("="*60)
        
        cmd = [
            'python', 'coverage_report.py',
            '--metadata', f"{self.config['output_dir']}/code_metadata.json",
            '--output', f"{self.config['output_dir']}/coverage_report.json",
            '--by-chapter',
            '--by-type'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            print(result.stdout)
            self.results['coverage'] = {'status': 'OK', 'output': result.stdout}
            return True
        except Exception as e:
            error = f"Coverage analysis failed: {e}"
            print(f"✗ {error}")
            self.errors.append(error)
            return False
    
    def run_full_sync(self) -> bool:
        """Run complete sync pipeline"""
        print("\n")
        print("╔" + "="*58 + "╗")
        print("║" + " "*58 + "║")
        print("║     BIDIRECTIONAL DOCUMENTATION SYNC PIPELINE" + " "*12 + "║")
        print("║" + " "*58 + "║")
        print("╚" + "="*58 + "╝")
        
        steps = [
            ('Extract', self.extract),
            ('Lint', self.lint),
            ('Validate', self.validate),
            ('Generate', self.generate_tables),
            ('Coverage', self.coverage),
        ]
        
        passed = 0
        failed = 0
        
        for step_name, step_func in steps:
            if step_func():
                passed += 1
            else:
                failed += 1
        
        # Print summary
        print("\n" + "="*60)
        print("SYNC PIPELINE SUMMARY")
        print("="*60)
        print(f"Completed: {passed} steps")
        print(f"Failed: {failed} steps")
        
        if self.errors:
            print(f"\nErrors:")
            for error in self.errors:
                print(f"  ✗ {error}")
        
        # Save results
        results_file = Path(self.config['output_dir']) / 'sync_results.json'
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'passed': passed,
                'failed': failed,
                'errors': self.errors,
                'results': self.results
            }, f, indent=2)
        
        print(f"\n✓ Results saved to {results_file}")
        
        return failed == 0
    
    def run_extract_only(self) -> bool:
        """Run only extraction step"""
        return self.extract()
    
    def run_validate_only(self) -> bool:
        """Run only validation step"""
        return self.validate()
    
    def run_quick_check(self) -> bool:
        """Run quick validation without full sync"""
        print("\n" + "="*60)
        print("QUICK VALIDATION CHECK")
        print("="*60)
        
        return self.extract() and self.validate()


def main():
    parser = argparse.ArgumentParser(
        description='Orchestrate documentation sync pipeline'
    )
    parser.add_argument('--full-sync', action='store_true',
                       help='Run complete sync pipeline (all steps)')
    parser.add_argument('--extract', action='store_true',
                       help='Run extraction only')
    parser.add_argument('--lint', action='store_true',
                       help='Run linting only')
    parser.add_argument('--validate', action='store_true',
                       help='Run validation only')
    parser.add_argument('--generate', action='store_true',
                       help='Run table generation only')
    parser.add_argument('--coverage', action='store_true',
                       help='Run coverage analysis only')
    parser.add_argument('--quick-check', action='store_true',
                       help='Quick check (extract + validate)')
    parser.add_argument('--config', type=Path,
                       help='Configuration file (JSON)')
    parser.add_argument('--source-dir', type=Path,
                       help='Source directory')
    parser.add_argument('--latex-dir', type=Path,
                       help='LaTeX chapters directory')
    parser.add_argument('--output-dir', type=Path,
                       help='Output directory for reports')
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        pipeline = SyncPipeline(args.config)
    else:
        pipeline = SyncPipeline()
    
    # Override config from command line
    if args.source_dir:
        pipeline.config['source_dir'] = str(args.source_dir)
    if args.latex_dir:
        pipeline.config['latex_dir'] = str(args.latex_dir)
    if args.output_dir:
        pipeline.config['output_dir'] = str(args.output_dir)
    
    # Create output directory
    Path(pipeline.config['output_dir']).mkdir(parents=True, exist_ok=True)
    
    # Run requested steps
    if args.full_sync:
        success = pipeline.run_full_sync()
    elif args.extract and args.validate and args.generate:
        success = pipeline.extract() and pipeline.validate() and pipeline.generate_tables()
    elif args.extract:
        success = pipeline.extract()
    elif args.lint:
        success = pipeline.lint()
    elif args.validate:
        success = pipeline.validate()
    elif args.generate:
        success = pipeline.generate_tables()
    elif args.coverage:
        success = pipeline.coverage()
    elif args.quick_check:
        success = pipeline.run_quick_check()
    else:
        print("No action specified. Use --help for options.")
        print("Suggested: --full-sync for complete pipeline")
        success = True
    
    exit(0 if success else 1)


if __name__ == '__main__':
    main()
