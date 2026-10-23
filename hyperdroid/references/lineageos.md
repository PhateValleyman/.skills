# LineageOS development

Use for LineageOS-specific source trees, device bring-up, vendor blobs, ROM builds, `breakfast`/`brunch`, `repopick`, and Gerrit contributions. For generic Android build environment and Gradle/kernel guidance, see [android-build.md](android-build.md); for flashing, see [android-fastboot.md](android-fastboot.md).

## Contents

- [Choose device and branch](#choose-device-and-branch)
- [Initialize and sync source](#initialize-and-sync-source)
- [Device trees and dependencies](#device-trees-and-dependencies)
- [Build and validate](#build-and-validate)
- [Vendor blobs](#vendor-blobs)
- [Gerrit and repopick](#gerrit-and-repopick)

## Choose device and branch

- Confirm the exact device/codename, target LineageOS release/branch, and current support status using the official LineageOS device pages and the maintained source manifest. A device's codename, supported branches, partition scheme, or installation steps can change; don't infer a branch from an old example.
- Confirm host requirements and free disk before syncing. Full Android source and build outputs are large; set a reasonable sync/build job count and allow for substantial time.
- Note whether the user's goal is a local build, bring-up, device-tree change, or contribution. Do not turn a build request into a flash or Gerrit push without user intent.

## Initialize and sync source

- Use the current documented manifest URL and branch for the target release. Keep branch choice explicit; don't hardcode the repository's historical LineageOS 21 examples.
- Inspect the current checkout and local modifications before syncing. `repo sync` updates many project checkouts; avoid `--force-sync` unless specifically needed and approved.
- Use `breakfast <device>` after sourcing the tree's `build/envsetup.sh` when supported; it may select targets and sync device-specific dependencies. Inspect its output and resulting tree.
- `repo sync -c -j<N>` can reduce checkout scope and concurrency; choose `<N>` for available bandwidth, memory, and CPU rather than assuming `nproc` is safe.

```sh
# Inspect local repository changes before synchronization.
git status --short --branch

# Initialize the documented LineageOS manifest and target branch.
repo init -u <documented-manifest-url> -b <supported-branch>

# Sync using a bounded number of parallel jobs.
repo sync -c -j<bounded-job-count>

# Load build functions from the checked-out tree.
source build/envsetup.sh

# Configure the exact device using its current tree instructions.
breakfast <device-codename>
```

## Device trees and dependencies

Common device trees live under `device/<vendor>/<device>/` and may include:

- `BoardConfig.mk`, `device.mk`, `AndroidProducts.mk`, product makefiles, and `vendorsetup.sh`;
- `lineage.dependencies` and local manifest entries for device-common, kernel, or vendor repositories;
- `extract-files.sh`, `proprietary-files.txt`, overlays, recovery configuration, and SELinux policy.

Inspect existing device-family trees and current upstream conventions before editing. Verify each dependency repository, target path, revision, and product inheritance. Do not copy BoardConfig, partition sizes, kernel settings, or SELinux rules from a similar model without checking hardware and branch compatibility.

A local manifest can add repositories under `.repo/local_manifests/`; preserve existing entries and review the diff before syncing. A missing dependency may call for correcting the manifest or rerunning the documented setup—not deleting a local checkout.

## Build and validate

- In the source tree, load `build/envsetup.sh`, run the documented `breakfast <device>`, then use `brunch <device>` or the maintainer's specified target. `brunch` often combines setup and a full build; do not repeat setup unnecessarily.
- Common targets include `mka bacon` for a flashable ROM package and `mka bootimage`/`mka systemimage` for individual build products when supported. Confirm the selected target for the current branch.
- Check the final exit code and actual artifacts under `out/target/product/<device>/`. A successful compile is not proof that the package is compatible or safe to flash.
- For build failures, capture the first useful error, missing project/module, and relevant device tree. Avoid starting with a full clean or wiping output; inspect the cause first.

```sh
# Build the configured device using the LineageOS full-build wrapper.
brunch <device-codename>

# Build a flashable package when the configured tree provides this target.
mka bacon

# Build only the boot image when the current device tree supports it.
mka bootimage

# Synchronize one project path when diagnosing a source dependency.
repo sync <project-path>
```

## Vendor blobs

- Extract only from firmware or a device the user is authorized to use, following the device tree's documented script and exact release. Proprietary blobs remain subject to their licenses; do not redistribute them or upload them to an external service without clear authorization and legal permission.
- Review `proprietary-files.txt` and extraction output for missing files, source/destination mappings, and device/build mismatch. Preserve provenance and avoid copying blobs from a similar model as a guess.
- If a build reports missing symbols/services, inspect the first linker or service error and verify the corresponding tree/blob version before changing the file list.

```sh
# Run the tree's extraction script from its documented device directory.
./extract-files.sh

# Extract only from an authorized local OTA package when supported by the script.
./extract-files.sh <authorized-local-ota-file>
```

## Gerrit and repopick

- Use the project's Gerrit instructions and current branch/project path. Configure Git identity locally to the repository by default; avoid changing `--global` settings unless requested. Never expose private SSH keys or tokens.
- Before picking a change, inspect local work and confirm the target branch. Prefer `repopick -n <change>` for preview when supported; use force options only when the user approves overwriting local changes.
- A Gerrit push uploads a patch for review. Do it when the user explicitly requests submission; inspect the exact staged diff, commit, project, and target branch first. Use the repository's `Change-Id` hook and contribution standards rather than inventing a Change-Id.
- Keep review credentials private and do not put them in shell history, logs, source files, or URLs.

```sh
# Preview the requested Gerrit change when this repopick version supports dry run.
repopick -n <change-number>

# Start a named repo branch in the intended project checkout.
repo start <topic-branch> <project-path>

# Review the staged diff before making a commit.
git diff --cached --check && git diff --cached

# Push the approved patch to the documented Gerrit project and branch.
git push ssh://<username>@review.lineageos.org:29418/<project> HEAD:refs/for/<branch>
```
