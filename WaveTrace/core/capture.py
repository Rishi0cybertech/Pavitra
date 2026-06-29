import pyshark
import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich import box
from collections import defaultdict
from datetime import datetime

console = Console()

def get_interfaces():
    """Get all available network interfaces."""
    interfaces = []
    for name, addrs in psutil.net_if_addrs().items():
        interfaces.append(name)
    return interfaces


def display_interfaces():
    """Show available interfaces in a styled table."""
    interfaces = get_interfaces()

    table = Table(
        title="Available Network Interfaces",
        box=box.DOUBLE_EDGE,
        title_style="bold cyan",
        header_style="bold white on dark_blue",
        border_style="cyan",
        show_lines=True
    )
    table.add_column("No.", style="bold yellow", width=5)
    table.add_column("Interface", style="bold white", width=20)
    table.add_column("Status", style="bold green", width=10)

    for i, iface in enumerate(interfaces, 1):
        stats = psutil.net_if_stats().get(iface)
        status = "[green]UP[/green]" if stats and stats.isup else "[red]DOWN[/red]"
        table.add_row(str(i), iface, status)

    console.print()
    console.print(table)
    console.print()
    return interfaces


def capture_packets(interface: str, packet_count: int = 50) -> list:
    """Capture packets and return analyzed data."""

    stats = {
        "total":      0,
        "protocols":  defaultdict(int),
        "src_ips":    defaultdict(int),
        "dst_ips":    defaultdict(int),
        "suspicious": [],
        "packets":    [],
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    SUSPICIOUS_PORTS = {
        23: "Telnet — Unencrypted",
        21: "FTP — Cleartext",
        4444: "Metasploit Default",
        1337: "Hacker Port",
        31337: "Elite Hacker Port",
        6667: "IRC — Botnet C2",
        9001: "Tor Default",
    }

    console.print(Panel.fit(
        f"[bold cyan]WaveTrace — Network Packet Analyzer[/bold cyan]\n"
        f"[white]Interface : [yellow]{interface}[/yellow][/white]\n"
        f"[white]Capturing : [yellow]{packet_count} packets[/yellow][/white]\n"
        f"[white]Started   : [yellow]{stats['start_time']}[/yellow][/white]",
        border_style="cyan",
        title="[bold white]WAVETRACE v1.0[/bold white]",
        title_align="center"
    ))

    console.print()

    # Live capture table
    table = Table(
        box=box.SIMPLE_HEAVY,
        header_style="bold white on dark_blue",
        border_style="dim white",
        show_lines=False,
        expand=True
    )
    table.add_column("#",        style="dim white",    width=4)
    table.add_column("TIME",     style="cyan",         width=12)
    table.add_column("PROTOCOL", style="bold yellow",  width=10)
    table.add_column("SOURCE",   style="green",        width=20)
    table.add_column("DEST",     style="blue",         width=20)
    table.add_column("LENGTH",   style="white",        width=8)
    table.add_column("STATUS",   style="bold",         width=12)

    with Live(table, refresh_per_second=4, console=console):
        try:
            capture = pyshark.LiveCapture(interface=interface)
            count   = 0

            for packet in capture.sniff_continuously():
                if count >= packet_count:
                    break

                count += 1
                stats["total"] += 1

                # Extract fields
                proto  = packet.highest_layer
                src    = getattr(packet, 'ip', None)
                src_ip = src.src if src else "N/A"
                dst_ip = src.dst if src else "N/A"
                length = packet.length
                time   = datetime.now().strftime("%H:%M:%S")

                # Update stats
                stats["protocols"][proto] += 1
                if src_ip != "N/A":
                    stats["src_ips"][src_ip] += 1
                    stats["dst_ips"][dst_ip] += 1

                # Check suspicious
                status     = "[green]NORMAL[/green]"
                is_suspicious = False

                try:
                    dport = int(packet.tcp.dport) if hasattr(packet, 'tcp') else None
                    sport = int(packet.tcp.sport) if hasattr(packet, 'tcp') else None

                    for port in [dport, sport]:
                        if port and port in SUSPICIOUS_PORTS:
                            reason = SUSPICIOUS_PORTS[port]
                            stats["suspicious"].append({
                                "packet": count,
                                "src":    src_ip,
                                "dst":    dst_ip,
                                "port":   port,
                                "reason": reason
                            })
                            status        = f"[red]⚠ SUSPICIOUS[/red]"
                            is_suspicious = True
                except Exception:
                    pass

                stats["packets"].append({
                    "num":      count,
                    "time":     time,
                    "protocol": proto,
                    "src":      src_ip,
                    "dst":      dst_ip,
                    "length":   length,
                    "suspicious": is_suspicious
                })

                table.add_row(
                    str(count),
                    time,
                    f"[yellow]{proto}[/yellow]",
                    src_ip,
                    dst_ip,
                    str(length),
                    status
                )

        except Exception as e:
            console.print(f"[red]Capture error: {e}[/red]")

    # Summary panel
    console.print()
    console.print(Panel(
        f"[bold green]✔ Capture Complete[/bold green]\n\n"
        f"[white]Total Packets   : [cyan]{stats['total']}[/cyan]\n"
        f"Unique Protocols : [cyan]{len(stats['protocols'])}[/cyan]\n"
        f"Unique Sources   : [cyan]{len(stats['src_ips'])}[/cyan]\n"
        f"Suspicious       : [red]{len(stats['suspicious'])}[/red][/white]",
        border_style="green",
        title="[bold white]CAPTURE SUMMARY[/bold white]"
    ))

    stats["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return stats
