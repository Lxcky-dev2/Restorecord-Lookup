import csv
import sys
import os
import glob
from ipwhois import IPWhois
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

csv.field_size_limit(10_000_000)

console = Console()

def load_dataset():
    dataset = {}
    files = sorted(glob.glob("users_part_*.csv"))
    if not files:
        console.print("[bold red]Error:[/bold red] No dataset files found.")
        return None
    for filepath in files:
        loaded = 0
        skipped = 0
        try:
            with open(filepath, mode='r', encoding='utf-8', errors='replace') as f:
                reader = csv.reader(f)
                for row in reader:
                    try:
                        if len(row) >= 4:
                            discord_id = row[1].strip()
                            if not discord_id:
                                skipped += 1
                                continue
                            dataset[discord_id] = {
                                "index": row[0].strip(),
                                "discord_id": discord_id,
                                "username": row[2].strip(),
                                "ip": row[3].strip(),
                                "timestamp": row[4].strip() if len(row) > 4 else "N/A"
                            }
                            loaded += 1
                        else:
                            skipped += 1
                    except Exception:
                        skipped += 1
        except Exception as e:
            console.print(f"[bold red]Error loading {filepath}:[/bold red] {e}")
            continue
        console.print(f"[dim]{filepath}: {loaded} loaded, {skipped} skipped[/dim]")
    return dataset

def discord_lookup(dataset):
    discord_id = Prompt.ask("[bold cyan]Discord ID[/bold cyan]")
    if not dataset:
        console.print("[bold red]Dataset is not loaded.[/bold red]")
        return
    user_data = dataset.get(discord_id.strip())
    if user_data:
        table = Table(title=f"User Found: {discord_id}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Discord ID", user_data["discord_id"])
        table.add_row("Username", user_data["username"])
        table.add_row("IP", user_data["ip"])
        table.add_row("Timestamp", user_data["timestamp"])
        console.print(table)
    else:
        console.print("[bold yellow]User not found in the data set[/bold yellow]")

def ip_lookup():
    ip_address = Prompt.ask("[bold cyan]Enter IP Address[/bold cyan]")
    try:
        obj = IPWhois(ip_address)
        results = obj.lookup_rdap(depth=1)
        country = results.get('asn_country_code', 'Unknown')
        asn_description = results.get('asn_description', 'Unknown')
        network = results.get('network', {}).get('name', 'Unknown')
        table = Table(title=f"IP Lookup: {ip_address}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("IP", ip_address)
        table.add_row("Country Code", country)
        table.add_row("ASN Description", asn_description)
        table.add_row("Network Name", network)
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Lookup failed:[/bold red] {e}")

def main():
    console.print("[bold white]Loading dataset...[/bold white]")
    dataset = load_dataset()
    if dataset is None:
        sys.exit(1)
    console.print(f"[bold green]Loaded {len(dataset):,} unique Discord IDs.[/bold green]")
    Prompt.ask("[dim]Press Enter to open LxckyTools...[/dim]", default="")
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        console.print(Panel.fit(
            "[bold magenta]LxckyTools[/bold magenta]",
            border_style="magenta",
            padding=(0, 4)
        ))
        console.print()
        console.print("  [bold cyan][1][/bold cyan] Discord Lookup")
        console.print("  [bold cyan][2][/bold cyan] IP Lookup")
        console.print("  [bold cyan][0][/bold cyan] Exit")
        console.print()
        choice = Prompt.ask("[bold yellow]Select an option[/bold yellow]", choices=["1", "2", "0"])
        if choice == "1":
            discord_lookup(dataset)
        elif choice == "2":
            ip_lookup()
        elif choice == "0":
            console.print("[bold]Exiting...[/bold]")
            break
        Prompt.ask("\n[dim]Press Enter to continue...[/dim]", default="")

if __name__ == "__main__":
    main()