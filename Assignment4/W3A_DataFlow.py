import argparse
import logging
import os

def ParseW3A():

    return


def main():
    parser_args = argparse.ArgumentParser(description="Give a W3A file and either signed or reaching for analysis type (ex: python W3A_DataFlow.py prog_1.w3a reaching)")
    parser_args.add_argument("W3A_file", help="Path to the W3A file to analyze.")
    parser_args.add_argument("function",help="Type of flow function, either signed or reaching")
    return

main()