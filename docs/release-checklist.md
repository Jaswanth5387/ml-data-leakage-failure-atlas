# Release checklist

Use this sequence for the `v0.1.0` archive. Do not create a DOI placeholder.

## Before publishing

- [ ] Confirm the creator name in `CITATION.cff` and `.zenodo.json` is the name that should appear in citations.
- [ ] Confirm the repository is enabled in the Zenodo GitHub integration before creating the GitHub release.
- [ ] Confirm `main` contains the complete reviewed corpus and has no open release-blocking corrections.
- [ ] Run `python scripts/validate_cases.py`.
- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Run `python scripts/check_release.py 0.1.0`.
- [ ] Confirm the GitHub Actions checks pass on the release-preparation pull request.

## Publish

1. Merge the release-preparation pull request into `main`.
2. Create a GitHub release from `main` with tag `v0.1.0` and title `ML Data Leakage Failure Atlas v0.1.0`.
3. Use [`release-notes-v0.1.0.md`](release-notes-v0.1.0.md) as the GitHub release notes.
4. Confirm the tag-triggered `Validate release` workflow passes.
5. Confirm Zenodo archives the release and creates the record.

## After Zenodo archives the release

- [ ] Check the title, version, creator, dataset type, CC BY 4.0 license, description, and keywords on Zenodo.
- [ ] Copy the DOI exactly from Zenodo.
- [ ] Add the DOI to `CITATION.cff` and add a DOI badge to `README.md` in a small follow-up pull request.
- [ ] Cite the version DOI when an exact snapshot matters; use Zenodo's all-versions DOI when referring to the evolving atlas.
- [ ] Confirm the DOI resolves to the archived `v0.1.0` files.
