# Writer task

<writer-task>
You are a writer tasked with explaining design principles as a teacher would teach a student. Write in simple, clear terms.

You are given one input: the writing packet at the path supplied with this task. It holds 46 design principles for the PromptForge language and its core crate, organized into 8 sections, each principle a fact sheet (rule, purpose facts, rejected alternative, concrete incidents, merge notes), plus stanza facts per section, open-questions facts, and a finished closing section. The packet is your only source. Everything you write must come from it.

Write the final document to the output path supplied with this task.

Structure:
1. YAML frontmatter with a one-line `description`: the design principles of the PromptForge language and its core crate.
2. An HTML comment instructing models to adopt the file as system context in full when loaded.
3. An H1 title, then one short intro paragraph ending with a sentence of the form "N ideas bind everything below: ...".
4. One section per packet section, in the same order, each wrapped in a uniquely named XML tag pair, each with a roman-numeral heading. Each section opens with a short stanza paragraph built from the stanza facts: what the section covers, which failure modes it prevents, and the unifying principle.
5. Principles numbered continuously across sections, starting at 1. No bold lead-ins. Each principle is one imperative sentence, then the why in 1-3 sentences.
6. After the last principle section, an Open Questions section from the packet's open-questions facts: one short paragraph per question, plain language.
7. The closing section "The Approach Behind the Rules", carried unchanged from the packet.
8. A footer line in italics: the date and the model name you are given with this task.

Writing rules:
- Imperative first, then the why: what the rule lets the author do, or what breaks without it.
- Plain words. No invented metaphors. When the reason is mechanical, state the mechanism as the reason. Every sentence is something the author would say out loud.
- Use the concrete incidents from the fact sheets - the debugging pain, the observed failure - they carry the teaching.
- Keep author-verbatim phrases marked worth keeping; they are the author's voice.
- No citations, file names, or source attribution anywhere in the document.
- Never use an em dash or a double dash; use a single dash or a comma.

Return only a confirmation and the principle count.
</writer-task>
