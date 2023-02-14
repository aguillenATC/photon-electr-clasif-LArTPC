import os
from git import Repo
from ..base import Syncer

class GithubSyncer(Syncer):

    def __init__(self, repo: dict, commit: dict, optional: dict):

        self.repo_params = repo
        self.commit_params = commit
        self.optional_params = optional
        self.__setup_repo()

    def __setup_repo(self) -> None:

        if "clone" in self.optional_params and self.optional_params["clone"]:

            username, token = os.environ.get("GITHUB_USERNAME"), os.environ.get("GITHUB_TOKEN")
            remote = f"https://{username}:{token}@github.com/{self.repo_params['repo_owner']}/{self.repo_params['repo_name']}.git"
            self.repo = Repo.clone_from(remote, self.repo_params["path_to_main"])

        else:

            self.repo = Repo(self.repo_params["path_to_main"],
                                  search_parent_directories = True)

    def __setup_default_file_list(self, repo: Repo) -> None:

        if not self.commit_params["file_list"]:

            repo_parent_dir_name: str = repo.working_dir.split("/")[-1]
            results_dir: str = self.results_path.split(repo_parent_dir_name)[-1]
            results_dir = results_dir[1:] if results_dir[0] == "/" else results_dir
            self.commit_params["file_list"] = results_dir

    def sync(self) -> None:

        repo: Repo = self.repo
        did_local_branch_exist: bool = self.__did_local_branch_exist(repo)
        did_remote_branch_exist: bool = self.__did_remote_branch_exist(repo)
        self.__setup_default_file_list(repo)

        self.__git_checkout(repo, did_local_branch_exist, did_remote_branch_exist)
        self.__git_pull(repo, did_remote_branch_exist)
        self.__git_add(repo)
        self.__git_commit(repo)
        self.__git_push(repo, did_remote_branch_exist)

        self.__return_to_previous_branch(repo)

    def __git_checkout(self, repo: Repo, did_local_branch_exist: bool, did_remote_branch_exist: bool) -> None:

        self.repo_params["previous_branch"] = repo.active_branch.name

        if did_local_branch_exist or did_remote_branch_exist:

            repo.git.checkout(self.commit_params["branch"])

        else:

            repo.git.checkout("-b", self.commit_params["branch"])

    def __git_pull(self, repo: Repo, did_remote_branch_exist: bool) -> None:

        if did_remote_branch_exist:

            origin = repo.remote(name = "origin")
            origin.pull()

    def __git_add(self, repo: Repo) -> None:

        repo.git.add(self.commit_params["file_list"])

    def __git_commit(self, repo: Repo) -> None:

        repo.index.commit(self.commit_params["message"])

    def __git_push(self, repo: Repo, did_remote_branch_exist: bool) -> None:

        if did_remote_branch_exist:

            origin = repo.remote(name = "origin")
            origin.push()

        else:

            repo.git.push("--set-upstream", "origin", self.commit_params["branch"])

    def __return_to_previous_branch(self, repo: Repo) -> None:

        if self.optional_params["return_to_previous_branch"]:

            repo.git.checkout(self.repo_params["previous_branch"])

    def __did_local_branch_exist(self, repo: Repo) -> bool:

        repo_branch_names = [ref.name for ref in repo.references]
        return self.commit_params["branch"] in repo_branch_names

    def __did_remote_branch_exist(self, repo: Repo) -> bool:

        repo_branch_names = [ref.name for ref in repo.references]
        remote_branch = "origin/" + self.commit_params["branch"]
        return remote_branch in repo_branch_names
