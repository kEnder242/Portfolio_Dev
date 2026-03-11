# Specification: Multi-Vector Acquisition [SPR-11-RECRUITER]

## 1. Requirement: Headless Browser Node
- Implementation: `src/nodes/browser_node.py` using Playwright.
- Protocol: FastMCP tool provider.
- Tool: `browse_url(url: str) -> str`.
- Output: Cleaned text or markdown representation of the page content.

## 2. Requirement: Verified Discovery
- The Recruiter must not report any URL that has not been successfully processed by the Browser Node.
- Discard: 404s, login redirects, empty content.

## 3. Requirement: Multi-Vector Semantic Scoring
- Use `team_signatures.json` as the definition of truth for "Job Buckets".
- Scoring Pass: Task the Sovereign Brain (4090) with analyzing the JD text.
- Alignment Mapping: Map the JD requirements to specific project anchors (e.g. VISA, Aurora) found in the Rank 4 gems.

## 4. Requirement: Bucket-Aware Reporting
- Group listings by Team Signature Bucket in the final markdown brief.
- Provide a "Lead Engineer Match" summary for every job.
