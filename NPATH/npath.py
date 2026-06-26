import sys
from core.scanner import scan_target
from core.reporter import generate_report
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    args = sys.argv[1:]

    if len(args) == 0 or args[0] in ("--help", "-h"):
        console.print(Panel.fit(
            "[bold cyan]NPath — Network Scanner[/bold cyan]\n\n"
            "[white]Usage:[/white]\n"
            "  python3 npath.py scan [TARGET]\n"
            "  python3 npath.py scan [TARGET] --report\n\n"
            "[white]Examples:[/white]\n"
            "  python3 npath.py scan 127.0.0.1\n"
            "  python3 npath.py scan 127.0.0.1 --report\n"
            "  python3 npath.py scan 192.168.1.1 --report",
            border_style="cyan"
        ))
        return

    if args[0] == "scan":
        if len(args) < 2:
            console.print("[red]Error:[/red] Target IP required.")
            console.print("Usage: python3 npath.py scan 127.0.0.1")
            return

        target     = args[1]
        make_report = "--report" in args or "-r" in args

        data = scan_target(target)

        if make_report:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename  = f"npath_report_{timestamp}.pdf"
            generate_report(data, filename)
        else:
            console.print("\n[bold green]Scan complete.[/bold green] Use --report to generate PDF.")
    else:
        console.print(f"[red]Unknown command:[/red] {args[0]}")
        console.print("Use: python3 npath.py --help")

if __name__ == "__main__":
    main()
