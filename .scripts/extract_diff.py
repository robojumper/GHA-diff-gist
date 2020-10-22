import sys
import requests
import zipfile

from io import BytesIO

def handle_art_url(artifact):
    r = requests.get(artifact, headers={"Authorization": "token " + sys.argv[4]})
    if r.status_code == 200:
        zip = zipfile.ZipFile(BytesIO(r.content))
        patch = zip.open(sys.argv[1])
        print('**Workflow failed because Compiletest file needs changes**\n\n')
        print('<details><summary>Patch (click to expand)</summary>\n\n```patch')
        print(patch.read().decode('utf-8'))
        print('```\n</details>\n\n<details><summary>What? (click to expand)</summary>\n\n')
        print('The repository contains some test files to verify that event listeners are documented correctly.')
        print('If you changed any event documentation, the event listener dump needs to be updated.')
        print('The documentation tool has determined that the above changes are needed to update the event listener dump; ')
        print('alternatively you can download the patch file from the [failed run page](' + sys.argv[3] + ') as an artifact ')
        print('or run the `makeDocs` task locally to update the file.</details>')
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