# Adaptive Shortlisting Environment

A reinforcement learning environment for sequential candidate shortlisting under uncertainty, inspired by constraint-based feedback systems such as Wordle.

## Overview

This project is inspired by the mechanics of a Wordle-solving system, where iterative guesses and structured feedback are used to progressively narrow down possible solutions.

Building on this idea, the project generalizes the approach into a real-world shortlisting framework, where an agent selects candidates, receives evaluation feedback, and efficiently reduces the search space to identify the optimal match.

The goal is to train an agent to:
- Make informed sequential decisions
- Maximize information gain from feedback
- Identify the correct candidate in minimal steps

## Inspiration

The core inspiration comes from Wordle-style feedback mechanisms:
- **Iterative selection process**: Making successive attempts to find the target.
- **Structured feedback signals**: Receiving precise signals (correct / partial / incorrect) about each attempt.
- **Constraint-based elimination**: Using feedback to rapidly prune the search space of possibilities.

These principles are widely applicable beyond games and form the foundation of this environment.

## Extension to Real-World Problems

The project reframes this mechanism as a candidate shortlisting problem, commonly seen in:
- **Hiring and resume filtering**: Efficiently identifying the best candidate from a large pool.
- **Student selection systems**: Matching students to programs based on iterative evaluations.
- **Search and recommendation engines**: Refining results based on user interactions.
- **Diagnostic decision-making**: Narrowing down possibilities through sequential testing.
