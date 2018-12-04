# @file VersionAggregator facilitates the collection of information
# regarding the tools, binaries, submodule configuration used in a build
#
##
# Copyright (c) 2017, Microsoft Corporation
#
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##
import copy
import logging
from enum import Enum

VERSION_AGGREGATOR = None


class VersionAggregator(object):
    def __init__(self):
        super(VersionAggregator, self).__init__()
        self.Versions = {}

    def ReportVersion(self, key, value, versionType):
        """
        Report the version of something.

        key -- The name of what you are reporting.
        value -- The value of what you are reporting.
        versionType -- The method of categorizing what is being reported. See VersionTypes for details.
        """
        if key in self.Versions:
            if self.Versions[key]["version"] == value:
                logging.warning("VersionAggregator: This {0}:{1} key/value pair was already registered".format(key, value))
            else:
                error = "VersionAggregator: {0} key registered with a different value\n\tOld:{1}\n\tNew:{2}".format(key, self.Versions[key]["version"], value)
                logging.error(error)
                raise Exception(error)
            return

        self.Versions[key] = {
            "name": key,
            "version": value,
            "type": versionType.name
        }
        logging.debug("VersionAggregator logging version: {0}".format(str(self.Versions[key])))

    def GetAggregatedVersionInformation(self):
        """
        Returns a copy of the aggregated information.
        """
        return copy.deepcopy(self.Versions)


class VersionTypes(Enum):
    """
    COMMIT is for the commit hash of a repository.
    BINARY is for a pre-packaged binary that is distributed with a version number.
    TOOL is for recording the version number of a tool that was used during the build process.
    INFO is for recording miscellanious information.
    """
    TOOL = 1
    COMMIT = 2
    BINARY = 3
    INFO = 4


def GetVersionAggregator():
    """
    Returns a singleton instance of this class for global use.
    """
    global VERSION_AGGREGATOR

    if VERSION_AGGREGATOR is None:
        logging.debug("Setting up version aggregator")
        VERSION_AGGREGATOR = VersionAggregator()

    return VERSION_AGGREGATOR
