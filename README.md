---
title: Adaptive Shortlisting Env
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
---

# Adaptive Shortlisting Environment

An RL-compatible environment for sequential candidate shortlisting under uncertainty, modeling the process of identifying the optimal match within a large candidate pool through iterative evaluation and structured feedback.

## Overview
This project models candidate or student shortlisting as a sequential decision-making problem. Instead of a single-pass filter, the system uses an iterative approach where an agent selects a candidate, receives precise feedback, and uses that information to prune the search space for the next decision.

## Problem Statement
- **Massive Scale**: Organizations often face candidate pools of thousands or tens of thousands.
- **Limited Resources**: Human and computational evaluation rounds are expensive and limited.
- **Efficiency Gap**: Traditional filtering is often static; there is a need for adaptive systems that learn to eliminate large sections of the search space with minimal steps.

## Solution
The **Adaptive Shortlisting Environment** provides a framework for training agents to:
- Perform iterative shortlisting using structured feedback signals.
- Maximize information gain from every evaluation.
- Minimize the number of steps required to identify the target candidate through aggressive constraint-based elimination.

## Inspiration
While inspired by the mechanics of **Wordle** (using precise signals like Correct, Partial, and Incorrect), this project is **not a game**. It is a generalized constraint-based filtering system designed to solve high-stakes selection problems where every "guess" carries a cost.

## How It Works
The environment maps real-world shortlisting logic to a symbolic system:
- **Candidates**: Represented as symbolic tokens (currently words) in a searchable pool.
- **Action**: Selecting a specific candidate for evaluation.
- **Feedback**: A structured signal (Green/Yellow/Red) indicating how closely the selected candidate matches the target profile's attributes.
- **Filtering**: Automatically eliminating candidates from the pool that are mathematically inconsistent with the received feedback.

## Reinforcement Learning Framing
The environment follows the standard RL interaction loop:
- **State**: Current observation including `remaining_candidates`, `last_feedback`, `attempts`, and `candidate_ratio` (the current pool size relative to the start).
- **Action**: Selection of a candidate string from the available pool.
- **Reward**: Calculated as the **search space reduction**—the percentage of candidates eliminated in a single step. A terminal reward of `1.0` is given for finding the target.
- **Done**: Triggered when the correct candidate is identified or the maximum number of attempts is reached.

## Tasks
The environment includes three standardized tasks to measure agent scalability:
- **Easy**: Shortlist from a pool of 100 candidates.
- **Medium**: Shortlist from a pool of 1,000 candidates.
- **Hard**: Shortlist from the full dataset of over 12,000 candidates.

## Current Implementation
- **RL-Ready Environment**: The `ShortlistingEnv` class is fully compatible with sequential decision-making workflows.
- **Baseline Agent**: A heuristic-based solver is provided that utilizes filtering logic to consistently solve the tasks, serving as a benchmark for future RL models.

## How to Run
To run the environment across all tasks using the baseline agent and generate structured logs:
```bash
python inference.py
```

## Note
In the current implementation, candidates are represented as symbolic tokens (words) to maintain a fast, offline-first development loop. However, the system is designed to generalize to real-world vector-based or attribute-based candidate data.
