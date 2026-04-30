import marimo

__generated_with = "0.23.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell
def _():
    def runs_in_molab() -> bool:
        """
        Heuristic to determine if we're running in the molab environment. 
        We want to do this because in the molab environment, the beancount file is not available, 
        and we will need to download it from github.
        """
        from pathlib import Path
    
        EXPECTED_IN_MOLAB_NAMES: set[str] = {
            "lock.txt",
            "notebook.py",
        } 

        cwd = Path.cwd()
        # List the names of the files and folders in the current directory
        found_names: set[str] = {p.name for p in cwd.iterdir()}

        return EXPECTED_IN_MOLAB_NAMES.issubset(found_names)

    runs_in_molab()
    return


@app.cell
def _():
    import json
    import urllib.request
    from pathlib import Path

    def _api_get(repo: str, path: str, branch: str) -> dict | list:
        """Fetch the GitHub Contents API response for a given repo path.

        Calls https://api.github.com/repos/{repo}/contents/{path}?ref={branch}.

        Args:
            repo:   Repository in 'owner/repo' form (e.g. 'octocat/Hello-World').
            path:   Path relative to the repository root (e.g. 'src/data' or 'README.md').
            branch: Branch, tag, or commit SHA to resolve the path against.

        Returns:
            A dict when the path points to a single file, or a list of dicts when
            the path points to a directory. Each dict contains at minimum the keys
            'name', 'path', 'type' ('file' | 'dir'), and 'download_url'.

        Raises:
            urllib.error.HTTPError: If the GitHub API returns a non-2xx status
                (e.g. 404 for a missing path or 403 for rate-limiting).
        """
        url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
        with urllib.request.urlopen(url) as resp:
            return json.loads(resp.read().decode())

    def _download(download_url: str, local_path: Path) -> None:
        """Download a single file from a URL and write it to a local path.

        Intermediate directories are created automatically if they do not exist.

        Args:
            download_url: Direct URL to the raw file content.
            local_path:   Destination path on the local filesystem. Any missing
                          parent directories are created with mkdir(parents=True).

        Raises:
            urllib.error.URLError: If the download URL is unreachable.
        """
        local_path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(download_url) as resp:
            local_path.write_bytes(resp.read())

    def _copy_item(repo: str, path: str, branch: str) -> None:
        """Recursively copy a file or directory from GitHub to the local filesystem.

        If *path* resolves to a file, that file is downloaded. If it resolves to a
        directory, all files inside it are downloaded recursively, preserving the
        directory structure relative to the repository root.

        Args:
            repo:   Repository in 'owner/repo' form.
            path:   Path to a file or directory relative to the repository root.
            branch: Branch, tag, or commit SHA to resolve the path against.
        """
        contents = _api_get(repo, path, branch)
        if isinstance(contents, dict):
            _download(contents["download_url"], Path(contents["path"]))
        else:
            for item in contents:
                if item["type"] == "file":
                    _download(item["download_url"], Path(item["path"]))
                elif item["type"] == "dir":
                    _copy_item(repo, item["path"], branch)

    def copy_data_from_github(repo: str, branch: str, data: list) -> None:
        """Copy files and/or directories from a GitHub repository to the local environment.

        Each entry in *data* may be a path to an individual file or to a directory.
        Directories are copied recursively. The local path structure mirrors the
        repository layout relative to the repository root.

        Args:
            repo:   Repository in 'owner/repo' form (e.g. 'octocat/Hello-World').
            branch: Branch to copy from (e.g. 'main').
            data:   List of file or directory paths relative to the repository root.

        Example:
            copy_data_from_github(
                repo="owner/myrepo",
                branch="main",
                data=["data/prices.csv", "config/"],
            )
        """
        for item in data:
            _copy_item(repo, item, branch)

    return (_api_get, _copy_item, _download, copy_data_from_github,)


if __name__ == "__main__":
    app.run()
