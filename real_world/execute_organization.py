#!/usr/bin/env python3
"""
DONGOL Safe File Organizer
Actually reorganizes files in parallel (safe directories only)
"""
import asyncio
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import DongolEngine, Chunk


# Safe directories to organize (user folders only)
SAFE_DIRECTORIES = [
    'download',
    'downloads', 
    'pictures',
    'documents',
    'doxcs',
    'coding',
    'Archive',
]

# File type to folder mapping
ORGANIZATION_RULES = {
    # Images
    '.jpg': 'Organized/Images/JPEG',
    '.jpeg': 'Organized/Images/JPEG',
    '.png': 'Organized/Images/PNG',
    '.gif': 'Organized/Images/GIF',
    '.webp': 'Organized/Images/WebP',
    '.bmp': 'Organized/Images/BMP',
    
    # Documents
    '.pdf': 'Organized/Documents/PDFs',
    '.doc': 'Organized/Documents/Word',
    '.docx': 'Organized/Documents/Word',
    '.txt': 'Organized/Documents/Text',
    '.md': 'Organized/Documents/Markdown',
    '.rtf': 'Organized/Documents/RichText',
    
    # Videos
    '.mp4': 'Organized/Videos/MP4',
    '.avi': 'Organized/Videos/AVI',
    '.mkv': 'Organized/Videos/MKV',
    '.mov': 'Organized/Videos/MOV',
    '.wmv': 'Organized/Videos/WMV',
    
    # Audio
    '.mp3': 'Organized/Audio/MP3',
    '.wav': 'Organized/Audio/WAV',
    '.flac': 'Organized/Audio/FLAC',
    '.aac': 'Organized/Audio/AAC',
    '.ogg': 'Organized/Audio/OGG',
    
    # Archives
    '.zip': 'Organized/Archives/ZIP',
    '.rar': 'Organized/Archives/RAR',
    '.7z': 'Organized/Archives/7Z',
    '.tar': 'Organized/Archives/TAR',
    '.gz': 'Organized/Archives/GZ',
    
    # Code
    '.py': 'Organized/Code/Python',
    '.js': 'Organized/Code/JavaScript',
    '.ts': 'Organized/Code/TypeScript',
    '.html': 'Organized/Code/HTML',
    '.css': 'Organized/Code/CSS',
    '.json': 'Organized/Code/JSON',
    '.xml': 'Organized/Code/XML',
    '.yaml': 'Organized/Code/YAML',
    '.yml': 'Organized/Code/YAML',
    
    # Data
    '.csv': 'Organized/Data/CSV',
    '.xlsx': 'Organized/Data/Excel',
    '.xls': 'Organized/Data/Excel',
    '.db': 'Organized/Data/Database',
    '.sql': 'Organized/Data/SQL',
    
    # Executables
    '.exe': 'Organized/Programs/EXE',
    '.msi': 'Organized/Programs/MSI',
    '.bat': 'Organized/Programs/Scripts',
    '.ps1': 'Organized/Programs/Scripts',
}


