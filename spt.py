import sys
import getpass

import spotify

async def main():
    playlist_uri = input("playlist_uri: ")
    client_id = input("client_id: ")
    secret = getpass.getpass("application secret: ")
    token = getpass.getpass("user token: ")

    async with spotify.Client(client_id, secret) as client:
        user = await spotify.User.from_token(client, token)

        async for playlist in user:
            if playlist.uri == playlist_uri:
                return await playlist.sort(reverse=True, key=(lambda track: track.popularity))

        print('No playlists were found!', file=sys.stderr)

if __name__ == '__main__':
    client.loop.run_until_complete(main())