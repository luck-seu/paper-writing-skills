"""core/ -- view-agnostic machinery of the state compiler.

One job per module, no view knowledge: texscan (reading the .tex
sources), mathmode (math segmentation + tokens), macromap
(macro-source files -> definitions + classification), copilot
(.copilot/ output + diagnostics). Views live in views/; nothing
here imports from there.
Modules are import-only -- the public interface is compile.py.
"""
