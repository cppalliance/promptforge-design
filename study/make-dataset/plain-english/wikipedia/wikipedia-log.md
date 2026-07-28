# Wikipedia blur-to-original dataset - build log

Training pairs for the prompt-compression (deblurring) study. Each pair is `{input: blurred, target: original}`: the model learns to recover a sharp Wikipedia lead from a bloated, vaguer paraphrase of it.

## Source and method

- Source: English Wikipedia lead extracts (article intros) pulled from random articles via the MediaWiki Action API (`generator=random`), filtered to 60-200 words and deduped by title. Broad domains (people, places, vehicles, species, institutions, architecture, and more).
- Blur: each lead was run through blur-gen for 3 sequential passes (1 variant), one model per pass (claude-haiku-4-5 -> claude-sonnet-4-6 -> claude-opus-4-8), producing a wordier / vaguer paraphrase at each pass. This gives 3 blur records per passage.
- Gate: the directional meaning gate `gate1(A=original, B=blurred)` was run through pairgen's control path (synthetic `## pNNNN` headings stripped first). PASS means the blurred text B preserves everything in the original A (the blur dropped nothing); FAIL means B lost or shifted meaning that was present in A.
- Kept pairs: only gate1 PASS controls were kept and emitted as `blur-to-original` pairs where the target is the true sharp original captured before blur. A learned model approximates the inverse of the blur from these pairs.

## Counts

- Passages fetched: 100 (word-count spread 60 / 99 / 191 min/median/max)
- Blur records: 300 (100 passages x 3 blur passes; blur run fail=0)
- Gate control records: 300 (gate run fail=0)

## Gate results

- gate1 PASS (kept): 169 / 300 = 56.3 percent
- gate1 FAIL (dropped): 131 / 300 = 43.7 percent
- Kept pairs: 169

## Size and expansion (from finalize, over the 169 kept pairs)

- Blur-expansion (original -> blurred, mean): 1.06x
- Median input (blurred) words: 95
- Median target (original) words: 89

## Sample kept pairs (input = blurred, target = original; truncated to ~200 chars)

- Sample 1 - Jowett Bradford (source `wikipedia-p1-0`, input 73w -> target 71w)
    - input (blurred): "From 1946 until 1953, Jowett Cars Ltd, a company based in Idle near Bradford, England, manufactured the Jowett Bradford, a British light van. Between 1947 and 1953, an estate car variant was also offe..."
    - target (original): "The Jowett Bradford was a British light van produced from 1946 to 1953 by Jowett Cars Ltd of Idle, near Bradford, England. It was also available as an estate car from 1947 to 1953. The vehicle was bas..."
- Sample 2 - Anna Maria Amcats (source `wikipedia-p2-4`, input 107w -> target 121w)
    - input (blurred): "Located in Paxton, Massachusetts, Anna Maria College sponsored intercollegiate athletic programs whose teams were called the Anna Maria Amcats. Competing across 13 sports, these teams operated under N..."
    - target (original): "The Anna Maria Amcats was the nickname of the intercollegiate athletic teams of Anna Maria College, located in Paxton, Massachusetts. The school's teams participated in 13 intercollegiate sports at th..."
- Sample 3 - Kristoffer Wikner Sundborg (source `wikipedia-p2-16`, input 72w -> target 68w)
    - input (blurred): "Kristoffer Wikner Sundborg, born January 20, 1993, is a retired Swedish ice hockey winger. He made his Elitserien debut during the 2011-12 season with Frolunda HC, going on to appear in 21 total games..."
    - target (original): "Kristoffer Wikner Sundborg (born January 20, 1993) is a Swedish retired ice hockey winger. He made his Elitserien debut with Frolunda HC during the 2011-12 season and played a total of 21 games during..."

## Sample gate-FAIL drops (the meaning loss gate1 caught)

- `wikipedia-p3-8`: "Many specimens are sterile" (A) becomes "Most specimens lack fruiting bodies" (B), shifting the quantifier from "many" to "most" and thus changing the claimed proportion.
- `wikipedia-p1-12`: "Bequeathed his stamp collection" implies a posthumous gift via will, whereas A's "donated" describes an act he made during life (consistent with also having "turned a building into a museum" and rented it out from 1955).
- `wikipedia-p3-32`: "Some architectural scholars believe" (A) becomes "Many architectural historians link" (B) - the quantifier shifts from "some" to "many," changing the claimed prevalence of the belief, which would yield different answers to a question about how widely held the Carolina-origin theory is.

*Built 2026-07-27 from the make-dataset pipeline (blur-gen 3 passes, pairgen gate1 control path). Commit intentionally omitted; the parent will commit.*
