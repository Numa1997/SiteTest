"""The Electron Beam, from Tip to Measurement: the Python reference solver.

A readable NumPy re-implementation of each chapter's browser solver (physics/chNN.js), written from the same equations, so
that the two can be compared on the same inputs (checks/check_parity.py). One module per chapter, ref/chNN.py, each with

    INPUTS, OUTPUTS            the contract symbols it reads and writes (contract.json)
    compute(p) -> dict         SI in, SI out, no side effects

and ref/core.py with the constants, unit factors and the number formatter the build uses for every number in the text.
"""
