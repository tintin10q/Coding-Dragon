import asyncio
import aiohttp

BASE_URL = 'https://leetcode-stats-api.herokuapp.com/'
usernames = ["quintunit"]

async def fetch_user_data(session, user):
    try:
        async with session.get(BASE_URL + user) as response:
            if response.status != 200:
                print(f'[ERROR] Failed to retrieve data for {user}: {response.status}')
                return None

            data = await response.json()
            if data.get('status') == 'error':
                print(f"[ERROR] {data['message']}")
            else:
                print(data['status'])
            return data
    except aiohttp.ClientError as e:
        print(f'[ERROR] Client error for user {user}: {e}')
    except aiohttp.ContentTypeError as e:
        print(f'[ERROR] Failed to parse JSON response for user {user}: {e}')
    return None

async def repeatedly_check_changes(users, timeout):
    async with aiohttp.ClientSession() as session:
        while True:
            if not users:
                print('[WARNING] No users added to track')
            else:
                tasks = [fetch_user_data(session, user) for user in users]
                r = await asyncio.gather(*tasks)
                print(r)
            await asyncio.sleep(timeout)

async def main():
    await repeatedly_check_changes(usernames, 5)

if __name__ == '__main__':
    asyncio.run(main())