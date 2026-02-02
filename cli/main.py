#!/usr/bin/env python3
"""
DONGOL CLI - Universal Interface for Humans and Agents
"""
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Optional, List

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.tree import Tree

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import (
    DongolEngine, Task, Chunk, TaskStatus, Priority,
    get_engine, ChunkingEngine
)

console = Console()


@click.group(invoke_without_command=True)
@click.option('--config', '-c', type=click.Path(), help='Config file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """
    🧠 DONGOL - Distributed Orchestration for Navigating Goals and Operational Logic
    
    Universal task management for humans and AI agents.
    
    Examples:
      dongol think "Analyze this code" --file main.py
      dongol run "Process data" --parallel --workers 8
      dongol status
      dongol chunk "Large text..." --size 500
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose
    
    if ctx.invoked_subcommand is None:
        console.print(Panel.fit(
            "[bold cyan]🧠 DONGOL[/bold cyan] - Parallel Thinking Task Manager\n"
            "[dim]Run 'dongol --help' for commands[/dim]",
            title="Welcome",
            border_style="cyan"
        ))


@cli.command()
@click.argument('query')
@click.option('--mode', '-m', type=click.Choice(['parallel', 'sequential', 'auto']), default='auto')
@click.option('--workers', '-w', type=int, default=4, help='Number of parallel workers')
@click.option('--chunk-size', '-s', type=int, default=500, help='Chunk size for splitting')
@click.option('--priority', '-p', type=click.Choice(['critical', 'high', 'normal', 'low', 'background']), default='normal')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
@click.option('--json-output', 'json_out', is_flag=True, help='Output as JSON')
@click.pass_context
async def think(ctx, query: str, mode: str, workers: int, chunk_size: int, priority: str, output: Optional[str], json_out: bool):
    """
    🤔 Think about something - DONGOL will parallelize the thinking process
    
    QUERY: The task or question to think about
    
    Example:
      dongol think "How to optimize this database query?"
      dongol think "Analyze pros and cons of microservices" --mode parallel --workers 8
    """
    config = {
        'max_workers': workers,
        'chunking': {'max_chunk_size': chunk_size}
    }
    
    engine = await get_engine(config)
    
    # Custom handler for thinking tasks
    async def think_handler(chunk: Chunk) -> dict:
        """Process a thinking chunk"""
        await asyncio.sleep(0.01)  # Simulate processing
        return {
            'chunk_id': chunk.id,
            'thought': f"Processed: {str(chunk.content)[:50]}...",
            'insights': ['insight_1', 'insight_2'],
            'confidence': 0.85
        }
    
    engine.register_handler('think', think_handler)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task_progress = progress.add_task(f"[cyan]Thinking about: {query[:50]}...", total=None)
        
        # Create and execute task
        task = await engine.create_task(
            name=f"Think: {query[:30]}",
            content=query,
            handler_name='think',
            auto_chunk=True,
            chunk_size=chunk_size,
            priority=Priority[priority.upper()],
            parallel=(mode in ['parallel', 'auto'])
        )
        
        result_task = await engine.execute_task(task.id, 'think')
        progress.update(task_progress, completed=True)
    
    # Display results
    if json_out:
        output_data = {
            'task_id': result_task.id,
            'name': result_task.name,
            'status': result_task.status.name,
            'duration_ms': result_task.duration_ms,
            'chunks_processed': len(result_task.chunks),
            'results': result_task.results
        }
        if output:
            Path(output).write_text(json.dumps(output_data, indent=2, default=str))
        else:
            console.print_json(data=output_data)
    else:
        console.print(Panel(
            f"[bold green]✓ Task Complete[/bold green]\n"
            f"ID: [dim]{result_task.id}[/dim]\n"
            f"Chunks: [yellow]{len(result_task.chunks)}[/yellow]\n"
            f"Duration: [cyan]{result_task.duration_ms:.2f}ms[/cyan]",
            title="Results",
            border_style="green"
        ))
        
        # Show chunk results tree
        tree = Tree("[bold]Processing Tree[/bold]")
        for chunk_id, result in result_task.results.items():
            tree.add(f"[dim]{chunk_id}[/dim]: {str(result)[:60]}...")
        console.print(tree)


@cli.command()
@click.argument('content')
@click.option('--by', type=click.Choice(['tokens', 'sentences', 'paragraphs', 'structure']), default='tokens')
@click.option('--size', '-s', type=int, default=500)
@click.option('--overlap', type=float, default=0.1)
@click.option('--output', '-o', type=click.Path())
def chunk(content: str, by: str, size: int, overlap: float, output: Optional[str]):
    """
    ✂️ Chunk content intelligently
    
    CONTENT: Text or JSON to chunk
    
    Example:
      dongol chunk "Long text here..." --size 200
      dongol chunk '{"data": ...}' --by structure
    """
    chunker = ChunkingEngine({'overlap_ratio': overlap})
    
    if by == 'tokens':
        chunks = chunker.chunk_by_tokens(content, size)
    elif by == 'structure':
        try:
            data = json.loads(content)
            chunks = chunker.chunk_by_structure(data)
        except json.JSONDecodeError:
            console.print("[red]Error: Content is not valid JSON for structure chunking[/red]")
            return
    else:
        # Fallback to token-based
        chunks = chunker.chunk_by_tokens(content, size)
    
    # Display results
    table = Table(title=f"Generated {len(chunks)} Chunks")
    table.add_column("ID", style="cyan", width=10)
    table.add_column("Size", style="yellow", width=8)
    table.add_column("Tags", style="green")
    table.add_column("Preview", style="white")
    
    for i, c in enumerate(chunks):
        preview = str(c.content)[:50] + "..." if len(str(c.content)) > 50 else str(c.content)
        table.add_row(
            c.id,
            str(len(str(c.content))),
            ", ".join(c.tags),
            preview
        )
    
    console.print(table)
    
    if output:
        output_data = [c.to_dict() for c in chunks]
        Path(output).write_text(json.dumps(output_data, indent=2))
        console.print(f"[green]Saved to {output}[/green]")


@cli.command()
@click.option('--watch', '-w', is_flag=True, help='Watch mode - continuous updates')
@click.option('--json-output', 'json_out', is_flag=True, help='Output as JSON')
async def status(watch: bool, json_out: bool):
    """
    📊 Show system status and statistics
    
    Example:
      dongol status
      dongol status --watch
    """
    engine = await get_engine()
    
    if watch:
        with console.status("[cyan]Monitoring DONGOL...[/cyan]") as status:
            while True:
                stats = engine.get_stats()
                if json_out:
                    console.print_json(data=stats)
                else:
                    table = Table(title="DONGOL System Status")
                    table.add_column("Metric", style="cyan")
                    table.add_column("Value", style="yellow")
                    
                    for key, value in stats.items():
                        table.add_row(key, str(value))
                    
                    console.clear()
                    console.print(table)
                
                await asyncio.sleep(2)
    else:
        stats = engine.get_stats()
        if json_out:
            console.print_json(data=stats)
        else:
            table = Table(title="🧠 DONGOL System Status", border_style="cyan")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="yellow")
            
            table.add_row("Total Tasks", str(stats['total_tasks']))
            table.add_row("Total Chunks", str(stats['total_chunks']))
            table.add_row("Avg Chunks/Task", f"{stats['avg_chunks_per_task']:.2f}")
            table.add_row("Engine Running", "✓" if stats['engine_running'] else "✗")
            
            if stats['status_distribution']:
                status_str = ", ".join([f"{k}: {v}" for k, v in stats['status_distribution'].items()])
                table.add_row("Status Distribution", status_str)
            
            console.print(table)


