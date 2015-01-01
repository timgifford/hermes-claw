import unittest
import datetime
import hook

class CommitContext(object):
    def __init__(self):
        self._parents = []
        self._description = ""

    def parents(self):
        return self._parents

    def description(self):
        return self._description

class FakeUI(object):

    def __init__(self):
        self.actualWarning = []

    def warn(self, message):
        self.actualWarning.append(message)


class CheckAllCommitsAreValidTest(unittest.TestCase):

    def setUp(self):
        self.goodCommit = CommitContext()
        self.goodCommit._description = "US12345 good stuff"

        self.badCommit = CommitContext()
        self.badCommit._description = "NO TICKET ID"

        self.ui = FakeUI()
    
    def testAllValidCommitsReturnsTrue(self):
        ui = object()
        repo = {1:self.goodCommit, 2:self.goodCommit}
        revrange = xrange(1,3)

        actual = hook.checkAllCommitsInRangeAreValid(ui,repo, revrange)

        self.assertTrue(actual)

    def testSingleInvalidCommitWarnsUser(self):
        repo = {1:self.badCommit}
        revrange = xrange(1,2)

        actual = hook.checkAllCommitsInRangeAreValid(self.ui,repo, revrange)

        self.assertFalse(actual)
        self.assertEqual(self.ui.actualWarning[0], "commit message:[NO TICKET ID] must start with a User Story or Defect Number, e.g. 'USxxxx' or 'DExxxx'\n")

    def testTwoInvalidCommitWarnsUserOnce(self):
        repo = {1:self.badCommit, 2:self.badCommit}
        revrange = xrange(1,3)

        actual = hook.checkAllCommitsInRangeAreValid(self.ui,repo, revrange)

        self.assertFalse(actual)
        self.assertEqual(self.ui.actualWarning[0], "commit message:[NO TICKET ID] must start with a User Story or Defect Number, e.g. 'USxxxx' or 'DExxxx'\n")
        self.assertEqual(len(self.ui.actualWarning), 1)

class IsValidCommitTest(unittest.TestCase):

    def setUp(self):
        # unittest.TestCase.setUp(self)
        self.commit = CommitContext()

    def testMergeCommitWithoutTicketIdIsValid(self):
        self.commit._parents = [1,3]

        self.assertTrue(hook.isValidCommit(self.commit))

    def testCommitWithoutTicketIdIsNotValid(self):
        self.commit._description = "Bad commit"

        self.assertFalse(hook.isValidCommit(self.commit))

    def testCommitStartingWithUSIsValid(self):
        self.commit._description = "US12345 good commit"

        self.assertTrue(hook.isValidCommit(self.commit))

    def testCommitStartingWithDEIsValid(self):
        self.commit._description = "DE12345 good commit"

        self.assertTrue(hook.isValidCommit(self.commit))

    def testCommitEndingWithUSIsNotValid(self):
        self.commit._description = "Bad commit US"

        self.assertFalse(hook.isValidCommit(self.commit))

def main():
    unittest.main()

if __name__ == '__main__':
    main()
