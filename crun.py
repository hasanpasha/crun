#!/usr/bin/python

"""
Compile & run c&c++ file.
"""

from argparse import ArgumentParser
import subprocess
import os
import logging


LOGGING_FORMAT = "[%(levelname)s] %(message)s"
LOGGING_DEFAULT_LEVEL = 0

def main():
	"""Start the script."""
	args = get_args()
	filename = args.file_name
	cmd_args=args.cmd_args
	logging_level = args.verbose_level

	set_logging_config(logging_level)

	try:
		if not compile(filename):
			exit(1)
		
		if not run(get_exec_name(filename), *(cmd_args)):
			exit(2)
	
	except KeyboardInterrupt:
		exit(3)

def set_logging_config(level: int = LOGGING_DEFAULT_LEVEL):
	"""Set logging config"""
	logging.basicConfig(format=LOGGING_FORMAT, level=level)


def get_args() -> list:
	"""Get user command arguments."""

	parser = ArgumentParser(description="Compile & run c&c++ file.")
	parser.add_argument("file_name", metavar="filename", type=str,
			help="The name of the file you want to run.")
	parser.add_argument("--cmd-args", "-ca", metavar="cmd_args", 
				type=str, nargs="+", default=[],
				help="pass executable command arguments.")
	parser.add_argument("-vl", "--verbose-level", type=int,
		default=LOGGING_DEFAULT_LEVEL, help="set the level of logging.")

	args = parser.parse_args()

	return args

def run_cmd(cmd: list) -> bool:
	"""Run commands."""
	logging.info(" ".join(cmd))
	exit_code = subprocess.run(cmd).returncode

	if (exit_code != 0):
		logging.error(f"Error in executing command `{' '.join(cmd)}`."
			+ f" exit code is {exit_code}")
		return False
	return True

def get_exec_name(filename: str) -> bool:
	"""Get the executable file name."""
	return filename.split('.')[0]

def compile(filename: str) -> bool:
	"""Compile and build the executable."""
	exec_name = get_exec_name(filename)
	cmd = ["make", exec_name]
	return run_cmd(cmd)
	

def run(exec_name: str, *cmd_args) -> bool:
	"""Run the executable."""
	if not is_executable(exec_name):
		logging.error(f"{exec_name} is not executable.")
		return
	
	if "/" in exec_name:
		cmd = [exec_name]
	
	else:
		cmd = [f"./{exec_name}"] + list(cmd_args)

	return run_cmd(cmd)

def is_executable(exec_name: str):
	"""Check whether the file is executable or not."""
	return os.access(exec_name, os.X_OK)


if __name__ == '__main__':
	main()