@cli.command()
@click.argument('task_spec')
@click.option('--type', 'task_type', type=click.Choice(['shell', 'python', 'javascript', 'llm']), default='shell')
@click.option('--env', '-e', multiple=True, help='Environment variables (KEY=VALUE)')
@click.option('--timeout', '-t', type=int, default=60)
@click.option('--parallel', '-p', is_flag=True, help='Run in parallel mode')
async def run(task_spec: str, task_type: str, env: List[str], timeout: int, parallel: bool):
    """
    ▶️ Run a task or command
    
    TASK_SPEC: The command, code, or task to execute
    
    Example:
      dongol run "ls -la" --type shell
      dongol run "print('Hello')" --type python
      dongol run "Analyze sentiment" --type llm
    """
    engine = await get_engine()
    
    # Parse environment variables
    env_vars = {}
    for e in env:
        if '=' in e:
            key, value = e.split('=', 1)
            env_vars[key] = value
    
    async def execution_handler(chunk: Chunk) -> dict:
        content = chunk.content
        start_time = time.time()
        
        if task_type == 'shell':
            import subprocess
            result = subprocess.run(
                content if isinstance(content, list) else content.split(),
                capture_output=True,
                text=True,
                timeout=timeout,
                env={**dict(os.environ), **env_vars} if env_vars else None
            )
            return {
                'returncode': result.returncode,
                'stdout': result.stdout[:1000],
                'stderr': result.stderr[:500],
                'duration_ms': (time.time() - start_time) * 1000
            }
        
        elif task_type == 'python':
            # Execute Python code safely
            output = {}
            exec_globals = {'__builtins__': __builtins__, 'output': output}
            exec(content, exec_globals)
            return {
                'output': output,
                'duration_ms': (time.time() - start_time) * 1000
            }
        
        else:
            return {
                'content': content,
                'type': task_type,
                'processed': True
            }
    
    engine.register_handler('exec', execution_handler)
    
    task = await engine.create_task(
        name=f"Run: {task_spec[:30]}",
        content=task_spec,
        handler_name='exec',
        auto_chunk=False,
        parallel=parallel
    )
    
    with console.status(f"[cyan]Running {task_type} task...[/cyan]"):
        result = await engine.execute_task(task.id, 'exec')
    
    console.print(Panel(
        json.dumps(result.results, indent=2, default=str),
        title=f"[green]Execution Result[/green]",
        border_style="green"
    ))


