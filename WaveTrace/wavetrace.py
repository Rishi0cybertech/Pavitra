import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich import box
from core.capture import display_interfaces, capture_packets
from core.reporter import generate_report
from datetime import datetime

console = Console()

def show_banner():
    console.print(Panel.fit(
        "[bold cyan]██╗    ██╗ █████╗ ██╗   ██╗███████╗\n"
        "[bold cyan]██║    ██║██╔══██╗██║   ██║██╔════╝\n"
        "[bold cyan]██║ █╗ ██║███████║██║   ██║█████╗  \n"
        "[bold cyan]██║███╗██║██╔══██║╚██╗ ██╔╝██╔══╝  \n"
        "[bold cyan]╚███╔███╔╝██║  ██║ ╚████╔╝ ███████╗\n"
        "[bold cyan] ╚══╝╚══╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝\n"
        "[bold cyan]        ████████╗██████╗  █████╗  ██████╗███████╗\n"
        "[bold cyan]        ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝\n"
        "[bold cyan]           ██║   ██████╔╝███████║██║     █████╗  \n"
        "[bold cyan]           ██║   ██╔══██╗██╔══██║██║     ██╔══╝  \n"
        "[bold cyan]           ██║   ██║  ██║██║  ██║╚██████╗███████╗\n"
        "[bold cyan]           ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝[/bold cyan]\n\n"
        "[white]        Network Packet Analyzer — Part of Pavitra Security Suite[/white]\n"
        "[dim]        Built by Rishi Gauttam | github.com/Rishi0cybertech[/dim]",
        border_style="cyan",
        box=box.DOUBLE_EDGE
    ))
    console.print()

def main():
    show_banner()

    console.print("[bold cyan]STEP 1[/bold cyan] — Select a network interface:\n")
    interfaces = display_interfaces()

    choice = IntPrompt.ask("[bold yellow]Enter interface number[/bold yellow]", default=1)

    if choice < 1 or choice > len(interfaces):
        console.print("[red]Invalid choice. Exiting.[/red]")
        sys.exit(1)

    selected = interfaces[choice - 1]
    console.print(f"\n[green]✔ Selected:[/green] [bold white]{selected}[/bold white]\n")

    count = IntPrompt.ask("[bold yellow]How many packets to capture[/bold yellow]", default=50)

    console.print()
    stats = capture_packets(interface=selected, packet_count=count)
    stats["interface"] = selected

    console.print()
    make_report = Prompt.ask(
        "[bold yellow]Generate PDF report?[/bold yellow]",
        choices=["y", "n"],
        default="y"
    )

    if make_report == "y":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename  = f"reports/wavetrace_report_{timestamp}.pdf"
        generate_report(stats, filename)
        console.print(f"\n[bold green]✔ Report saved:[/bold green] [cyan]{filename}[/cyan]")
    else:
        console.print("\n[dim]Report skipped.[/dim]")

if __name__ == "__main__":
    main()
