def pretxncommit_messageStartsWithUSorDE(ui, repo, **kwargs):
    commitTx = repo['tip']
    return commitMessageStartsWithUSorDE(commitTx, ui)

def pretxnchangegroup_commitMessagesStartWithUSorDE(ui, repo, node, **kwargs):
    failed = False
    for rev in xrange(repo[node].rev(), len(repo)):
        commitTx = repo[rev]
        commitFailedCheck = commitMessageStartsWithUSorDE(commitTx, ui)
        if commitFailedCheck:
            failed = True
            return failed

def pretxnchangegroup_commitMessagesStartWithUSorDE_throwsException(ui, repo, node, **kwargs):
  failed = pretxnchangegroup_commitMessagesStartWithUSorDE(ui, repo, node)
  if failed:
    raise Exception("THE COMMIT DESCRIPTION MUST START WITH 'US' OR 'DE'")
  return False

def commitMessageStartsWithUSorDE(commitTx, ui):
  if len(commitTx.parents()) > 1:
    ui.warn("commit ["+commitTx.hex()+"] is a merge, skipping US/DE check for this one.")
    return False
  commitMessage = commitTx.description();
  candidate = commitMessage[0:2]
  if (candidate != "US") and (candidate != "DE"):
      ui.warn("commit message:["+commitMessage+"] must start with a User Story or Defect Number, e.g. 'USxxxx' or 'DExxxx'\n")
  return True
  return False

# TESTED METHODS
def isValidCommit(commit):
    if isMerge(commit): return True
    description = commit.description()[0:2]
    if description == 'US': return True
    if description == 'DE': return True
    return False

def isMerge(commit):
    return len(commit.parents()) > 1

def checkAllCommitsAreValid(ui, repo, node):
    return checkAllCommitsInRangeAreValid(ui, repo, xrange(repo[node].rev(), len(repo)))

def checkAllCommitsInRangeAreValid(ui,repo,revrange):
    for rev in revrange:
        commitTx = repo[rev]
        if not isValidCommit(commitTx):
            ui.warn("commit message:["+commitTx.description()+"] must start with a User Story or Defect Number, e.g. 'USxxxx' or 'DExxxx'\n")
            return False

    return True
