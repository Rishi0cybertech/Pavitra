import webbrowser
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import IntPrompt
from rich import box

console = Console()

LABS = [
    {
        "name": "Juice Shop",
        "category": "Modern Web Vulnerabilities (OWASP Top 10)",
        "url": "http://localhost:3000",
        "type": "web",
        "difficulty": "Beginner → Advanced",
        "hint": "Score Board is hidden — find it to track your progress",
    },
    {
        "name": "DVWA",
        "category": "Classic SQLi / XSS / Command Injection",
        "url": "http://localhost:8081",
        "type": "web",
        "difficulty": "Beginner → Advanced",
        "hint": "Login: admin / password — then click Setup to initialize",
    },
    {
        "name": "vsftpd — Anonymous FTP",
        "category": "Unauthenticated File Transfer",
        "url": "ftp://localhost:2121",
        "type": "cli",
        "difficulty": "Beginner",
        "hint": "Try: ftp 127.0.0.1 2121 — attempt anonymous login",
    },
    {
        "name": "Redis — No Auth",
        "category": "Unauthenticated Database Access",
        "url": "redis://localhost:6379",
        "type": "cli",
        "difficulty": "Beginner",
        "hint": "Try: redis-cli -p 6379 — then run: KEYS *",
    },
]


def show_banner():
    console.print(Panel.fit(
        "[bold magenta]███╗   ██╗███████╗████████╗██████╗  █████╗ \n"
        "[bold magenta]████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗\n"
        "[bold magenta]██╔██╗ ██║█████╗     ██║   ██████╔╝███████║\n"
        "[bold magenta]██║╚██╗██║██╔══╝     ██║   ██╔══██╗██╔══██║\n"
        "[bold magenta]██║ ╚████║███████╗   ██║   ██║  ██║██║  ██║\n"
        "[bold magenta]╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝[/bold magenta]\n\n"
        "[white]        Virtual Attack Labs — Pavitra Security Suite[/white]\n"
        "[dim]        Built by Rishi Gauttam | github.com/Rishi0cybertech[/dim]",
        border_style="magenta",
        box=box.DOUBLE_EDGE
    ))
    console.print()


def show_lab_table():
    table = Table(
        title="Available Labs",
        box=box.DOUBLE_EDGE,
        title_style="bold magenta",
        header_style="bold white on dark_magenta",
        border_style="magenta",
        show_lines=True
    )
    table.add_column("No.", style="bold yellow", width=4)
    table.add_column("Lab", style="bold white", width=22)
    table.add_column("Category", style="cyan", width=32)
    table.add_column("Difficulty", style="green", width=18)
    table.add_column("Access", style="bold blue", width=12)

    for i, lab in enumerate(LABS, 1):
        access = "🌐 Browser" if lab["type"] == "web" else "⌨ Terminal"
        table.add_row(str(i), lab["name"], lab["category"], lab["difficulty"], access)

    console.print(table)
    console.print()


def show_lab_detail(lab):
    console.print(Panel(
        f"[bold white]{lab['name']}[/bold white]\n\n"
        f"[cyan]Category:[/cyan]   {lab['category']}\n"
        f"[cyan]Difficulty:[/cyan] {lab['difficulty']}\n"
        f"[cyan]Access:[/cyan]     {lab['url']}\n\n"
        f"[yellow]💡 Hint:[/yellow] {lab['hint']}",
        border_style="green",
        title="[bold]LAB SELECTED[/bold]"
    ))

    if lab["type"] == "web":
        console.print(f"\n[bold green]→ Opening in browser:[/bold green] [underline blue]{lab['url']}[/underline blue]")
        try:
            webbrowser.open(lab["url"])
        except Exception:
            console.print("[dim]Could not auto-open — copy the link above manually.[/dim]")
    else:
        console.print(f"\n[bold yellow]→ This lab has no web GUI. Run this in a terminal:[/bold yellow]")
        console.print(f"[bold white]{lab['hint'].split('Try: ')[-1]}[/bold white]")

    console.print()


def main():
    show_banner()
    show_lab_table()

    choice = IntPrompt.ask(
        "[bold magenta]Select a lab number to begin[/bold magenta]",
        default=1
    )

    if choice < 1 or choice > len(LABS):
        console.print("[red]Invalid selection.[/red]")
        return

    show_lab_detail(LABS[choice - 1])


if __name__ == "__main__":
    main()
