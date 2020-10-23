import sys
import requests
import zipfile

from io import BytesIO


def handle_art_url(artifact):
    r = requests.get(artifact,
                     headers={"Authorization": "token " + sys.argv[4]})
    if r.status_code == 200:
        zip = zipfile.ZipFile(BytesIO(r.content))
        patch = zip.open(sys.argv[1])
        print(
            '**Pull request modifies event listener templates**\n\n',
            '<details><summary>Difference (click to expand)</summary>\n\n```diff',
            sep='')
        print(patch.read().decode('utf-8'))
        print(
            '```\n</details>\n\n<details><summary>What? (click to expand)</summary>\n\n',
            'The Highlander documentation tool generates event listener examples from event specifications. ',
            'This comment contains the modifications that would be made to event ',
            'listeners for PR authors and reviewers to inspect for correctness and will ',
            'automatically be kept up-to-date whenever this PR is updated.</details>\n\n',
            '<!-- GHA-event-listeners-diff -->',
            sep='')
        # early exit
        sys.exit(0)


def main():
    url = sys.argv[2]
    r = requests.get(url)
    if r.status_code == 200:
        js = r.json()
        for art in js["artifacts"]:
            if art["name"] == sys.argv[1]:
                handle_art_url(art["archive_download_url"])
    sys.exit(1)


if __name__ == "__main__":
    main()
