# Bolt's Journal - Critical Learnings Only

This journal contains critical learnings to avoid mistakes or make better decisions.

## 2025-05-14 - [Initial Entry]
**Learning:** Initializing the Bolt journal to track performance-related learnings in the Multi-Layer Research Agent.
**Action:** Always check this file before starting new optimizations.

## 2025-05-14 - Order Preservation in Parallel Stages
**Learning:** Using `as_completed()` with `ThreadPoolExecutor` in Stages 2, 3, and 4 is a performance anti-pattern in this codebase. While it allows processing as tasks finish, it scrambles document relevance (Stage 2/4) and text chunk chronology (Stage 3). Scrambled chunks lead to poor synthesis, which triggers expensive regeneration loops in Stage 7/8.
**Action:** Always iterate over futures in submission order when parallelizing stages that depend on relevance or chronological sequence.
