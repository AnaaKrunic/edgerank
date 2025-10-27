# 🧠 EdgeRank Simulator

A console-based simulation of Facebook’s **EdgeRank algorithm**, implemented in **Python**.  
This project models how posts are ranked in a user’s feed based on **affinity**, **popularity**, and **time decay** — the three key factors of the original EdgeRank formula.

---

## 📘 Overview

The system simulates a simplified version of Facebook’s News Feed ranking.  
It loads data from CSV files (posts, users, reactions, friendships, etc.), computes personalized post rankings for each logged-in user, and allows **intelligent search** across all posts.

---

## ⚙️ Core Features

- 🧮 **EdgeRank computation**
  - User affinity (based on interactions)
  - Post popularity (reactions, shares, comments)
  - Time decay (recency of post)
- 👤 **User login and personalized feed**
- 🔍 **Search engine** for posts by one or multiple keywords
- 🗣️ **Phrase search** using quotation marks (`" "`)
- ✨ **Autocomplete** suggestions using Trie data structure
- 💾 **Serialization** of data structures for faster startup
- 🌐 **Graph representation** of users and their interactions

---

## 🧱 Data Files

The system uses a set of CSV files:

| File | Description |
|------|--------------|
| `statuses.csv` | Post metadata (text, author, date, reactions, etc.) |
| `comments.csv` | Comments on posts |
| `friends.csv` | User friendships |
| `reactions.csv` | Reactions to posts |
| `shares.csv` | Shares of posts |

> Provided datasets simulate real-world social interactions.

---

## 🧠 EdgeRank Formula

\[
Score = u<sub>i</sub> * w<sub>i</sub> * d<sub>i</sub>
\]

Where:
- **u** – user affinity toward the post author  
- **w** – content weight (popularity)  
- **d** – time decay factor  

Each parameter equally influences the post’s visibility score.

---

## 🧮 Implementation Highlights

- Python OOP design (classes for `User`, `Post`, `Graph`, `EdgeRank`, `SearchEngine`, `Trie`)  
- Efficient text search using **Trie**  
- Personalized feed generation using **graph traversal**  
- Modular design with focus on readability and extensibility  
- Data serialization for faster reloads  
