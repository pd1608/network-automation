#!/usr/bin/env python3

import git




repo = git.Repo("/home/netman/Documents/network-automation")

print("current git status: ")


#repo.index.add(["cpu_utilization.jpg", "router_data.txt"])

repo.git.add('--all')
print(repo.git.status())

repo.index.commit("Updated CPU utilization and router data on network-automation repository")
print("pushing changes to network-automation repo")

origin = repo.remote(name="origin")
origin.push()

print("Changes updated to GitHub successfully!!")
