import logging
import argparse
import sys
import random
import time
from rich.console import Console
from rich.logging import RichHandler
from os import system, name
from typing import List
from requests import get
from codecs import encode
from mmh3 import hash as favhash
from concurrent.futures import ThreadPoolExecutor


console = Console()
FORMAT = "%(message)s"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")


class FavFinder:	
	
	@staticmethod
	def clean_console() -> None:
		system("cls" if name == "nt" else "clear")
	

	@staticmethod
	def print_ascii_art():
		colors = [36, 32, 34, 35, 31, 37]
		clear = "\x1b[0m"
		ascii_art = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠾⠛⢉⣉⣉⣉⡉⠛⠷⣦⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠋⣠⣴⣿⣿⣿⣿⣿⡿⣿⣶⣌⠹⣷⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣆⠉⠻⣧⠘⣷⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠈⠀⢹⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢸⣿⠛⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⢸⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⢿⡆⠈⠛⠻⠟⠛⠉⠀⠀⠀⠀⠀⠀⣾⠃⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣧⡀⠻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⠿⣦⣄⠀⠀⠀⠀⠀⠀⠀⣀⣴⠟⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣦⠀⠀⠈⠉⠛⠓⠲⠶⠖⠚⠋⠉⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣾⣿⣿⠟⠁⠀⠀FavFinder v1.0⠀⠀⠀⠀
⠀⠀⠀⣾⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣄⠈⠛⠁⠀github.com/0xuf⠀⠀⠀⠀⠀⠀⠀⠀
- Coded with <3 By ZeroXUF 
	"""
		for N, line in enumerate(ascii_art.split("\n")):
				sys.stdout.write("\x1b[1;%dm%s%s\n" %(random.choice(colors), line, clear))
				time.sleep(0.05)
	

	@staticmethod
	def normalize_url(url: str) -> str:
		# Normalize url with http schemes

		schemes = ("https://", "http://")
		if not url.startswith(schemes):
			url = f"http://{url}"
		
		return url
	
	def find_hash(self, link: str, silent: bool) -> None:
		link = self.normalize_url(url=link)

		# Add favicon.ico end of the link
		fav_link = f"{link}favicon.ico" if link.endswith("/") else f"{link}/favicon.ico"

		# Make http request to get favicon.ico response
		response = get(fav_link, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}, timeout=5)
		favicon_hash = None

		# Print the favhash if status code is 200 and everything is ok
		if response.status_code == 200:
			favicon = encode(response.content, "base64")
			favicon_hash = favhash(favicon)
			if silent:
				print(f"{link} => {favicon_hash}")
			else:
				console.log(f"[bold yellow][ [bold red]{link}[bold yellow] ][bold cyan] => [bold green]{favicon_hash}")
		else:
			if not silent:
				log.error(f"couldn't find favicon of {link}")


	
	def fav_finder(self, silent: bool, websites: List[str], threads: int) -> None:
		
		with ThreadPoolExecutor(max_workers=threads) as executor:
			for website in websites:
				executor.submit(self.find_hash, website, silent)



if __name__ == "__main__":
	
	# Parse arguments
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument("--silent", "-silent", action="store_true", help="Show output only without any ascii art")
	argument_parser.add_argument("--threads", "-t", type=int, default=5, help="Number of threads")
	arguments = argument_parser.parse_args()

	# Clean the console and print ascii art
	if not arguments.silent:
		FavFinder.clean_console()
		FavFinder.print_ascii_art()
	
	# Check if stdin is empty
	if not sys.stdin.isatty():
		websites = [line for line in sys.stdin]
		websites = list(map(str.strip, websites))

		if not len(websites) <= 0:
			if websites[0] == "":
				log.error("\tWebsites list cannot be empty!")
				console.log("[bold GREEN]Exiting ...")
				sys.exit()
		
	else:
		console.log("[bold blue]Usage: ")
		console.log(f"[bold white]$[bold green] echo domain.tld [bold cyan]| [bold green]python {sys.argv[0]}")
		console.log(f"[bold white]$[bold green] cat domains.txt [bold cyan]| [bold green]python {sys.argv[0]}")
		sys.exit()
	
	
	# Make instance from FavFinder class
	instance = FavFinder()
	instance.fav_finder(silent=arguments.silent, websites=websites, threads=arguments.threads)