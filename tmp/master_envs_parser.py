#! /usr/bin/env python3
# coding = utf-8

import os

# Exceptions
class JenkinsEnvironsMissing(Exception):
    pass

class Envs():

    must_envs = ["MAPS", "FILTER", "PLATFORM", "FW_VERSION", "FW_IMAGE_PATH"]

    def __init__(self):
        self.maps_done = False
        self.filter_done = False
        self.strip_and_export()

    def show(self):
        print("""
    === [Beg] All Envs Provided by User ===

[MAPS]
{MAPS}

[FILTER]
{FILTER}

[PLATFORM]
{PLATFORM}

[FW_VERSION]
{FW_VERSION}

[FW_IMAGE_PATH]
{FW_IMAGE_PATH}

    === [End] All Envs Provided by User ===
        """.format(**self.envs))
        pass

    def strip_and_export(self):
        """
        Strip and Export Jenkins envs strings.
        After that, save the envs in local
        """
        self.envs = {}
        try:
            for e in Envs.must_envs:
                self.envs[e] = os.environ[e] = os.environ[e].strip()
        except KeyError as e:
            e.args
            raise JenkinsEnvironsMissing("Please check your jenkins job configuration, confirm some envs missing.")

    def deal_maps(self):
        self.cases_maps = None
        pass

    def deal_filter(self):
        self.cases_filter = None
        pass

    @property
    def maps(self):
        if self.maps_done == True:
            return self.cases_maps
        else:
            self.deal_maps()
            self.maps_done = True
            return self.cases_maps

    @property
    def filter(self):
        if self.filter_done == True:
            return self.cases_filter
        else:
            self.deal_filter()
            self.filter_done = True
            return self.cases_filter

    @property
    def fw_image_path(self):
        return self.envs["FW_IMAGE_PATH"]

    @property
    def fw_version(self):
        return self.envs["FW_VERSION"]

    @property
    def platform(self):
        return self.envs["PLATFORM"]


def get_envs():
    return Envs()

if __name__ == "__main__":
    e = Envs()
    e.strip_and_export()
    e.show()
    os.environ["PLATFORM"] = "MMM"
    pass
