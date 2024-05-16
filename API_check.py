import asyncio
import json

import aiohttp
import requests
from typing import TypedDict, Literal, Dict

import websockets

BASE_URL_LEET = 'https://leetcode-stats-api.herokuapp.com/'
BASE_URL_DRAGON = 'http://localhost:3001/api/warrior'
INTERVAL = 10  # sec


class Warrior(TypedDict):
    username: str
    easy: int
    medium: int
    hard: int


class LeetCodeResponse(TypedDict):
    status: Literal['success', 'failure']
    message: str
    totalSolved: int
    totalQuestions: int
    easySolved: int
    totalEasy: int
    mediumSolved: int
    totalMedium: int
    hardSolved: int
    totalHard: int
    acceptanceRate: float
    ranking: int
    contributionPoints: int
    reputation: int
    submissionCalendar: Dict[str, int]


def fetch_local_warriors() -> [Warrior]:
    return requests.get(BASE_URL_DRAGON).json()


async def fetch_user_data_from_leetcode(session: aiohttp.ClientSession, user: str) -> LeetCodeResponse | None:
    try:
        async with session.get(BASE_URL_LEET + user) as response:
            if response.status != 200:
                print(f'[ERROR] Failed to retrieve data for {user}: {response.status}, {await response.text()}')
                return None

            data = await response.json()
            if data.get('status') == 'error':
                print(f"[ERROR] {data['message']}")
            return data
    except aiohttp.ClientError as e:
        print(f'[ERROR] Client error for user {user}: {e}')
    except aiohttp.ContentTypeError as e:
        print(f'[ERROR] Failed to parse JSON response for user {user}: {e}')
    return None


async def process_warrior(session: aiohttp.ClientSession, warrior: Warrior):
    leet_code_data = await fetch_user_data_from_leetcode(session, warrior["username"])
    if leet_code_data is None:
        print("[WARRIOR] Failed to retrieve leet code for", warrior['username'])
        return
    print(leet_code_data)

    username = warrior["username"]
    increased = False
    if leet_code_data['easySolved'] > warrior['easy'] or True:
        print(f"Easy increased for {username}, {leet_code_data['easySolved']} > {warrior['easy']}")
        broadcast_easy_increase_msg(username, leet_code_data['easySolved'])
        increased = True
    if leet_code_data['mediumSolved'] > warrior['medium']:
        broadcast_medium_increase_msg(username, leet_code_data['mediumSolved'])
        print(f"Medium increased for {username} {leet_code_data['mediumSolved']} > {warrior['medium']}")
        increased = True
    if leet_code_data['hardSolved'] > warrior['hard']:
        broadcast_hard_increase_msg(username, leet_code_data['totalHard'])
        increased = True
        print(f"Hard increased for {username}, {leet_code_data['hardSolved']} > {warrior['hard']}")
    if not increased:
        print(f" Not increased for {username}")


CONNECTIONS = set()


async def repeatedly_check_changes(interval):
    async with aiohttp.ClientSession() as session:
        while True:
            if CONNECTIONS:
                warriors = fetch_local_warriors()
                tasks = [process_warrior(session, warrior) for warrior in warriors]
                r = await asyncio.gather(*tasks, return_exceptions=True)
            else:
                print("Skipping checks, no connections")
            await asyncio.sleep(interval)


async def ws_connect_handler(websocket):
    CONNECTIONS.add(websocket)
    print("Got a connection!", f"Now got {len(CONNECTIONS)} connection{'s' if len(CONNECTIONS) != 1 else ''}", websocket.id)
    try:
        await websocket.wait_closed()
    finally:
        print(f"Lost connection to {websocket.id}")
        CONNECTIONS.remove(websocket)


def broadcast_easy_increase_msg(username: str, new_easy: int) -> None:
    msg = {"type": "easy_increase", "data": {"username": username, "new_easy": new_easy}}
    msg = json.dumps(msg)
    message_all(msg)


def broadcast_medium_increase_msg(username: str, new_medium: int) -> None:
    msg = {"type": "medium_increase", "data": {"username": username, "new_medium": new_medium}}
    msg = json.dumps(msg)
    message_all(msg)


def broadcast_hard_increase_msg(username: str, new_hard: int) -> None:
    msg = {"type": "hard_increase", "data": {"username": username, "new_hard": new_hard}}
    msg = json.dumps(msg)
    message_all(msg)


def message_all(message: bytes | str):
    websockets.broadcast(CONNECTIONS, message)


async def main():
    async with websockets.serve(ws_connect_handler, "", 8001):
        await repeatedly_check_changes(INTERVAL)


if __name__ == '__main__':
    asyncio.run(main())
