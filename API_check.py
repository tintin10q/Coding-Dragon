import asyncio
import json

import aiohttp
import requests
from typing import TypedDict, Literal, Dict

import websockets

import sqlite3

BASE_URL_LEET = 'https://leetcode-stats-api.herokuapp.com/'
BASE_URL_DRAGON = 'http://localhost:3000/api/warrior'
BASE_URL_DRAGON_PING = 'http://localhost:3000/api/ping'
INTERVAL = 20  # sec


class Warrior(TypedDict):
    username: str
    easy: int
    medium: int
    hard: int
    start_easy: int
    start_medium: int
    start_hard: int


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

    username = warrior["username"]
    damage = 0

    if leet_code_data['easySolved'] > warrior['start_easy']:
        damage += leet_code_data['easySolved'] - warrior['start_easy']
    if leet_code_data['mediumSolved'] > warrior['start_medium']:
        damage += (leet_code_data['mediumSolved'] - warrior['start_medium']) * 3
    if leet_code_data['hardSolved'] > warrior['start_hard']:
        damage += (leet_code_data['hardSolved'] - warrior['start_hard']) * 10
    if damage > 0:
        broadcast_damage_msg(username, damage)
    db = None
    if leet_code_data['easySolved'] > warrior['easy']:
        print("Updating easy for",username)
        db = sqlite3.connect("_dragon.sqlite") if db is None else db
        db.execute("update warrior set easy = ? where username = ? ", (leet_code_data['easySolved'], username))
        db.commit()
    if leet_code_data['mediumSolved'] > warrior['medium']:
        print("Updating medium for", username)
        db = sqlite3.connect("_dragon.sqlite") if db is None else db
        db.execute("update warrior set medium = ? where username = ? ", (leet_code_data['mediumSolved'], username))
        db.commit()
    if leet_code_data['hardSolved'] > warrior['hard']:
        print("Updating hard for", username)
        db = sqlite3.connect("_dragon.sqlite") if db is None else db
        db.execute("update warrior set hard = ? where username = ? ", (leet_code_data['hardSolved'], username))
        db.commit()


CONNECTIONS = set()


async def repeatedly_check_changes(interval):
    async with aiohttp.ClientSession() as session:
        while True:
            if CONNECTIONS:
                warriors = fetch_local_warriors()
                print("Got ", len(warriors), "warrior", warriors)
                if warriors:
                    tasks = [process_warrior(session, warrior) for warrior in warriors if "username" in warrior]
                    r = await asyncio.gather(*tasks, return_exceptions=True)
                else:
                    print("Skipping checks, no warriors")
            else:
                print("Skipping checks, no connections")
            print("Waiting", interval, "seconds", end=", ", flush=True)
            await asyncio.sleep(interval)
            print("Waited", interval, "seconds")


async def ws_connect_handler(websocket):
    CONNECTIONS.add(websocket)
    print("Got a connection!", f"Now got {len(CONNECTIONS)} connection{'s' if len(CONNECTIONS) != 1 else ''}", websocket.id)
    try:
        await websocket.wait_closed()
    finally:
        print(f"Lost connection to {websocket.id}")
        CONNECTIONS.remove(websocket)


def broadcast_damage_msg(username: str, amount: int) -> None:
    msg = {"type": "damage", "data": {"username": username, "damage": amount}}
    msg = json.dumps(msg)
    message_all(msg)

def message_all(message: bytes | str):
    websockets.broadcast(CONNECTIONS, message)


async def main():
    async with websockets.serve(ws_connect_handler, "", 9000):
        await repeatedly_check_changes(INTERVAL)


if __name__ == '__main__':
    if not requests.get(BASE_URL_DRAGON_PING).ok:
        print(f"Could not reach {BASE_URL_DRAGON_PING} :()")
        exit(1)
    else:
        print("Connected to the dragon!")
    asyncio.run(main())
