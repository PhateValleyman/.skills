# Physics and simulation

## What can and cannot be changed
Bedrock add-ons can modify or simulate many gameplay effects through entity components, movement settings where exposed, block collision/geometry, impulses/velocity APIs where available, damage, knockback, gravity-like behavior, projectiles, and scripted forces. They cannot generally replace the engine's native physics solver through a normal add-on.

## Approach
1. Name the desired behavior precisely: gravity, friction, jump height, fall damage, buoyancy, vehicle steering, projectile trajectory, collision shape, knockback, or time scale.
2. Find a documented component/API for the exact game version.
3. If no direct control exists, simulate it with bounded impulses, state machines, or custom entity behavior.
4. Clamp values, apply cooldowns, and account for tick rate, lag, and multiplayer authority.
5. Test at several frame/tick conditions and on target hardware.

## Examples of simulation systems
- Low-gravity or moon-jump gameplay
- Water buoyancy and swimming-like motion
- Custom vehicles and steering
- Projectile arcs and explosive knockback
- Slippery surfaces and custom block collision
- Fall/damage modifiers where supported
- Wind zones, launch pads, bounce blocks
- Ragdoll-like effects (usually an approximation, not a true engine ragdoll)

## Safety and correctness
- Never claim a JSON component changes native physics unless the schema confirms it.
- Avoid unbounded per-tick impulses that can launch entities or destabilize worlds.
- Explain approximations and limitations to the user.
