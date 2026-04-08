---
title: Adaptive Shortlisting Env
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
---
LIVE DEMO = [https://huggingface.co/spaces/avanti29/adaptive-shortlisting-env]
# Adaptive Shortlisting Environment

An interactive system that models candidate shortlisting as a **sequential decision-making process**, efficiently reducing large candidate pools using structured feedback.

---

## 🚀 Live Demo
Select a difficulty level and run the simulation to watch how the system progressively eliminates candidates step-by-step.

---

## 🧠 What This Does

Instead of filtering candidates in a single pass, this system:

- Evaluates one candidate at a time  
- Uses structured feedback to eliminate inconsistent candidates  
- Rapidly reduces the search space  
- Identifies the optimal candidate in minimal steps  

---

## ⚡ Why This Matters

Real-world systems often face:
- Thousands of candidates  
- Limited evaluation resources  
- Expensive decision-making steps  

This approach enables:
- Faster shortlisting  
- Reduced computational and human cost  
- Smarter, adaptive filtering strategies  

---

## 🎮 Interactive Simulation

- Choose difficulty: **Easy / Medium / Hard**
- Run the agent
- Observe:
  - Step-by-step candidate selection  
  - Search space reduction  
  - Final efficiency score  

---

## 🧩 Key Concepts

- **Step** → One evaluation round (one candidate tested)  
- **Feedback** → Signal used to eliminate candidates  
- **Adaptive Filtering** → Dynamically shrinking the pool  
- **Final Score** → Measures overall efficiency  

---

## ⚙️ How It Works

The system maps shortlisting into a structured environment:

- **Candidates** → Represented as symbolic tokens (words)  
- **Action** → Selecting a candidate  
- **Feedback** → Green / Yellow / Red signals  
- **Filtering** → Eliminates inconsistent candidates  

---

## 🤖 Reinforcement Learning Framing

- **State** → Remaining candidates + history  
- **Action** → Candidate selection  
- **Reward** → Reduction in search space  
- **Goal** → Maximize information gain per step  

---

## 📊 Tasks

- **Easy** → ~100 candidates  
- **Medium** → ~1,000 candidates  
- **Hard** → ~12,000+ candidates  

---

## 🛠️ Current Implementation

- RL-compatible environment (`ShortlistingEnv`)  
- Baseline agent for demonstration  
- Interactive web interface using FastAPI  

---

## ▶️ Run Locally

```bash
python inference.py
