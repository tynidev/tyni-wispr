#!/usr/bin/env python3
"""
Compatibility script for tyni-wispr.py

This script maintains backward compatibility by importing and running 
the main function from the new modular structure.
"""

from tyni_wispr import main

if __name__ == "__main__":
    main()
