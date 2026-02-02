#!/usr/bin/env python3
"""
DONGOL Performance Comparison: Sequential vs Parallel
Real-world file processing benchmark
"""
import asyncio
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import DongolEngine, Chunk


def simulate_file_processing(file_path: str) -> Dict:
    """Simulate processing a file (classification)"""
    ext = Path(file_path).suffix.lower()
    size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    
    # Simulate work (1ms per MB)
    time.sleep(size / (1024**2) * 0.001)
    
    return {
        'file': file_path,
        'type': ext,
        'size': size,
        'processed': True
    }


async def sequential_processing(files: List[str]) -> Dict:
    """Process files sequentially"""
    print("\n[SEQUENTIAL MODE]")
    print("Processing files one by one...")
    
    start = time.perf_counter()
    results = []
    
    for i, file_path in enumerate(files, 1):
        result = simulate_file_processing(file_path)
        results.append(result)
        
        if i % 100 == 0:
            print(f"  Processed {i}/{len(files)} files...")
    
    elapsed = time.perf_counter() - start
    
    total_size = sum(r['size'] for r in results)
    
    return {
        'mode': 'sequential',
        'files_processed': len(results),
        'total_size_mb': total_size / (1024**2),
        'elapsed_seconds': elapsed,
        'throughput_files_sec': len(results) / elapsed,
        'throughput_mb_sec': (total_size / (1024**2)) / elapsed
    }


async def parallel_processing(files: List[str], workers: int = 8) -> Dict:
    """Process files using DONGOL parallel engine"""
    print(f"\n[DONGOL PARALLEL MODE - {workers} workers]")
    print("Processing files in parallel chunks...")
    
    engine = DongolEngine({'max_workers': workers})
    await engine.start()
    
    def process_chunk(chunk: Chunk) -> Dict:
        """Process a batch of files"""
        batch = chunk.content
        results = []
        
        for file_path in batch:
            result = simulate_file_processing(file_path)
            results.append(result)
        
        return {
            'results': results,
            'count': len(results),
            'total_size': sum(r['size'] for r in results)
        }
    
    engine.register_handler("process", process_chunk)
    
    # Create chunks (50 files per chunk)
    chunk_size = 50
    file_chunks = [
        files[i:i + chunk_size]
        for i in range(0, len(files), chunk_size)
    ]
    
    task = await engine.create_task(
        name="Parallel File Processing",
        content="processing",
        auto_chunk=False
    )
    
    task.chunks = [
        Chunk(content=chunk_files, tags={"file_batch"})
        for chunk_files in file_chunks
    ]
    
    start = time.perf_counter()
    result = await engine.execute_task(task.id, "process")
    elapsed = time.perf_counter() - start
    
    # Merge results
    total_files = 0
    total_size = 0
    for chunk_result in result.results.values():
        if isinstance(chunk_result, dict):
            total_files += chunk_result.get('count', 0)
            total_size += chunk_result.get('total_size', 0)
    
    await engine.stop()
    
    return {
        'mode': f'parallel ({workers} workers)',
        'files_processed': total_files,
        'total_size_mb': total_size / (1024**2),
        'elapsed_seconds': elapsed,
        'throughput_files_sec': total_files / elapsed,
        'throughput_mb_sec': (total_size / (1024**2)) / elapsed
    }


async def main():
    """Compare sequential vs parallel processing"""
    print("=" * 70)
    print("DONGOL Performance Comparison: Sequential vs Parallel")
    print("=" * 70)
    
    # Collect real files from D drive
    target_dirs = ['D:\\download', 'D:\\pictures']
    files = []
    
    print("\nCollecting files...")
    for target_dir in target_dirs:
        if os.path.exists(target_dir):
            for root, _, filenames in os.walk(target_dir):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
                    if len(files) >= 500:  # Limit to 500 for demo
                        break
                if len(files) >= 500:
                    break
    
    if len(files) < 100:
        print("Not enough files found. Using synthetic benchmark.")
        # Create synthetic file list
        files = [f"D:\\test\\file_{i}.txt" for i in range(200)]
    
    print(f"Total files to process: {len(files)}")
    
    # Sequential processing
    seq_result = await sequential_processing(files)
    
    # Wait a bit between tests
    await asyncio.sleep(1)
    
    # Parallel processing
    par_result = await parallel_processing(files, workers=8)
    
    # Results comparison
    print("\n" + "=" * 70)
    print("RESULTS COMPARISON")
    print("=" * 70)
    
    print(f"\n{'Metric':<30} {'Sequential':>15} {'Parallel':>15} {'Speedup':>10}")
    print("-" * 70)
    
    print(f"{'Files processed':<30} {seq_result['files_processed']:>15,} {par_result['files_processed']:>15,} {'1.0x':>10}")
    
    print(f"{'Total size (MB)':<30} {seq_result['total_size_mb']:>15.1f} {par_result['total_size_mb']:>15.1f} {'1.0x':>10}")
    
    print(f"{'Time (seconds)':<30} {seq_result['elapsed_seconds']:>15.2f} {par_result['elapsed_seconds']:>15.2f} "
          f"{seq_result['elapsed_seconds']/par_result['elapsed_seconds']:>9.1f}x")
    
    print(f"{'Throughput (files/sec)':<30} {seq_result['throughput_files_sec']:>15.1f} {par_result['throughput_files_sec']:>15.1f} "
          f"{par_result['throughput_files_sec']/seq_result['throughput_files_sec']:>9.1f}x")
    
    print(f"{'Throughput (MB/sec)':<30} {seq_result['throughput_mb_sec']:>15.1f} {par_result['throughput_mb_sec']:>15.1f} "
          f"{par_result['throughput_mb_sec']/seq_result['throughput_mb_sec']:>9.1f}x")
    
    # Summary
    speedup = seq_result['elapsed_seconds'] / par_result['elapsed_seconds']
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"DONGOL parallel processing is {speedup:.1f}x faster than sequential!")
    print(f"Time saved: {seq_result['elapsed_seconds'] - par_result['elapsed_seconds']:.2f} seconds")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
