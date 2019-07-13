from pygit2 import Repository

def get_branch():
    """ """
    branch = Repository('.').head.shorthand
    return branch

def get_repo_name():
    """ """
    repo_url = Repository('.').remotes['origin'].url
    return repo_url.split('/')[-1]
