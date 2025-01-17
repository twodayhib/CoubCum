import requests
import json
import os
import urllib.parse
from core.helper import get_headers, countdown_timer, extract_user_data, config
from colorama import *
import random
from datetime import datetime
import time


class Coub:
    def __init__(self) -> None:
        self.session = requests.Session()

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        banner = f"""{Fore.GREEN}
 ██████  ██    ██   ██████  ██    ██  ███    ███  ██████   ███████  ██████  
██       ██    ██  ██       ██    ██  ████  ████  ██   ██  ██       ██   ██ 
██       ██    ██  ██       ██    ██  ██ ████ ██  ██████   █████    ██████  
██       ██    ██  ██       ██    ██  ██  ██  ██  ██   ██  ██       ██   ██ 
 ██████   ██████    ██████   ██████   ██      ██  ██████   ███████  ██   ██     
                                            """
        print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
        print(Fore.GREEN + f" Coub bot")
        print(Fore.RED + f" FREE TO USE = Join us on {Fore.GREEN}t.me/cucumber_scripts")
        print(Fore.YELLOW + f" before start please '{Fore.GREEN}git pull{Fore.YELLOW}' to update bot")
        print(f"{Fore.WHITE}~" * 60)

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        query = query_params.get('user', [None])[0]

        if query:
            user_data_json = urllib.parse.unquote(query)
            user_data = json.loads(user_data_json)
            first_name = user_data.get('first_name', 'unknown')
            return first_name
        else:
            raise ValueError("User data not found in query.")
    
    def load_task_list(self):
        url = "https://raw.githubusercontent.com/vonssy/Response.JSON/refs/heads/main/coub_tasks.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get('task_list', [])
        except requests.exceptions.RequestException as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Error: Failed to fetch data from URL. {e}{Style.RESET_ALL}")
            return []
        except json.JSONDecodeError:
            self.log(f"{Fore.RED + Style.BRIGHT}Error: Failed to parse JSON data.{Style.RESET_ALL}")
            return []
        
    def login(self, query: str, retries=5, delay=3):
        url = 'https://coub.com/api/v2/sessions/login_mini_app'
        data = query
        self.headers.update({
            'Content-Length': str(len(data)),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'coub.com',
            'Origin': 'https://coub.com',
            'Referer': 'https://coub.com/tg-app',
            'Sec-Fetch-Site': 'same-origin',
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                result = response.json()
                if response.status_code == 200:
                    return result['api_token']
                else:
                    return None
            except Exception as e:
                if "RemoteDisconnected" in str(e) or "requests.exceptions" in str(e):
                    if attempt < retries - 1:
                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                            end="\r",
                            flush=True
                        )
                        time.sleep(delay * (2 ** attempt))
                else:
                    return None
    
    def get_token(self, api_token: str, retries=5, delay=3):
        url = 'https://coub.com/api/v2/torus/token'
        self.headers.update({
            'Content-Length': '0',
            'X-Auth-Token': api_token,
            'Host': 'coub.com',
            'Origin': 'https://coub.com',
            'Referer': 'https://coub.com/tg-app',
            'Sec-Fetch-Site': 'same-origin',
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers)
                result = response.json()
                if response.status_code == 200:
                    return result['access_token']
                else:
                    return None
            except Exception as e:
                if "RemoteDisconnected" in str(e) or "requests.exceptions" in str(e):
                    if attempt < retries - 1:
                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                            end="\r",
                            flush=True
                        )
                        time.sleep(delay * (2 ** attempt))
                else:
                    return None
        
    def user_rewards(self, token: str, query: str, retries=5, delay=3):
        url = 'https://rewards.coub.com/api/v2/get_user_rewards'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'X-Tg-Authorization': query,
            'Host': 'rewards.coub.com',
            'Origin': 'https://coub.com',
            'Referer': 'https://coub.com/',
            'Sec-Fetch-Site': 'same-site',
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                result = response.json()
                if response.status_code == 200:
                    return result
                else:
                    return None
            except Exception as e:
                if "RemoteDisconnected" in str(e) or "requests.exceptions" in str(e):
                    if attempt < retries - 1:
                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                            end="\r",
                            flush=True
                        )
                        time.sleep(delay * (2 ** attempt))
                else:
                    return None
    
    def refferal_rewards(self, token: str, query: str, retries=5, delay=3):
        url = 'https://rewards.coub.com/api/v2/referal_rewards'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'X-Tg-Authorization': query,
            'Host': 'rewards.coub.com',
            'Origin': 'https://coub.com',
            'Referer': 'https://coub.com/',
            'Sec-Fetch-Site': 'same-site',
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                result = response.json()
                if response.status_code == 200:
                    return result
                else:
                    return None
            except Exception as e:
                if "RemoteDisconnected" in str(e) or "requests.exceptions" in str(e):
                    if attempt < retries - 1:
                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                            end="\r",
                            flush=True
                        )
                        time.sleep(delay * (2 ** attempt))
                else:
                    return None
    
    def complete_tasks(self, token: str, query: str, task_id, retries=5, delay=3):
        url = "https://rewards.coub.com/api/v2/complete_task"
        params = {"task_reward_id": task_id}
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'X-Tg-Authorization': query,
            'Host': 'rewards.coub.com',
            'Origin': 'https://coub.com',
            'Referer': 'https://coub.com/',
            'Sec-Fetch-Site': 'same-site',
        })
        
        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers, params=params)
                result = response.json()
                if response.status_code == 200:
                    return result
                else:
                    return None
            except Exception as e:
                if "RemoteDisconnected" in str(e) or "requests.exceptions" in str(e):
                    if attempt < retries - 1:
                        print(
                            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}[{attempt + 1}/{retries}]{Style.RESET_ALL}",
                            end="\r",
                            flush=True
                        )
                        time.sleep(delay * (2 ** attempt))
                else:
                    return None
    def set_proxy(self, proxy):
        self.session.proxies = {
            "http": proxy,
            "https": proxy,
        }
        if '@' in proxy:
            host_port = proxy.split('@')[-1]
        else:
            host_port = proxy.split('//')[-1]
        return host_port

    def process_query(self, query: str):
        
        first_name = self.load_data(query)
        if not first_name:
            return

        api_token = self.login(query)
        if not api_token:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {first_name} {Style.RESET_ALL}"
                f"{Fore.CYAN+Style.BRIGHT}] [ Token{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Is None {Style.RESET_ALL}"
                f"{Fore.CYAN+Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return

        token = self.get_token(api_token)
        if not token:
            self.log(
                f"{Fore.CYAN+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {first_name} {Style.RESET_ALL}"
                f"{Fore.CYAN+Style.BRIGHT}] [ Token{Style.RESET_ALL}"
                f"{Fore.RED+Style.BRIGHT} Is None {Style.RESET_ALL}"
                f"{Fore.CYAN+Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return
        
        if token:
            user = self.user_rewards(token, query)
            reff = self.refferal_rewards(token, query)
            user_rewards = sum(point['points'] for point in user)
            reff_rewards = reff['referal_balance']

            total_rewards = user_rewards + reff_rewards

            if total_rewards:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {first_name} {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {total_rewards} $COUB {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}]{Style.RESET_ALL}"
                )
            else:
                self.log(
                    f"{Fore.CYAN+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {first_name} {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Is None {Style.RESET_ALL}"
                    f"{Fore.CYAN+Style.BRIGHT}]{Style.RESET_ALL}"
                )
            time.sleep(1)

            tasks = self.load_task_list()
            if tasks:
                for task in tasks:
                    task_id = task['id']
                    title = task['title']
                    reward = task['reward']
                    status = task['status']

                    if status in ["ready-to-start", "ready-to-claim"]:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {task_id} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}-{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {title} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Status{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {status} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )

                        complete_task = self.complete_tasks(token, query, task_id)
                        if complete_task:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {title} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}is Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {reward} $COUB {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {title} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}is Failed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} or {Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT}Already Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        time.sleep(1)
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
        
    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]
            with open('proxies.txt', 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]

            while True:
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Proxy's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(proxies)}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.CYAN + Style.BRIGHT}-----------------------------------------------------------------------{Style.RESET_ALL}")

                for i, query in enumerate(queries):
                    query = query.strip()
                    if query:
                        self.log(
                            f"{Fore.GREEN + Style.BRIGHT}Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{i + 1} / {len(queries)}{Style.RESET_ALL}"
                        )
                        if len(proxies) >= len(queries):
                            proxy = self.set_proxy(proxies[i])  # Set proxy for each account
                            self.log(
                                f"{Fore.GREEN + Style.BRIGHT}Use proxy: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
                            )

                        else:
                            self.log(
                                Fore.RED + "Number of proxies is less than the number of accounts. Proxies are not used!")

                    user_info = extract_user_data(query)
                    user_id = str(user_info.get('id'))
                    self.headers = get_headers(user_id)

                    try:
                        self.process_query(query)
                    except Exception as e:
                        self.log(f"{Fore.RED + Style.BRIGHT}An error process_query: {e}{Style.RESET_ALL}")

                    self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}" * 75)
                    account_delay = config['account_delay']
                    countdown_timer(random.randint(min(account_delay), max(account_delay)))

                cycle_delay = config['cycle_delay']
                countdown_timer(random.randint(min(cycle_delay), max(cycle_delay)))

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Coub - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    coub = Coub()
    coub.clear_terminal()
    coub.welcome()
    coub.main()