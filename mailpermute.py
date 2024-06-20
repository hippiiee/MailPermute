import aiohttp
import argparse
import asyncio
from checkers import gmail, yahoo, yandex, duckduckgo
from rich.progress import Progress
import sys

version_number = "0.7"

banner = f"""\x1b[0;33m
888b     d888          d8b 888                                                  888            
8888b   d8888          Y8P 888                                                  888            
88888b.d88888              888                                                  888            
888Y88888P888  8888b.  888 888 88888b.   .d88b.  888d888 88888b.d88b.  888  888 888888 .d88b.  
888 Y888P 888     "88b 888 888 888 "88b d8P  Y8b 888P"   888 "888 "88b 888  888 888   d8P  Y8b 
888  Y8P  888 .d888888 888 888 888  888 88888888 888     888  888  888 888  888 888   88888888 
888   "   888 888  888 888 888 888 d88P Y8b.     888     888  888  888 Y88b 888 Y88b. Y8b.     
888       888 "Y888888 888 888 88888P"   "Y8888  888     888  888  888  "Y88888  "Y888 "Y8888  
                               888 \x1b[1;33mv{version_number}\x1b[0;33m                                                       
                               888                                                             
                               888                                                             
\x1b[0;1;3mBy Hippie\x1b[0;33m | \x1b[0;1mhttps://twitter.com/hiippiiie\x1b[0m
"""

def gen_permutations(firstname, lastname):
    permutations = []
    separators = ['','-','_']

    for separator in separators:
        permutations.append(f"{lastname}{separator}{firstname}")
        permutations.append(f"{firstname}{separator}{lastname}")
        permutations.append(f"{firstname[0]}{separator}{lastname}")
        permutations.append(f"{lastname}{separator}{firstname[0]}")
        permutations.append(f"{lastname[0]}{separator}{firstname}")
        permutations.append(f"{firstname}{separator}{lastname[0]}")
    
    return permutations

def parse_args():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-n", "--name", default=None, help='Name of the person (e.g. "John Doe")')
    parser.add_argument("-c", "--checkers", default="all", help='Checkers to use (e.g. "gmail, yandex")')
    args = parser.parse_args()
    
    return args

async def print_results(checker, target, session):
    err = None
    res = await checker(target, session)
    if isinstance(res, tuple):
      res, err = res
      if err:
        print("error",checker, err)
    if bool(res):
      print("\033[1;32m[+]\033[0m",res.get(checker.__name__.title()))

async def main():
    args = parse_args()
    all_checkers = [duckduckgo, gmail, yahoo, yandex]
    checkers = []

    if args.name:
        name_parts = args.name.lower().split()
        if len(name_parts) != 2:
            print('Error: The name must consist of exactly two parts (e.g. "John Doe").')
            sys.exit(1)
        if args.checkers != 'all':
            selected_checkers = args.checkers.lower().split(',')
            for chk in selected_checkers:
                checker_func = next((c for c in all_checkers if c.__name__ == chk), None)
                if checker_func:
                    checkers.append(checker_func)
                else:
                    print(f"Error: The checker {chk} does not exist.")
                    sys.exit(1)
        else:
            checkers = all_checkers 
        if len(checkers) > 0:
            async with aiohttp.ClientSession() as session:
                email_permutations = gen_permutations(name_parts[0], name_parts[-1])
                with Progress() as progress:
                    task = progress.add_task("[green]Testing permutations...", total=len(email_permutations))
                    for target in email_permutations:
                        progress.update(task, description=f"[green]Testing {target}", advance=1)
                        jobs = asyncio.gather(
                            *[print_results(checker, target, session) for checker in checkers]
                        )
                        await jobs

    else:
        print('Help: ./mailpermute -h')
        sys.exit(1)


if __name__ == '__main__':
  print(banner)
  loop = asyncio.new_event_loop()
  loop.run_until_complete(main())