class SafeFileOrganizer:
    """Safely organize files using DONGOL parallel processing"""
    
    def __init__(self, engine: DongolEngine, base_path: str, dry_run: bool = True):
        self.engine = engine
        self.base_path = Path(base_path)
        self.dry_run = dry_run
        self.stats = {
            'files_moved': 0,
            'files_skipped': 0,
            'errors': 0,
            'bytes_moved': 0
        }
        self.created_folders = set()
    
    async def organize_directory(self, target_dir: str) -> Dict:
        """Organize files in a specific directory"""
        target_path = self.base_path / target_dir
        
        if not target_path.exists():
            print(f"Directory not found: {target_path}")
            return self.stats
        
        print(f"\n{'[DRY-RUN] ' if self.dry_run else ''}Organizing: {target_path}")
        
        # Collect files to organize
        files_to_organize = []
        for file_path in target_path.rglob('*'):
            if file_path.is_file():
                # Skip if already in an Organized folder
                if 'Organized' in str(file_path):
                    continue
                # Skip system files
                if file_path.name.startswith('.') or file_path.name.startswith('~'):
                    continue
                files_to_organize.append(file_path)
        
        print(f"  Found {len(files_to_organize)} files to organize")
        
        if not files_to_organize:
            return self.stats
        
        # Create chunks for parallel processing
        chunk_size = 20
        file_chunks = [
            files_to_organize[i:i + chunk_size]
            for i in range(0, len(files_to_organize), chunk_size)
        ]
        
        async def organize_chunk(chunk: Chunk) -> Dict:
            """Organize a batch of files"""
            files = chunk.content
            results = {
                'moved': 0,
                'skipped': 0,
                'errors': 0,
                'bytes_moved': 0,
                'operations': []
            }
            
            for file_path in files:
                try:
                    ext = file_path.suffix.lower()
                    target_folder = ORGANIZATION_RULES.get(ext)
                    
                    if not target_folder:
                        results['skipped'] += 1
                        continue
                    
                    # Determine destination
                    dest_dir = self.base_path / target_folder / target_dir
                    dest_path = dest_dir / file_path.name
                    
                    # Handle duplicates
                    counter = 1
                    original_dest = dest_path
                    while dest_path.exists():
                        stem = original_dest.stem
                        suffix = original_dest.suffix
                        dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    file_size = file_path.stat().st_size
                    
                    if self.dry_run:
                        results['operations'].append({
                            'action': 'MOVE',
                            'from': str(file_path),
                            'to': str(dest_path),
                            'size': file_size
                        })
                        results['moved'] += 1
                        results['bytes_moved'] += file_size
                    else:
                        # Actually move the file
                        dest_dir.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(file_path), str(dest_path))
                        results['moved'] += 1
                        results['bytes_moved'] += file_size
                        
                except Exception as e:
                    results['errors'] += 1
                    results['operations'].append({
                        'action': 'ERROR',
                        'file': str(file_path),
                        'error': str(e)
                    })
            
            return results
        
        self.engine.register_handler("organize", organize_chunk)
        
        # Create task
        task = await self.engine.create_task(
            name=f"Organize {target_dir}",
            content="organization",
            auto_chunk=False
        )
        
        task.chunks = [
            Chunk(content=chunk_files, tags={"file_organization"})
            for chunk_files in file_chunks
        ]
        
        # Execute parallel organization
        start_time = datetime.now()
        result = await self.engine.execute_task(task.id, "organize")
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # Merge results
        for chunk_result in result.results.values():
            if isinstance(chunk_result, dict):
                self.stats['files_moved'] += chunk_result.get('moved', 0)
                self.stats['files_skipped'] += chunk_result.get('skipped', 0)
                self.stats['errors'] += chunk_result.get('errors', 0)
                self.stats['bytes_moved'] += chunk_result.get('bytes_moved', 0)
        
        print(f"  Completed in {elapsed:.2f}s")
        print(f"  Files to move: {self.stats['files_moved']}")
        print(f"  Files skipped: {self.stats['files_skipped']}")
        print(f"  Errors: {self.stats['errors']}")
        
        return self.stats
    
    def generate_report(self) -> str:
        """Generate organization report"""
        report = []
        report.append("\n" + "=" * 70)
        report.append("ORGANIZATION REPORT")
        report.append("=" * 70)
        report.append(f"Mode: {'DRY-RUN (no changes made)' if self.dry_run else 'LIVE (files moved)'}")
        report.append(f"Files to be moved: {self.stats['files_moved']}")
        report.append(f"Files skipped: {self.stats['files_skipped']}")
        report.append(f"Errors: {self.stats['errors']}")
        report.append(f"Total size: {self.stats['bytes_moved'] / (1024**2):.2f} MB")
        report.append("=" * 70)
        return "\n".join(report)


async def main():
    """Main organization workflow"""
    print("=" * 70)
    print("DONGOL Safe File Organizer")
    print("=" * 70)
    print("\n⚠️  This will organize files in safe directories only")
    print("   System files and folders will be ignored\n")
    
    # Ask for confirmation
    print("Available safe directories:")
    for d in SAFE_DIRECTORIES:
        print(f"  - {d}")
    
    response = input("\nRun in DRY-RUN mode first? (recommended) [Y/n]: ").strip().lower()
    dry_run = response in ('', 'y', 'yes')
    
    # Initialize engine
    engine = DongolEngine({'max_workers': 4})
    await engine.start()
    
    target_drive = "D:\\"
    organizer = SafeFileOrganizer(engine, target_drive, dry_run=dry_run)
    
    total_stats = {
        'files_moved': 0,
        'files_skipped': 0,
        'errors': 0,
        'bytes_moved': 0
    }
    
    # Process each safe directory
    for directory in SAFE_DIRECTORIES:
        stats = await organizer.organize_directory(directory)
        for key in total_stats:
            total_stats[key] += stats.get(key, 0)
    
    # Update final stats
    organizer.stats = total_stats
    
    # Print report
    print(organizer.generate_report())
    
    # If dry run, ask if they want to execute
    if dry_run and total_stats['files_moved'] > 0:
        print("\n⚠️  This was a dry-run. No files were actually moved.")
        execute = input("Do you want to execute these changes for real? [y/N]: ").strip().lower()
        
        if execute in ('y', 'yes'):
            print("\n🚀 Executing real organization...")
            organizer_real = SafeFileOrganizer(engine, target_drive, dry_run=False)
            
            for directory in SAFE_DIRECTORIES:
                await organizer_real.organize_directory(directory)
            
            print(organizer_real.generate_report())
            print("\n✅ Organization complete!")
        else:
            print("\n❌ Cancelled. No changes made.")
    
    await engine.stop()


if __name__ == "__main__":
    # Auto-confirm for demo (dry-run only)
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--auto':
        print("=" * 70)
        print("DONGOL Safe File Organizer (AUTO MODE - DRY RUN)")
        print("=" * 70)
        
        async def auto_run():
            engine = DongolEngine({'max_workers': 4})
            await engine.start()
            
            target_drive = "D:\\"
            organizer = SafeFileOrganizer(engine, target_drive, dry_run=True)
            
            for directory in SAFE_DIRECTORIES[:3]:  # Just first 3 for demo
                await organizer.organize_directory(directory)
            
            print(organizer.generate_report())
            await engine.stop()
        
        asyncio.run(auto_run())
    else:
        asyncio.run(main())
