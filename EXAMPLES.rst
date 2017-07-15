
Project selection
=================
> Project must be selected before invoking commands, the state
> is stored in ~/.atlssn folder...

atlssn project <PROJECT_NAME>



Issues management
=================

atlssn issue create [-t|--type ] [-c|--components comp1,comp2,comp3] [-p|--priority blocker|critical|MAJOR|minor|trivial] [-s|--sprint <SPRINTID>] -s|--summary "SUMMARY"

atlssn issue modify <ISSUE_ID> [-c|--components comp1,comp2,comp3] [-p|--priority blocker|critical|minor|trivial] [-s|--sprint <SPRINTID>] -s|--summary "SUMMARY"

#
# Get complete status of the ticket including status in sprint,
# branches and their latest commits, 
#
atlssn issue status VFS-1234

atlssn issue resolve VFS-1234

atlssn issue create-branch VFS-1234 <REPO1> <REPO2> ...

atlssn issue progress [in-progress|resolved|closed]



Sprint management
=================

#
# By default returns the status of the current sprint
#
atlssn sprint status [<SPRINT_ID>] 

atlssn sprint start <SPRINT_ID>

atlssn sprint close <SPRINT_ID>



Code management
===============



Build management
================

atlssn build start <REPO_NAME> --plan <PLAN_ID> --issue <ISSUE_ID> --branch <BRANCH_ID>

atlssn build status <REPO_NAME> --plan <PLAN_ID> --issue <ISSUE_ID> --branch <BRANCH_ID>

atlssn build status 



Document management
===================



