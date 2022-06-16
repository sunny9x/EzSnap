import requests, threading, random, string, re, os, json, ctypes
from colorama import Fore, init; init(autoreset=True)

class EzSnap:
    def __init__(self):
        if os.name == "nt":
            os.system("mode con: cols=138 lines=30")

        self.title("Initialization")

        self.logo()

        if not os.path.isfile("settings.json"):
            json.dump({
                "threads": 1,
                "proxiesUsage": {
                    "proxies": "http://user:pass@ip:port"
                }
            }, open("settings.json", "w", encoding="utf-8"), indent=4)

            print(f"{Fore.LIGHTMAGENTA_EX}Please modify the EzSnap settings which can be found in the settings.json file then save and press any key (If you don't want to use proxies, set proxies to None).")

            input()

            self.logo()

        self.config = json.load(open("settings.json", encoding="utf-8"))

        self.tLocker = threading.Lock()

        self.generated = 0

    def title(self, title: str):
        if os.name == "nt":
            ctypes.windll.kernel32.SetConsoleTitleW(f"EzSnap | By Frogy | {title}")
        else:
            print(f"\33]0;EzSnap | By Frogy | {title}\a", end="", flush=True)

    def logo(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        print(f"""{Fore.LIGHTYELLOW_EX}
                                            ███████╗███████╗███████╗███╗   ██╗ █████╗ ██████╗ 
                                            ██╔════╝╚══███╔╝██╔════╝████╗  ██║██╔══██╗██╔══██╗
                                            █████╗    ███╔╝ ███████╗██╔██╗ ██║███████║██████╔╝
                                            ██╔══╝   ███╔╝  ╚════██║██║╚██╗██║██╔══██║██╔═══╝ 
                                            ███████╗███████╗███████║██║ ╚████║██║  ██║██║     
                                            ╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     
                                                             {Fore.LIGHTCYAN_EX}The BEST Snapchat Account Generator by Frogy

{Fore.RESET}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n
        """)

    def generate(self, threadId: int):
        try:
            session = requests.Session()

            getCookies = session.get("https://accounts.snapchat.com/accounts/signup?client_id=ads-api&referrer=https%253A%252F%252Fads.snapchat.com%252Fgetstarted&ignore_welcome_email=true")

            if not "xsrf_token" in session.cookies.get_dict():
                self.tLocker.acquire()
                print(f"{Fore.LIGHTCYAN_EX}[#{threadId}] {Fore.LIGHTRED_EX}Unable to retrieve xsrf_token.")
                self.tLocker.release()

                return self.generate(threadId)

            username = f"{random.choice(string.ascii_letters)}{''.join(random.choice(string.ascii_letters + string.digits) for _ in range(11))}"

            getUsernames = session.post("https://accounts.snapchat.com/accounts/get_username_suggestions", data={
                "requested_username": username,
                "xsrf_token": session.cookies.get_dict()["xsrf_token"]
            }, proxies={
                "http": self.config["proxiesUsage"]["proxies"],
                "https": self.config["proxiesUsage"]["proxies"]
            })

            if getUsernames.text == "":
                self.tLocker.acquire()
                print(f"{Fore.LIGHTCYAN_EX}[#{threadId}] {Fore.LIGHTRED_EX}Unable to retrieve username sugegstions (you are most likely ratelimited).")
                self.tLocker.release()

                return self.generate(threadId)

            getUsernames = getUsernames.json()

            if getUsernames["reference"]["status_code"] == "TAKEN":
                username = getUsernames["reference"]["suggestions"][0]

            getRecaptchaToken = session.get("https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LezjdAZAAAAAD1FaW81QpkkplPNzCNnIOU5anHw&co=aHR0cHM6Ly9hY2NvdW50cy5zbmFwY2hhdC5jb206NDQz&hl=en&v=M-QqaF9xk6BpjLH22uHZRhXt&size=invisible&badge=inline&cb=9qlf8d10oqh9")

            recaptchaToken = re.findall('recaptcha-token" value="(.+?)"', getRecaptchaToken.text)

            if len(recaptchaToken) == 0:
                self.tLocker.acquire()
                print(f"{Fore.LIGHTCYAN_EX}[#{threadId}] {Fore.LIGHTRED_EX}Unable to retrieve recaptchaToken.")
                self.tLocker.release()

                return self.generate(threadId)

            getRecaptchaResponse = session.post("https://www.google.com/recaptcha/enterprise/reload?k=6LezjdAZAAAAAD1FaW81QpkkplPNzCNnIOU5anHw", data={
                "v": "M-QqaF9xk6BpjLH22uHZRhXt",
                "reason": "q",
                "c": recaptchaToken[0],
            })

            recaptchaSolution = re.findall('rresp","(.+?)"', getRecaptchaResponse.text)

            if len(recaptchaSolution) == 0:
                self.tLocker.acquire()
                print(f"{Fore.LIGHTCYAN_EX}[#{threadId}] {Fore.LIGHTRED_EX}Unable to retrieve recaptchaSolution.")
                self.tLocker.release()

                return self.generate(threadId)

            register = session.post("https://accounts.snapchat.com/accounts/signup", data={
                "first_name": "EzSnapByFrogyOnTop", 
                "last_name": "", 
                "username": username, 
                "password": "EzSnapByFrogyOnTop", 
                "birthday": "2000-06-12", 
                "email": f"{username}@gmail.com",
                "xsrf_token": session.cookies.get_dict()["xsrf_token"], 
                "g-recaptcha-response": recaptchaSolution[0],
                "client_id": "ads-api", 
                "referrer": "https://ads.snapchat.com/getstarted", 
                "ignore_welcome_email": True
            }, proxies={
                "http": self.config["proxiesUsage"]["proxies"],
                "https": self.config["proxiesUsage"]["proxies"]
            })

            if register.status_code == 200:
                self.tLocker.acquire()
                self.generated += 1

                self.title(f"Generated - {self.generated}")

                with open("generated.txt", "a", encoding="utf-8") as file:
                    file.write(f"{username}:{username}@gmail.com:EzSnapByFrogyOnTop\n")
                    file.close()

                print(f"{Fore.LIGHTCYAN_EX}[#{threadId}] {Fore.LIGHTGREEN_EX}Account generated! {username}:{username}@gmail.com:EzSnapByFrogyOnTop")
                self.tLocker.release()
            else:
                self.tLocker.acquire()
                print(f"{Fore.LIGHTCYAN_EX}[#{threadId} - {register.status_code}] {Fore.LIGHTRED_EX}An error occured while generating this account. {username}:{username}@gmail.com:EzSnapByFrogyOnTop")
                self.tLocker.release()         

            self.generate(threadId)   
        except Exception as exception:
            self.tLocker.acquire()
            print(f"{Fore.LIGHTCYAN_EX}[#{threadId}] {Fore.LIGHTRED_EX}An error occured while generating an account - {exception}")
            self.tLocker.release()

            self.generate(threadId) 

    def manager(self):
        for i in range(self.config["threads"]):
            threading.Thread(target=self.generate, args=(i + 1,)).start()

        self.title(f"Generated - {self.generated}")

if __name__ == "__main__":
    try:
        EzSnap().manager()
    except KeyboardInterrupt:
        exit()