# Audio, particles, animation, and visual effects

## Audio
- Check sound definitions, event names, file format/encoding, resource paths, volume/pitch, and localization where applicable.
- Keep file size reasonable and avoid excessive concurrent looping sounds.
- Verify licenses and attribution for imported sounds.

## Particles
- Define emitter identifiers, material/texture, lifetime, spawn rate, shape, motion, color/size curves, and events according to the current schema.
- Limit particle counts and test on mobile hardware.
- Use particles for dust, smoke, sparks, magic, lava, trails, and environmental ambience.

## Animation
- Distinguish animation data from animation controllers.
- Keep bone names aligned with geometry and controller references.
- Test transitions, loops, blend behavior, animation timing, and entity state changes.
- For animated textures, validate flipbook metadata and sprite-sheet frame layout.

## Visual polish checklist
- Correct asset paths and identifiers
- No missing textures/sounds
- No excessive tick or rendering cost
- Mobile readability and performance
- Clear fallback when assets fail
