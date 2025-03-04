#!/usr/bin/env python3

import git

repo = git.Repo("/home/netman/Documents/network-automation")

print("current git status: ")
print(repo.git.status())

repo.index.add(["cpu_utilization.jpg", "router_data.txt"])
repo.git.add("--all")

repo.index.commit("updated cpu utilization and router data on network-automation repository")
repo.commit("changes successfully synced")

origin = repo.remote(name="origin")
origin.push()

print("changes updated to Github successfully!!")