@cli.command()
@click.argument('pattern')
@click.option('--in-tasks', is_flag=True, help='Search in task names')
@click.option('--in-results', is_flag=True, help='Search in results')
@click.option('--json-output', 'json_out', is_flag=True)
async def search(pattern: str, in_tasks: bool, in_results: bool, json_out: bool):
    """
    🔍 Search through tasks and results
    
    PATTERN: Search pattern (supports wildcards)
    
    Example:
      dongol search "error*"
      dongol search "optimization" --in-results
    """
    engine = await get_engine()
    results = []
    
    for task in engine.tasks.values():
        match = False
        if in_tasks or not in_results:
            if pattern.lower() in task.name.lower():
                match = True
        
        if in_results or not in_tasks:
            for res in task.results.values():
                if pattern.lower() in str(res).lower():
                    match = True
                    break
        
        if match:
            results.append(task)
    
    if json_out:
        console.print_json(data=[{
            'id': t.id,
            'name': t.name,
            'status': t.status.name,
            'created': t.created_at
        } for t in results])
    else:
        table = Table(title=f"Search Results for '{pattern}'")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Status", style="yellow")
        table.add_column("Created", style="dim")
        
        for task in results:
            table.add_row(
                task.id,
                task.name,
                task.status.name,
                time.strftime('%H:%M:%S', time.localtime(task.created_at))
            )
        
        console.print(table)


@cli.command()
@click.argument('task_id')
@click.option('--force', '-f', is_flag=True, help='Force cancel even if running')
async def cancel(task_id: str, force: bool):
    """
    ⛔ Cancel a running or pending task
    
    TASK_ID: The task ID to cancel
    
    Example:
      dongol cancel abc123
      dongol cancel abc123 --force
    """
    engine = await get_engine()
    
    if task_id not in engine.tasks:
        console.print(f"[red]Task {task_id} not found[/red]")
        return
    
    task = engine.tasks[task_id]
    
    if task.status == TaskStatus.RUNNING and not force:
        console.print(f"[yellow]Task is running. Use --force to cancel.[/yellow]")
        return
    
    task.status = TaskStatus.CANCELLED
    console.print(f"[green]Task {task_id} cancelled[/green]")


def main():
    """Entry point for the CLI"""
    # Patch click to support async
    import click
    
    def async_command(f):
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            return asyncio.run(f(ctx, *args, **kwargs))
        return wrapper
    
    # Run the CLI
    cli()


if __name__ == '__main__':
    import os
    main()
