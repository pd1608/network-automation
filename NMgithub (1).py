#!/usr/bin/env python3

'''SSH keys are already configured for this linux box with my github account. Hence github authentication is not required.
Also, /home/netman/Documents/network-automation directory is a clone of the network-automation repository. Hence, git init is performed automatically for this 
folder '''

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
