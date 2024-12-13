# api id, hash
API_ID = 1488
API_HASH = 'abcde1488'

REF_LINK = 'https://t.me/dogshouse_bot/join?startapp=RRQUZbFUQTGTu0N5hAueeg'

DELAYS = {
    'ACCOUNT': [5, 15],  # delay between connections to accounts (the more accounts, the longer the delay)
    # 'TASK':  [5, 10],  # delay after complete task
    'FIRST_VISIT': [2, 5],  # delay after first visit request
    'ADDITION_TIME': [1000, 3000],  # addition time to next day check
}

# BLACKLIST_TASK = ['notcoin-tier-platinum', 'notcoin-tier-gold', 'join-blum-tribe', 'subscribe-dogs', 'add-bone-telegram']

PROXY = {
    "USE_PROXY_FROM_FILE": False,  # True - if use proxy from file, False - if use proxy from accounts.json
    "PROXY_PATH": "data/proxy.txt",  # path to file proxy
    "TYPE": {
        "TG": "socks5",  # proxy type for tg client. "socks4", "socks5" and "http" are supported
        "REQUESTS": "socks5"  # proxy type for requests. "http" for https and http proxys, "socks5" for socks5 proxy.
        }
}

# session folder (do not change)
WORKDIR = "sessions/"

# timeout in seconds for checking accounts on valid
TIMEOUT = 30