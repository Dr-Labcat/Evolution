# Implementation Summary

This project implements a compact terminal version of the Evolution rules.

Key points:
- Card play, feeding, carnivore attacks, extinction, and scoring are implemented.
- FAT TISSUE stores food and can be consumed to avoid starvation.
- Feeding rounds enforce trait behavior (GRAZING, COOPERATION, etc.).
- Scoring: surviving species, traits, parasites, and collected food are counted.

Removed items:
- The simulation harness and event logging were removed per user request.

Next steps (optional):
- Audit trait implementations and add unit tests for coverage.
- Tidy code comments and improve test cases if desired.
