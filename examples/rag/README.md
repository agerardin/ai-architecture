# RAG

Provide grounded answers.

## Workflow

- get user query
- reformulate for best embedding
- embed and get similar documents
- rerank document based on pertinence
- evaluate credibility and rerank based  trustworthiness
  - provenance
  - common knowledge (beware)
  - knowldege base and symbolic logic
  - graph analysis
- check for fact overlap, consistency
  - leverage info to provide weighted answers
- summarize finding
  - provide trade-offs
  - give an overall confidence score

