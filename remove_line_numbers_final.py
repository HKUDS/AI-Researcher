#!/usr/bin/env python3
"""
Final version: Comprehensively remove line numbers and page numbers while preserving legitimate numbers
"""

import re
import sys
import argparse
from pathlib import Path

def remove_line_numbers_final(text):
    """
    Comprehensively remove line numbers and page numbers while preserving legitimate numbers
    """
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip empty lines for efficiency
        if not line.strip():
            cleaned_lines.append(line)
            continue

        # If the line is a markdown header, handle it with specific logic
        if line.strip().startswith('#'):
            # Pattern 2 (Improved): Remove page numbers that might be embedded in markdown headers.
            # Handles both "# 217 6" and "# 142 4.1" style headers.
            pattern2 = r'^(#+\s+)(\d+)\s+([0-9\.]+\s+)'
            if re.match(pattern2, line):
                line = re.sub(pattern2, r'\1\3', line)
            cleaned_lines.append(line)
            continue

        # For all other lines, apply general line number removal patterns
        
        # Pattern 1 (New, more general): Remove line numbers at the beginning of any non-header line.
        # This is the most common case, e.g., "16 Robotic task..."
        pattern1 = r'^(\d+)\s+'
        line = re.sub(pattern1, '', line, count=1)
        
        # Pattern 3: Remove page numbers in the middle of text before math expressions
        # e.g., "metadomain, 198 $D" -> "metadomain, $D"
        pattern3 = r'(\w+),\s+(\d+)\s+(\$)'
        if re.search(pattern3, line):
            line = re.sub(pattern3, r'\1, \3', line)
        
        # Pattern 4: Remove standalone numbers before math expressions
        # e.g., "domain 198 $D" -> "domain $D"
        pattern4 = r'(\w+)\s+(\d+)\s+(\$[^$]*\$)'
        if re.search(pattern4, line):
            line = re.sub(pattern4, r'\1 \3', line)
        
        # Pattern 5 (New, more general): Remove numbers that appear between sentences
        # e.g., "end of sentence. 123 Next sentence." -> "end of sentence. Next sentence."
        pattern5 = r'(\.\s+)\d+\s+'
        line = re.sub(pattern5, r'\1', line)
        
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def process_file(input_file, output_file=None):
    """
    Process a single file to remove line numbers
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned_content = remove_line_numbers_final(content)
        
        # If no output file specified, overwrite the original
        if output_file is None:
            output_file = input_file
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"Processed: {input_file} -> {output_file}")
        
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Comprehensively remove line numbers from markdown files')
    parser.add_argument('input', help='Input markdown file or directory')
    parser.add_argument('-o', '--output', help='Output file (optional, defaults to overwrite input)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Process directory recursively')
    parser.add_argument('--backup', action='store_true', help='Create backup of original files')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without modifying files')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        if args.dry_run:
            # Show preview of changes
            content = input_path.read_text(encoding='utf-8')
            cleaned = remove_line_numbers_final(content)
            if content != cleaned:
                print("Changes would be made:")
                lines_orig = content.split('\n')
                lines_new = cleaned.split('\n')
                for i, (orig, new) in enumerate(zip(lines_orig, lines_new), 1):
                    if orig != new:
                        print(f"Line {i}:")
                        print(f"  OLD: {orig}")
                        print(f"  NEW: {new}")
            else:
                print("No changes needed.")
            return
        
        # Create backup if requested
        if args.backup:
            backup_path = input_path.with_suffix(input_path.suffix + '.backup')
            backup_path.write_text(input_path.read_text(encoding='utf-8'), encoding='utf-8')
            print(f"Backup created: {backup_path}")
        
        # Process single file
        output_file = args.output if args.output else None
        process_file(input_path, output_file)
    elif input_path.is_dir():
        # Process directory
        if args.recursive:
            md_files = list(input_path.rglob('*.md'))
        else:
            md_files = list(input_path.glob('*.md'))
        
        for md_file in md_files:
            if args.dry_run:
                print(f"Would process: {md_file}")
                continue
                
            # Create backup if requested
            if args.backup:
                backup_path = md_file.with_suffix(md_file.suffix + '.backup')
                backup_path.write_text(md_file.read_text(encoding='utf-8'), encoding='utf-8')
                print(f"Backup created: {backup_path}")
            
            if args.output:
                # Create output directory structure
                output_dir = Path(args.output)
                output_dir.mkdir(parents=True, exist_ok=True)
                relative_path = md_file.relative_to(input_path)
                output_file = output_dir / relative_path
                output_file.parent.mkdir(parents=True, exist_ok=True)
                process_file(md_file, output_file)
            else:
                # Overwrite original files
                process_file(md_file)
    else:
        print(f"Error: {input_path} is not a valid file or directory")
        sys.exit(1)

if __name__ == "__main__":
    main() 