"""Step 0: clean and chunk the chat corpus. Deterministic, no model.

Reads promptforge-design/chats/source/, writes promptforge-design/chats/scratch/.
Never modifies the source files.
"""
import os, re, sys

SRC = r'c:\Users\Vinnie\src\cursor\promptforge-design\chats\source'
OUT = r'c:\Users\Vinnie\src\cursor\promptforge-design\chats\scratch'

NOISE_PREFIXES = (
    'The beginning of the above subagent result',
    'Briefly inform the user about the task result',
)

CONTENT_FREE = {
    'run', 'yes', 'yeah', 'no', 'ok', 'okay', 'i approve', 'stop',
    'stop them', 'stop everything', 'try again', 'continue',
    'nope that sounds good', 'sounds good', 'go ahead', 'investigate',
    'yes i think this is the right choice', 'yes i think this is the right call',
}

# file stem -> cut-after paragraph indices (post-cleaning paragraph numbering)
SPLITS = {
    '2026-07-28-0207-architect-vibe-planning': [59, 116, 171],
    '2026-07-30-1046-compaction-algorithm-large': [62, 133, 223, 329],
    '2026-08-02-1134-mcp-client-large': [65, 133, 223, 348],
    '2026-08-09-1058-promptforge-core-large': [78, 155, 248, 374],
    '2026-08-14-1613-promptforge-core-largest': [79, 208, 326, 375],
}

def normalize(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9 ]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def split_sections(text):
    """Return (header, prompts_body, tail). Tail holds Plans/Docs sections."""
    if '## Prompts' not in text:
        return text, None, None
    header, rest = text.split('## Prompts', 1)
    tail = None
    for marker in ('## Plans', '## Design Documents Written'):
        if marker in rest:
            body, tail = rest.split(marker, 1)
            tail = marker + tail
            break
    else:
        body = rest
    return header, body, tail

def clean_paragraphs(body):
    paras = [p.strip() for p in body.split('\n\n')]
    kept, dropped_noise, dropped_empty = [], 0, 0
    for p in paras:
        if not p:
            continue
        if p.startswith(NOISE_PREFIXES):
            dropped_noise += 1
            continue
        if normalize(p) in CONTENT_FREE:
            dropped_empty += 1
            continue
        kept.append(p)
    return kept, dropped_noise, dropped_empty

def numbered(paras):
    return ['**[p%d]** %s' % (i, p) for i, p in enumerate(paras, 1)]

def part_note(lo, hi, total, nparts):
    return ('*Prompts p%d-p%d of %d. This is part %d of %d.'
            % (lo, hi, total, 0, nparts))

def main():
    if not os.path.isdir(SRC):
        print('MISSING SOURCE DIR:', SRC)
        sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    files = sorted(f for f in os.listdir(SRC) if f.endswith('.md'))
    if len(files) != 32:
        print('EXPECTED 32 SOURCE FILES, FOUND', len(files))
        sys.exit(1)
    print('%-52s %6s %6s %6s %5s' % ('file', 'noise', 'empty', 'kept', 'parts'))
    for fname in files:
        stem = fname[:-3]
        with open(os.path.join(SRC, fname), encoding='utf-8') as f:
            text = f.read()
        header, body, tail = split_sections(text)
        if body is None:
            print('NO PROMPTS SECTION:', fname)
            sys.exit(1)
        kept, d_noise, d_empty = clean_paragraphs(body)
        cuts = SPLITS.get(stem, [])
        for c in cuts:
            if c >= len(kept):
                print('BAD CUT INDEX:', fname, c, 'of', len(kept))
                sys.exit(1)
        marked = numbered(kept)
        nparts = len(cuts) + 1 if cuts else 1
        if not cuts:
            out = [header.rstrip(), '', '## Prompts', '']
            out.extend(marked)
            if tail:
                out.append('')
                out.append(tail.rstrip())
            with open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(out) + '\n')
        else:
            bounds = [0] + cuts + [len(marked)]
            for pi in range(nparts):
                lo, hi = bounds[pi], bounds[pi + 1]  # hi exclusive; cut after pN means index N
                chunk = marked[lo:hi]
                plo, phi = lo + 1, hi
                note = '*Prompts p%d-p%d of %d. Part %d of %d.' % (plo, phi, len(marked), pi + 1, nparts)
                if pi + 1 < nparts and tail:
                    note += ' The Plans and Design Documents sections are in part %d.*' % nparts
                else:
                    note = note[:-1] + '.*'
                out = [header.rstrip(), '', note, '', '## Prompts', '']
                out.extend(chunk)
                if pi + 1 == nparts and tail:
                    out.append('')
                    out.append(tail.rstrip())
                pname = '%s-part%d.md' % (stem, pi + 1)
                with open(os.path.join(OUT, pname), 'w', encoding='utf-8') as f:
                    f.write('\n\n'.join(out) + '\n')
                # first line after the cut, for eyeballing topic transitions
                if pi + 1 < nparts:
                    nxt = kept[hi].split('\n', 1)[0][:80]
                    print('   cut after p%d -> next: %s' % (phi, nxt))
        print('%-52s %6d %6d %6d %5d' % (fname[:52], d_noise, d_empty, len(kept), nparts))
    print('DONE')

if __name__ == '__main__':
    main()
