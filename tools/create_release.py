import sys

import requests


def create_release(token: str, repo: str, release: str, body: str):
    response = requests.post(f"https://api.github.com/repos/{repo}/releases",
                             headers={"Authorization": f"Bearer {token}"},
                             json={"tag_name": release, "name": release, "body": body})

    if response.status_code != 201:
        print(f"Failed to create release: {response.status_code} {response.text}", file=sys.stderr, flush=True)
        sys.exit(-1)


def main():
    try:
        token, repo, release, body_file = sys.argv[1:]
    except ValueError:
        print(f"Usage: python {sys.argv[0]} <token> <repo> <release> <body_file>", file=sys.stderr)
        sys.exit(-1)

    try:
        with open(body_file, 'r') as file:
            body = file.read()
    except (FileNotFoundError, IsADirectoryError):
        print(f"File not found: {body_file}", file=sys.stderr)
        sys.exit(-1)

    create_release(token, repo, release, body)


if __name__ == '__main__':
    main()
