import nmap
import json
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

console = Console()

def load_intel():
    path = Path("data/port_intel.json")
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def scan_target(target: str) -> list:
    """
    Always returns a LIST of host dicts — even a single IP scan
    returns a one-item list. Callers must not treat this as a dict.
    """
    nm = nmap.PortScanner()
    intel = load_intel()

    console.print(Panel.fit(
        f"[bold cyan]NPath Scanner v1.0[/bold cyan]\n"
        f"[white]Target : [yellow]{target}[/yellow][/white]\n"
        f"[white]Mode   : Service Detection[/white]",
        border_style="cyan"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Scanning target(s)...", total=None)
        nm.scan(hosts=target, arguments="-sV --open")
        progress.update(task, description="[green]Scan complete!")

    all_hosts = []

    if not nm.all_hosts():
        console.print("[red]No hosts responded. Check target/permissions.[/red]")
        return all_hosts

    for host in nm.all_hosts():
        host_data = {
            "ip": host,
            "hostname": nm[host].hostname(),
            "state": nm[host].state(),
            "ports": []
        }

        console.print(f"\n[bold green]Host    :[/bold green] {host} ({nm[host].hostname()})")
        console.print(f"[bold green]State   :[/bold green] {nm[host].state()}\n")

        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                service = nm[host][proto][port]

                intel_data = intel.get(str(port), {
                    "service":            service["name"],
                    "why_open":           "No data available",
                    "who_uses":           "N/A",
                    "who_exploits":       "Research manually",
                    "risk":               "Unknown — investigate",
                    "severity":           "MEDIUM",
                    "how_to_fix":         ["Research this port manually"],
                    "real_world_example": "N/A"
                })

                severity = intel_data.get("severity", "MEDIUM")
                severity_colors = {
                    "CRITICAL": "red", "HIGH": "orange1",
                    "MEDIUM": "yellow", "LOW": "green"
                }
                color = severity_colors.get(severity, "yellow")

                console.print(
                    f"  [bold white]PORT {port}/tcp[/bold white] "
                    f"[{color}][{severity}][/{color}] "
                    f"[cyan]{service['name']}[/cyan] "
                    f"[dim]{service.get('version', '')}[/dim]"
                )

                host_data["ports"].append({
                    "port":     port,
                    "protocol": proto,
                    "state":    service["state"],
                    "service":  service["name"],
                    "version":  service.get("version", "Unknown"),
                    "intel":    intel_data
                })

        all_hosts.append(host_data)

    console.print(f"\n[bold cyan]Total hosts scanned: {len(all_hosts)}[/bold cyan]\n")
    return all_hosts