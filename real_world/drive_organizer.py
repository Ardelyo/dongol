#!/usr/bin/env python3
"""
DONGOL Real-World Demo: Drive Organization
Uses parallel processing to analyze and reorganize a drive
"""
import asyncio
import os
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import DongolEngine, Chunk, Priority


class DriveAnalyzer:
    """Parallel drive analysis using DONGOL"""
    
    def __init__(self, engine: DongolEngine):
        self.engine = engine
        self.file_types = defaultdict(list)
        self.large_files = []
        self.old_files = []
        self.duplicates = defaultdict(list)
        self.total_size = 0
        self.file_count = 0
    
    async def analyze_directory(self, path: str, max_depth: int = 3) -> Dict:
        """Analyze a directory in parallel chunks"""
        print(f"Analyzing: {path}")
        
        # Collect all files first
        all_files = []
        for root, dirs, files in os.walk(path):
            depth = root.count(os.sep) - path.count(os.sep)
            if depth > max_depth:
                del dirs[:]
                continue
            
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    stat = os.stat(file_path)
                    all_files.append({
                        'path': file_path,
                        'size': stat.st_size,
                        'mtime': stat.st_mtime,
                        'name': file
                    })
                except (OSError, PermissionError):
                    continue
        
        print(f"  Found {len(all_files)} files")
        
        # Create chunks for parallel processing
        chunk_size = 50
        file_chunks = [
            all_files[i:i + chunk_size]
            for i in range(0, len(all_files), chunk_size)
        ]
        
        async def analyze_chunk(chunk: Chunk) -> Dict:
            """Process a batch of files"""
            files = chunk.content
            results = {
                'by_type': defaultdict(lambda: {'count': 0, 'size': 0}),
                'large_files': [],
                'old_files': [],
                'hashes': {}
            }
            
            for file_info in files:
                ext = Path(file_info['name']).suffix.lower() or 'no_extension'
                results['by_type'][ext]['count'] += 1
                results['by_type'][ext]['size'] += file_info['size']
                
                if file_info['size'] > 100 * 1024 * 1024:
                    results['large_files'].append({
                        'path': file_info['path'],
                        'size': file_info['size']
                    })
                
                age_days = (datetime.now().timestamp() - file_info['mtime']) / 86400
                if age_days > 365:
                    results['old_files'].append({
                        'path': file_info['path'],
                        'age_days': age_days
                    })
                
                try:
                    file_hash = f"{file_info['size']}"
                    if file_info['size'] < 1024 * 1024:
                        with open(file_info['path'], 'rb') as f:
                            file_hash += f.read(1024).hex()[:32]
                    results['hashes'][file_hash] = file_info['path']
                except:
                    pass
            
            return results
        
        self.engine.register_handler("analyze", analyze_chunk)
        
        task = await self.engine.create_task(
            name=f"Analyze {path}",
            content="batch_analysis",
            auto_chunk=False
        )
        
        task.chunks = [
            Chunk(content=chunk_files, tags={"file_analysis"})
            for chunk_files in file_chunks
        ]
        
        start_time = datetime.now()
        result = await self.engine.execute_task(task.id, "analyze")
        elapsed = (datetime.now() - start_time).total_seconds()
        
        merged = self._merge_analysis_results(result.results)
        merged['elapsed_seconds'] = elapsed
        merged['files_scanned'] = len(all_files)
        
        return merged
    
    def _merge_analysis_results(self, results: Dict) -> Dict:
        """Merge analysis results from all chunks"""
        merged = {
            'by_type': defaultdict(lambda: {'count': 0, 'size': 0}),
            'large_files': [],
            'old_files': [],
            'potential_duplicates': []
        }
        
        hash_map = defaultdict(list)
        
        for chunk_id, chunk_result in results.items():
            if not isinstance(chunk_result, dict):
                continue
            
            for ext, data in chunk_result.get('by_type', {}).items():
                merged['by_type'][ext]['count'] += data['count']
                merged['by_type'][ext]['size'] += data['size']
            
            merged['large_files'].extend(chunk_result.get('large_files', []))
            merged['old_files'].extend(chunk_result.get('old_files', []))
            
            for file_hash, path in chunk_result.get('hashes', {}).items():
                hash_map[file_hash].append(path)
        
        for file_hash, paths in hash_map.items():
            if len(paths) > 1:
                merged['potential_duplicates'].append(paths)
        
        merged['large_files'].sort(key=lambda x: x['size'], reverse=True)
        merged['large_files'] = merged['large_files'][:20]
        
        merged['old_files'].sort(key=lambda x: x['age_days'], reverse=True)
        merged['old_files'] = merged['old_files'][:20]
        
        return merged
    
    def generate_organization_plan(self, analysis: Dict) -> Dict:
        """Generate reorganization recommendations"""
        plan = {
            'new_structure': {},
            'recommendations': [],
            'space_savings': 0
        }
        
        type_mapping = {
            '.pdf': 'Documents/PDFs',
            '.doc': 'Documents/Word',
            '.docx': 'Documents/Word',
            '.txt': 'Documents/Text',
            '.jpg': 'Images/JPEG',
            '.jpeg': 'Images/JPEG',
            '.png': 'Images/PNG',
            '.mp4': 'Videos',
            '.avi': 'Videos',
            '.mkv': 'Videos',
            '.mp3': 'Audio',
            '.zip': 'Archives',
            '.rar': 'Archives',
            '.exe': 'Programs',
            '.py': 'Code/Python',
            '.js': 'Code/JavaScript',
            '.html': 'Code/Web',
        }
        
        for ext, data in analysis['by_type'].items():
            size_mb = data['size'] / (1024 * 1024)
            category = type_mapping.get(ext, f'Other/{ext.upper() if ext else "NoExtension"}')
            
            if category not in plan['new_structure']:
                plan['new_structure'][category] = {'count': 0, 'size_mb': 0}
            
            plan['new_structure'][category]['count'] += data['count']
            plan['new_structure'][category]['size_mb'] += size_mb
        
        if analysis['large_files']:
            total_large = sum(f['size'] for f in analysis['large_files'])
            plan['recommendations'].append(
                f"Found {len(analysis['large_files'])} large files (>100MB) totaling {total_large/(1024**3):.2f} GB"
            )
        
        if analysis['old_files']:
            plan['recommendations'].append(
                f"Found {len(analysis['old_files'])} files not accessed in >1 year"
            )
        
        return plan


