# Publication verification

20 November 2026. This records the scope of internal checks for the initial
publication, not external mathematical review or a novelty certificate.

- All 16 checks in `scripts/verify.py` passed in an isolated temporary copy.
  The receipt identifies the checked sources and the exact versus numerical scope.
- All eight generated pages passed `scripts/check_site.py`: 211 local links,
  64 repository targets, eight image alternatives and four labelled videos.
- All 1,344 video frames decoded successfully at native 1280 × 720, 24 fps.
  Hashes, durations, frame counts and nonstatic output were checked by
  `rendering/verify_media.py`. The four-frame-per-film contact sheet was inspected.
- Browser inspection at desktop and 390-pixel mobile width found no document
  overflow. Mobile navigation worked, and the displayed results formulas had
  no MathJax errors. Long formulas scroll within their own containers.
- The hero's metadata-event race was found and corrected. Autoplay initialized,
  and its visible pause control stopped the film. All three gallery videos
  loaded the expected dimensions and durations with no media errors.
- TouchDesigner native previews and a separate portable `.tox` import passed
  in the recorded session. A later project change and unresponsive MCP endpoint
  prevented a fresh live check. The new session was not altered.

See `PUBLICATION_AUDIT.md` for mathematical review. Historical originality,
exact Hausdorff dimensions, and the full attractor/complement classifications
remain open. The delivered objects meet the connected-spatial interpretation
of the brief; they have zero volume.

`SPECTRAL_TANGENTS_REVIEW.md` additionally audits the power-law tangent rate,
nonconstant Assouad spectrum and maximal quasi-Assouad dimension. The five
new finite whole-sphere bounds passed integer verification. These analytic
and finite results have different scopes and are identified separately.
