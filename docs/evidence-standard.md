# Evidence standard

Every case must make an audit possible without relying on the annotator's authority.

## Required evidence

- Canonical source URL and source type
- Immutable revision: notebook version, commit SHA, release tag, or archived identifier
- File/cell and line or execution location
- Short code excerpt where redistribution is allowed
- Dataset/task documentation supporting the evaluation boundary
- Step-by-step information-flow explanation
- Confidence and impact labels with reasons
- Reproduction environment, command, seed, result, and date
- Correction with the smallest change that restores the boundary

## Impact provenance

- `measured`: the atlas independently ran a controlled leaky-versus-corrected comparison.
- `source_measured`: the primary source reports a controlled comparison that the atlas has verified statically but not rerun.
- `inferred`: the information path establishes risk, but no controlled magnitude is available.
- `unknown`: the available evidence does not support an impact direction.

Never present `source_measured` as an atlas reproduction.

## Safe wording

Describe observable behavior: “the scaler is fitted on the full matrix before the split.” Avoid claims about an author's motives, competence, or production system.

Use `probable` or `ambiguous` when a necessary fact is missing. Do not turn uncertainty into certainty through confident prose.

## Source preservation

Prefer a commit permalink, notebook version URL, DOI, or web archive. Do not copy entire notebooks or datasets into this repository. Small excerpts must be necessary for analysis and retain attribution.

## Reproduction outcomes

- `reproduced`: original behavior and boundary violation were observed.
- `partially_reproduced`: the information path was executed, but the full metric comparison was not.
- `static_verified`: code and data semantics establish the path without a rerun.
- `not_reproduced`: a documented attempt failed.
- `not_attempted`: no execution attempt has been made.
