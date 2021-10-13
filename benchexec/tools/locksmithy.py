# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import benchexec.tools.template
import benchexec.result as result

import re


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for Locksmith.
    URL: http://www.cs.umd.edu/projects/PL/locksmith
    """

    def executable(self, tool_locator):
        return tool_locator.find_executable("locksmith")

    def version(self, executable):
        return self._version_from_tool(executable, line_prefix="Cil version: ")

    def name(self):
        return "Locksmith"

    def cmdline(self, executable, options, task, rlimits):
        return [executable, *options, *task.input_files]

    def determine_result(self, run):
        status = result.RESULT_ERROR
        if run.output:
            if any("Possible data race" in s for s in run.output):
                status = result.RESULT_UNKNOWN
            elif any("Fatal error" in s for s in run.output):
                status = result.RESULT_ERROR
            else:
                status = result.RESULT_TRUE_PROP
        return status
