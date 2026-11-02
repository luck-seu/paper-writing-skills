"""views/ -- one module per machine view.

Each module owns one artifact under $PAPER_ROOT/.copilot/compiled/
and is a mechanical function of the sources (the verdict rule).
Views take their inputs from compile.py and core/; they never parse
each other's output. Modules are import-only -- the public interface
is compile.py.
"""
