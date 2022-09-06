#!/bin/env python3

import logging
import subprocess

def exec_shell_command(command):
    """
    Execute shell command and return output as a string
    :param command:  1D array of strings e.g. ['ls', '-l']
    :return: output of command
    """
    logging.info(command)
    process = subprocess.run(command, stdout=subprocess.PIPE, universal_newlines=True)
    return process.stdout