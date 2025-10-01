# SQL_AGENT

## Goal

Build a agent that learn how to return data from free text queries.
Feedback loop so that we can reuse good queries.
Track statistics so we have a chance to improve them.

## Implementation Plan

1. Agent Inputs

DB schema: The agent needs access to the database schema (tables, columns, types, relationships).
User query: The natural language or raw SQL query from the user.
2. Query Normalization

Normalize or canonicalize queries so similar queries map to the same representation (for caching, similarity search, and deduplication).
3. Query Execution & Logging

Run the query against the database.
Log query, execution time, and results to a logging table.
4. Feedback Loop

Collect user feedback (happy/not happy).
If happy, persist the query to a catalog/cache for future reuse.
5. Query Catalog & Similarity Search

Store successful queries in a catalog.
When a new query comes in, check for similar queries using semantic or syntactic similarity (e.g., embedding search).
If a match is found, reuse or suggest the known query.
6. Popularity & Optimization

Track query usage frequency.
Optimize for popular queries (e.g., caching, indexing, pre-computation).
7. Workflow Example

Receive user query and schema.
Normalize query.
Check catalog for similar queries.
If found, reuse; if not, generate new query.
Execute query, log performance.
Return results.
Collect feedback.
If positive, persist query to catalog.
Tech Stack Suggestions

Use Pydantic for schema modeling.
Use a vector database (e.g., Qdrant, Pinecone) for similarity search.
Use SQLAlchemy for query execution and schema introspection.
Use a feedback table for logging user satisfaction.

## Implementation

Interaction of LLM agents and regular agents.
A central orchestrator can decide next steps or we can a fully decentralized architecture.