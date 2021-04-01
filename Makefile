# MAKEFILE - GRAPH DRAWING

# Makefile for the GDW project.

#______________________________________________________________________________

# ------ VARIABLES ------ #

# Special variables.
.RECIPEPREFIX = >

# OS-dependant variables.
ifeq ($(OS),Windows_NT)
  RMPY := for /d /r . %%i in (*__pycache__*) do @rmdir /s /q "%%i"
else ifndef OS
  UNAME := $(shell uname -s)
  ifeq ($(UNAME),Linux)
    RMPY := find . -type d -name "__pycache__" -exec rm -rf {} +
  endif
endif

#______________________________________________________________________________

# ------ ALL ------ #

# Default target.
.PHONY: all
all: clean

#______________________________________________________________________________

# ------ TARGETS ------ #

# Delete all temporary files and directories.
.PHONY: clean
clean:
ifndef RMPY
>$(error Cannot clean due to unknown OS)
else
>$(RMPY)
endif

#______________________________________________________________________________
