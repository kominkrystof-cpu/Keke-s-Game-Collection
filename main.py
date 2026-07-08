#!/usr/bin/env python3
"""Main entry point for Keke's Game Collection."""
import curses
from menu import main


if __name__ == "__main__":
    curses.wrapper(main)
