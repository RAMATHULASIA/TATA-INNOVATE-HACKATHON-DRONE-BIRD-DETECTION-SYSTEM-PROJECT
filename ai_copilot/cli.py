"""
Command Line Interface for AI Co-pilot

Provides a user-friendly CLI for interacting with the AI co-pilot system.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, List
import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .core import AICopilot, CodeRequest
from .config import CopilotConfig


console = Console()


@click.group()
@click.version_option(version="0.1.0")
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.pass_context
def main(ctx, config: Optional[str], debug: bool):
    """
    AI Co-pilot for Embedded Software Design
    
    Generate, analyze, and optimize embedded software for smart vehicles.
    """
    # Load configuration
    if config:
        copilot_config = CopilotConfig.from_file(config)
    else:
        copilot_config = CopilotConfig()
    
    if debug:
        copilot_config.debug = True
        copilot_config.log_level = "DEBUG"
    
    # Store config in context
    ctx.ensure_object(dict)
    ctx.obj['config'] = copilot_config


@main.command()
@click.argument('description')
@click.option('--language', '-l', default='c', help='Programming language (c, cpp)')
@click.option('--platform', '-p', help='Target platform/ECU type')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--constraints', help='Additional constraints (JSON format)')
@click.pass_context
def generate(ctx, description: str, language: str, platform: Optional[str], 
             output: Optional[str], constraints: Optional[str]):
    """Generate code based on description"""
    
    config = ctx.obj['config']
    
    async def _generate():
        copilot = AICopilot(config)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Initializing AI Co-pilot...", total=None)
            await copilot.initialize()
            
            progress.update(task, description="Generating code...")
            
            # Parse constraints if provided
            constraint_dict = None
            if constraints:
                import json
                try:
                    constraint_dict = json.loads(constraints)
                except json.JSONDecodeError:
                    console.print("[red]Error: Invalid JSON format for constraints[/red]")
                    return
            
            # Create request
            request = CodeRequest(
                description=description,
                language=language,
                target_platform=platform,
                constraints=constraint_dict
            )
            
            # Generate code
            response = await copilot.generate_code(request)
            
            progress.update(task, description="Code generation completed!")
        
        # Display results
        console.print("\n" + "="*60)
        console.print(Panel(description, title="[bold blue]Generated Code Description[/bold blue]"))
        
        # Show generated code with syntax highlighting
        syntax = Syntax(response.generated_code, language, theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="[bold green]Generated Code[/bold green]"))
        
        # Show explanation
        if response.explanation:
            console.print(Panel(response.explanation, title="[bold yellow]Explanation[/bold yellow]"))
        
        # Show warnings
        if response.warnings:
            warning_text = "\n".join(f"• {warning}" for warning in response.warnings)
            console.print(Panel(warning_text, title="[bold red]Warnings[/bold red]"))
        
        # Show suggestions
        if response.suggestions:
            suggestion_text = "\n".join(f"• {suggestion}" for suggestion in response.suggestions)
            console.print(Panel(suggestion_text, title="[bold cyan]Suggestions[/bold cyan]"))
        
        # Save to file if requested
        if output:
            output_path = Path(output)
            output_path.write_text(response.generated_code)
            console.print(f"\n[green]Code saved to: {output_path}[/green]")
        
        copilot.shutdown()
    
    asyncio.run(_generate())


@main.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--language', '-l', default='c', help='Programming language')
@click.pass_context
def analyze(ctx, file_path: str, language: str):
    """Analyze existing code file"""
    
    config = ctx.obj['config']
    
    async def _analyze():
        copilot = AICopilot(config)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Initializing AI Co-pilot...", total=None)
            await copilot.initialize()
            
            progress.update(task, description="Analyzing code...")
            
            # Read file
            code = Path(file_path).read_text()
            
            # Analyze code
            analysis = await copilot.analyze_existing_code(code, language)
            
            progress.update(task, description="Analysis completed!")
        
        # Display results
        console.print("\n" + "="*60)
        console.print(Panel(f"Analysis of: {file_path}", title="[bold blue]Code Analysis[/bold blue]"))
        
        # Show metrics
        if 'metrics' in analysis:
            metrics_table = Table(title="Code Metrics")
            metrics_table.add_column("Metric", style="cyan")
            metrics_table.add_column("Value", style="green")
            
            for key, value in analysis['metrics'].items():
                metrics_table.add_row(key.replace('_', ' ').title(), str(value))
            
            console.print(metrics_table)
        
        # Show warnings
        if analysis.get('warnings'):
            warning_text = "\n".join(f"• {warning}" for warning in analysis['warnings'])
            console.print(Panel(warning_text, title="[bold red]Warnings[/bold red]"))
        
        # Show suggestions
        if analysis.get('suggestions'):
            suggestion_text = "\n".join(f"• {suggestion}" for suggestion in analysis['suggestions'])
            console.print(Panel(suggestion_text, title="[bold cyan]Suggestions[/bold cyan]"))
        
        copilot.shutdown()
    
    asyncio.run(_analyze())


@main.command()
@click.pass_context
def interactive(ctx):
    """Start interactive mode"""
    
    config = ctx.obj['config']
    
    async def _interactive():
        copilot = AICopilot(config)
        
        console.print(Panel(
            "Welcome to AI Co-pilot Interactive Mode!\n"
            "Type 'help' for commands, 'exit' to quit.",
            title="[bold blue]AI Co-pilot Interactive Mode[/bold blue]"
        ))
        
        await copilot.initialize()
        
        while True:
            try:
                user_input = console.input("\n[bold green]ai-copilot>[/bold green] ")
                
                if user_input.lower() in ['exit', 'quit']:
                    break
                elif user_input.lower() == 'help':
                    show_interactive_help()
                elif user_input.startswith('generate '):
                    description = user_input[9:]  # Remove 'generate '
                    await handle_interactive_generate(copilot, description)
                elif user_input.startswith('analyze '):
                    file_path = user_input[8:]  # Remove 'analyze '
                    await handle_interactive_analyze(copilot, file_path)
                else:
                    console.print("[yellow]Unknown command. Type 'help' for available commands.[/yellow]")
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
        
        console.print("\n[blue]Goodbye![/blue]")
        copilot.shutdown()
    
    asyncio.run(_interactive())


def show_interactive_help():
    """Show help for interactive mode"""
    help_table = Table(title="Interactive Commands")
    help_table.add_column("Command", style="cyan")
    help_table.add_column("Description", style="white")
    
    help_table.add_row("generate <description>", "Generate code from description")
    help_table.add_row("analyze <file_path>", "Analyze existing code file")
    help_table.add_row("help", "Show this help message")
    help_table.add_row("exit/quit", "Exit interactive mode")
    
    console.print(help_table)


async def handle_interactive_generate(copilot: AICopilot, description: str):
    """Handle interactive code generation"""
    try:
        request = CodeRequest(description=description)
        response = await copilot.generate_code(request)
        
        # Show generated code
        syntax = Syntax(response.generated_code, "c", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="[bold green]Generated Code[/bold green]"))
        
        if response.warnings:
            warning_text = "\n".join(f"• {warning}" for warning in response.warnings)
            console.print(Panel(warning_text, title="[bold red]Warnings[/bold red]"))
    
    except Exception as e:
        console.print(f"[red]Generation failed: {e}[/red]")


async def handle_interactive_analyze(copilot: AICopilot, file_path: str):
    """Handle interactive code analysis"""
    try:
        if not Path(file_path).exists():
            console.print(f"[red]File not found: {file_path}[/red]")
            return
        
        code = Path(file_path).read_text()
        analysis = await copilot.analyze_existing_code(code)
        
        if analysis.get('warnings'):
            warning_text = "\n".join(f"• {warning}" for warning in analysis['warnings'])
            console.print(Panel(warning_text, title="[bold red]Warnings[/bold red]"))
        else:
            console.print("[green]No issues found![/green]")
    
    except Exception as e:
        console.print(f"[red]Analysis failed: {e}[/red]")


@main.command()
@click.pass_context
def config_init(ctx):
    """Initialize configuration file"""
    config_path = CopilotConfig.get_default_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    default_config = CopilotConfig()
    default_config.to_file(str(config_path))
    
    console.print(f"[green]Configuration file created at: {config_path}[/green]")


if __name__ == '__main__':
    main()
