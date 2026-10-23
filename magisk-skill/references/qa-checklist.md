Is the skill's description specific and does it include key trigger phrases?
Does the skill's description clearly state both what the skill does and when it should be used?
Is the skill's SKILL.md body under 5000 words?
Does the skill place additional details in separate reference files where necessary?
Does the skill avoid time-sensitive information, or isolate it in an "old patterns" section?
Does the skill use consistent terminology throughout?
Does the skill include concrete examples rather than abstract ones?
Does the skill limit file references to one level deep?
Does the skill use progressive disclosure appropriately?
Does the skill define workflows with clear, sequential steps?
Do the skill's scripts solve problems directly rather than deferring to Claude?
Does the skill include explicit and helpful error handling?
Does the skill justify all constants, avoiding unexplained values?
Does the skill list all required packages in the instructions and verify their availability?
Do the skill's scripts include clear documentation?
Does the skill use forward slashes for all file paths instead of Windows-style paths?
Does the skill include validation or verification steps for critical operations?
Does the skill include feedback loops for quality-critical tasks?
Does the YAML frontmatter use exactly --- as opening and closing delimiters?
Is the skill's description under 1024 characters?
Does the frontmatter avoid XML angle brackets?
Is the skill name free of reserved prefixes such as claude and anthropic?
Is the skill folder named in kebab-case with no spaces, underscores, or capitals?
Does the skill folder omit a README.md file?
Does the description include negative trigger phrases or scope-limiting language to prevent loading on unrelated queries?
Has the skill been tested to confirm it does not trigger on clearly unrelated requests?
Are critical instructions placed near the top of SKILL.md rather than buried further down?
Does the skill avoid vague instructional language in favour of explicit and deterministic steps?
Does the skill avoid assuming it is the only skill loaded and work correctly alongside other active skills?
if applicable, are all referenced MCP tool names verified to match the actual server tool names exactly including case?
if applicable, does the skill include instructions for what to do if the MCP connection fails entirely?
does the skill contain no emoji in the documentations?
Does the skill's own generated content follow the rules it teaches (dogfood check)?

==========skill specific QA goes below this point==========
Do all customize.sh code examples use abort instead of exit for fatal errors?
Does every boot script example derive MODDIR using ${0%/*} rather than a hardcoded path?
Does every API level guard include the corresponding Android version name in the abort message?
Does the build script in references/build-reference.md verify that curl and zip are available before use?
Is the time-sensitive raw GitHub URL in the build script annotated with a fallback instruction and pinning guidance?
Does the agent workflow section (section 0) appear before section 1 in SKILL.md?
Does references/customize-api.md exist and contain the full variable, function, and API level tables?
Does the skill include a bootloop recovery section with the disable file pattern?
Does the skill include an on-device test cycle before publishing guidance?
Does the skill include Play Integrity safety rules for module authors?
Does the skill identify behaviors that trigger Play Integrity failures?
Does the skill reference MMRL and MMAR as the active module repositories (not the inactive Magisk repo)?
Does the skill route to module-recipes.md when the user's request matches a known archetype?
Does module-recipes.md exist and include at least: prop-only, debloater, font, audio, performance, and PIF companion archetypes?
Does each recipe specify exactly which files are needed and which to omit?
Does the prop-only recipe correctly exclude service.sh and post-fs-data.sh?
Does the debloater recipe use REMOVE variable instead of mknod whiteouts?
Does the audio recipe include ABI-conditional library installation?
Does §12 include action.sh patterns for toggle, immediate-apply, and diagnostic log use cases?
Does §12 include an example of triggering action.sh from WebUI JS?