async def main():
    """Main drive organization workflow"""
    print("=" * 70)
    print("DONGOL Drive Organizer - Parallel Analysis")
    print("=" * 70)
    
    engine = DongolEngine({'max_workers': 8})
    await engine.start()
    
    drives = [f"{d}:\\" for d in 'DEFGH' if os.path.exists(f"{d}:")]
    print(f"\nAvailable drives: {', '.join(drives)}")
    
    target_drive = "D:\\"
    if not os.path.exists(target_drive):
        print(f"Drive {target_drive} not found")
        return
    
    print(f"\nTarget: {target_drive}")
    print("Running in ANALYSIS MODE - no files will be moved or deleted\n")
    
    analyzer = DriveAnalyzer(engine)
    
    print("Starting parallel analysis...")
    analysis = await analyzer.analyze_directory(target_drive, max_depth=2)
    
    print(f"\nAnalysis complete in {analysis['elapsed_seconds']:.2f}s")
    print(f"Files scanned: {analysis['files_scanned']:,}")
    
    print("\n" + "=" * 70)
    print("FILE TYPE BREAKDOWN")
    print("=" * 70)
    
    sorted_types = sorted(
        analysis['by_type'].items(),
        key=lambda x: x[1]['size'],
        reverse=True
    )
    
    for ext, data in sorted_types[:15]:
        size_mb = data['size'] / (1024 * 1024)
        print(f"  {ext or '(no ext)':12} {data['count']:6,} files {size_mb:10.1f} MB")
    
    plan = analyzer.generate_organization_plan(analysis)
    
    print("\n" + "=" * 70)
    print("PROPOSED ORGANIZATION STRUCTURE")
    print("=" * 70)
    
    sorted_structure = sorted(
        plan['new_structure'].items(),
        key=lambda x: x[1]['size_mb'],
        reverse=True
    )
    
    for category, data in sorted_structure[:15]:
        print(f"  {category:30} {data['count']:6,} files {data['size_mb']:10.1f} MB")
    
    if plan['recommendations']:
        print("\n" + "=" * 70)
        print("RECOMMENDATIONS")
        print("=" * 70)
        for rec in plan['recommendations']:
            print(f"  * {rec}")
    
    if analysis['large_files']:
        print("\n" + "=" * 70)
        print("LARGEST FILES")
        print("=" * 70)
        for file_info in analysis['large_files'][:10]:
            size_gb = file_info['size'] / (1024**3)
            print(f"  {size_gb:6.2f} GB  {file_info['path'][:60]}")
    
    total_size_gb = sum(d['size'] for d in analysis['by_type'].values()) / (1024**3)
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total files:    {analysis['files_scanned']:,}")
    print(f"  Total size:     {total_size_gb:.2f} GB")
    print(f"  File types:     {len(analysis['by_type'])}")
    print(f"  Analysis time:  {analysis['elapsed_seconds']:.2f}s")
    print(f"  Throughput:     {analysis['files_scanned']/analysis['elapsed_seconds']:.0f} files/sec")
    
    await engine.stop()
    
    print("\n" + "=" * 70)
    print("DONGOL analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
