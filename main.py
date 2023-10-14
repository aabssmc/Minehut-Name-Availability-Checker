import aiohttp
import asyncio
from os import system
from typing import List


def write_good(arg: str) -> None:
    with open('good.txt', 'a', encoding='UTF-8') as f:
        f.write(f'{arg}\n')

def write_bad(arg: str) -> None:
    with open('bad.txt', 'a', encoding='UTF-8') as f:
        f.write(f'{arg}\n')

def write_invalid(arg: str) -> None:
    with open('invalid.txt', 'a', encoding='UTF-8') as f:
        f.write(f'{arg}\n')


class Checker:
    def __init__(self, usernames: List[str]):
        self.to_check = usernames

    async def _check(self, session: aiohttp.ClientSession, username: str) -> None:
        async with session.head(f'https://api.minehut.com/server/{username}?byName=true') as response:
            if len(username) > 3:
                if len(username) < 15:
                    if response.status == 200:
                        print(
                            '%s[UNAVAILABLE] %s%s'
                            % ('\u001b[31;1m', username, '\u001b[0m'),
                        )
                        write_bad(username)
                    else:
                        print(
                           '%s[AVAILABLE] %s%s'
                            % ('\u001b[32;1m', username, '\u001b[0m')
                        )
                        write_good(username)
                else:
                    print(
                        '%s[INVALID] %s%s'
                        % ('\u001b[30;1m', username, '\u001b[0m'),
                    )
                    write_invalid(username)
            else:
                print(
                    '%s[INVALID] %s%s'
                    % ('\u001b[30;1m', username, '\u001b[0m'),
                )
                write_invalid(username)

    async def start(self):
        print('Loading.. by @big.abs on discord')
        async with aiohttp.ClientSession() as sess:
            return await asyncio.gather(*[self._check(sess, u) for u in self.to_check])


if __name__ == '__main__':
    system('cls && title Minehut Name Checker by aabss')

    with open('names.txt', encoding='UTF-8') as f:
        username_list = [line.strip() for line in f]

    checker = Checker(username_list)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(checker.start())
    input('Complete! Press ENTER to exit')