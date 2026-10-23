# Skins, textures, models, and geometry

## Player skins
- Confirm whether the target is a classic/Steve-style or slim/Alex-style geometry and the target version's skin import rules.
- Use the correct PNG canvas and UV layout for the chosen geometry. Preserve transparent pixels; do not flatten alpha unless requested.
- Inspect front/back/side UV regions, outer layer, head overlay, arms, and legs. A valid PNG can still have a broken UV layout.
- Skin packs have different metadata from ordinary RPs. Validate pack manifest, skin definitions, geometry identifiers, localization, and icon assets.
- A `.mcpack`/`.mcaddon` file extension alone does not make an invalid package valid.

## Textures and icons
- Use exact path/case expected by the pack.
- Check dimensions, alpha channel, palette, UV alignment, and animation metadata.
- Keep vanilla overrides isolated and document which files are intentionally replaced.
- For GUI icons, check transparency, pixel alignment, scaling, and atlas references.

## Blockbench and models
- Bedrock entity geometry is JSON-based and has its own format/version.
- Validate bone names, pivots, cubes, UVs, texture dimensions, render controllers, and animation references.
- Do not assume Java models or Java resource-pack formats are compatible.
- Keep model, texture, entity definition, render controller, and animation identifiers aligned.

## Asset QA
- Preview on a neutral background and at game scale.
- Check for mirrored UVs, seams, unexpected opaque pixels, incorrect layer order, and off-by-one dimensions.
- Include a small change log and source/license notes for imported assets.
