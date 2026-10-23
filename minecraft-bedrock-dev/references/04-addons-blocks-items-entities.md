# Add-ons: blocks, items, entities, recipes

## Behavior/resource split
Put gameplay data in BP and visuals/audio/localization in RP where appropriate. Link packs through manifests and ensure dependencies are compatible.

## Blocks
- Define the block's identifier, components, states, permutations, collision/selection geometry, mining/destruction behavior, and item mapping as supported by the target version.
- Define texture/material references in RP.
- Test placement, breaking, drops, collision, tool requirements, and behavior in a clean world.

## Items
- Define identifier, category, stack size, durability/use behavior, components, and icon mapping.
- Add recipe definitions if required; validate ingredients, result, unlock behavior, and recipe type.
- Test inventory display, hand rendering, use events, and survival/creative behavior.

## Entities and mobs
- Define identifier, component groups, events, properties, spawn rules, loot, and behavior goals.
- In RP, connect geometry, texture, render controller, animation controller, and animation assets.
- Validate AI goals and priorities; test target acquisition, pathfinding, damage, despawn, persistence, and multiplayer behavior.
- Use documented components first. Use Script API for logic that cannot be expressed safely in entity JSON.

## Recipes, loot, trades, spawn
- Confirm exact schema and folder name from current docs.
- Check namespace identifiers and referenced items/entities.
- Test expected and invalid cases, including duplicate recipe identifiers and missing results.
