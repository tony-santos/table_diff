class OutputChecker:
    """
    A class used to check the whether the actual output from a doctest
    example matches the expected output.  `OutputChecker` defines two
    methods: `check_output`, which compares a given pair of outputs,
    and returns true if they match; and `output_difference`, which
    returns a string describing the differences between two outputs.
    """
    def check_output(self, want, got, optionflags):
        """
        Return True iff the actual output from an example (`got`)
        matches the expected output (`want`).  These strings are
        always considered to match if they are identical; but
        depending on what option flags the test runner is using,
        several non-exact match types are also possible.  See the
        documentation for `TestRunner` for more information about
        option flags.
        """
        # Handle the common case first, for efficiency:
        # if they're string-identical, always return true.
        if got == want:
            return True

        # The values True and False replaced 1 and 0 as the return
        # value for boolean comparisons in Python 2.3.
        if not (optionflags & DONT_ACCEPT_TRUE_FOR_1):
            if (got,want) == ("True\n", "1\n"):
                return True
            if (got,want) == ("False\n", "0\n"):
                return True

        # <BLANKLINE> can be used as a special sequence to signify a
        # blank line, unless the DONT_ACCEPT_BLANKLINE flag is used.
        if not (optionflags & DONT_ACCEPT_BLANKLINE):
            # Replace <BLANKLINE> in want with a blank line.
            want = re.sub('(?m)^%s\s*?$' % re.escape(BLANKLINE_MARKER),
                          '', want)
            # If a line in got contains only spaces, then remove the
            # spaces.
            got = re.sub('(?m)^\s*?$', '', got)
            if got == want:
                return True

        # This flag causes doctest to ignore any differences in the
        # contents of whitespace strings.  Note that this can be used
        # in conjunction with the ELLIPSIS flag.
        if optionflags & NORMALIZE_WHITESPACE:
            got = ' '.join(got.split())
            want = ' '.join(want.split())
            if got == want:
                return True

        # The ELLIPSIS flag says to let the sequence "..." in `want`
        # match any substring in `got`.
        if optionflags & ELLIPSIS:
            if _ellipsis_match(want, got):
                return True

        # We didn't find any match; return false.
        return False

    # Should we do a fancy diff?
    def _do_a_fancy_diff(self, want, got, optionflags):
        # Not unless they asked for a fancy diff.
        if not optionflags & (REPORT_UDIFF |
                              REPORT_CDIFF |
                              REPORT_NDIFF):
            return False

        # If expected output uses ellipsis, a meaningful fancy diff is
        # too hard ... or maybe not.  In two real-life failures Tim saw,
        # a diff was a major help anyway, so this is commented out.
        # [todo] _ellipsis_match() knows which pieces do and don't match,
        # and could be the basis for a kick-ass diff in this case.
        ##if optionflags & ELLIPSIS and ELLIPSIS_MARKER in want:
        ##    return False

        # ndiff does intraline difference marking, so can be useful even
        # for 1-line differences.
        if optionflags & REPORT_NDIFF:
            return True

        # The other diff types need at least a few lines to be helpful.
        return want.count('\n') > 2 and got.count('\n') > 2

    def output_difference(self, example, got, optionflags):
        """
        Return a string describing the differences between the
        expected output for a given example (`example`) and the actual
        output (`got`).  `optionflags` is the set of option flags used
        to compare `want` and `got`.
        """
        want = example.want
        # If <BLANKLINE>s are being used, then replace blank lines
        # with <BLANKLINE> in the actual output string.
        if not (optionflags & DONT_ACCEPT_BLANKLINE):
            got = re.sub('(?m)^[ ]*(?=\n)', BLANKLINE_MARKER, got)

        # Check if we should use diff.
        if self._do_a_fancy_diff(want, got, optionflags):
            # Split want & got into lines.
            want_lines = want.splitlines(True)  # True == keep line ends
            got_lines = got.splitlines(True)
            # Use difflib to find their differences.
            if optionflags & REPORT_UDIFF:
                diff = difflib.unified_diff(want_lines, got_lines, n=2)
                diff = list(diff)[2:] # strip the diff header
                kind = 'unified diff with -expected +actual'
            elif optionflags & REPORT_CDIFF:
                diff = difflib.context_diff(want_lines, got_lines, n=2)
                diff = list(diff)[2:] # strip the diff header
                kind = 'context diff with expected followed by actual'
            elif optionflags & REPORT_NDIFF:
                engine = difflib.Differ(charjunk=difflib.IS_CHARACTER_JUNK)
                diff = list(engine.compare(want_lines, got_lines))
                kind = 'ndiff with -expected +actual'
            else:
                assert 0, 'Bad diff option'
            # Remove trailing whitespace on diff output.
            diff = [line.rstrip() + '\n' for line in diff]
            return 'Differences (%s):\n' % kind + _indent(''.join(diff))

        # If we're not using diff, then simply list the expected
        # output followed by the actual output.
        if want and got:
            return 'Expected:\n%sGot:\n%s' % (_indent(want), _indent(got))
        elif want:
            return 'Expected:\n%sGot nothing\n' % _indent(want)
        elif got:
            return 'Expected nothing\nGot:\n%s' % _indent(got)
        else:
            return 'Expected nothing\nGot nothing\n'

