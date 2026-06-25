# ASR Breakdown Report

All values use the same normalization and alignment rules as `score.py`.
Clip-level slices count insertions against the clip bucket. Token-language slices attribute substitutions and deletions to the reference token language; insertions are reported separately because they have no reference-language owner.

## headline

Clips: 40

| Metric | WER |
|---|---:|
| Overall | 59.5% (222/373) |
| Switch-region | 35.8% (59/165) |
| Monolingual | 66.3% (138/208) |
| Switch penalty | -30.6% |

### By speaker

| Bucket | Clips | WER |
|---|---:|---:|
| `spk01` | 40 | 59.5% (222/373) |

### By domain

| Bucket | Clips | WER |
|---|---:|---:|
| `oral_tradition` | 5 | 60.0% (33/55) |
| `transport` | 5 | 55.1% (27/49) |
| `family` | 5 | 61.7% (29/47) |
| `market` | 5 | 57.4% (27/47) |
| `everyday` | 5 | 44.4% (20/45) |
| `school_work` | 5 | 64.4% (29/45) |
| `culture` | 5 | 67.4% (29/43) |
| `health` | 5 | 66.7% (28/42) |

### By switch type

| Bucket | Clips | WER |
|---|---:|---:|
| `HIL+EN` | 17 | 59.9% (94/157) |
| `HIL` | 11 | 75.0% (75/100) |
| `HIL+TL` | 7 | 61.9% (39/63) |
| `HIL+TL+EN` | 5 | 26.4% (14/53) |

### By token language

| Bucket | Clips | WER |
|---|---:|---:|
| `hil` | 40 | 58.3% (176/302) |
| `en` | 22 | 29.2% (14/48) |
| `tl` | 12 | 30.4% (7/23) |

### Switch-region by language pair

| Bucket | WER |
|---|---:|
| `hil<->en` | 40.0% (48/120) |
| `hil<->tl` | 24.4% (11/45) |
| `tl<->en` | 6.2% (1/16) |

Unattributed token-language insertions: 25

## spk2

Clips: 40

| Metric | WER |
|---|---:|
| Overall | 34.4% (124/360) |
| Switch-region | 28.6% (52/182) |
| Monolingual | 38.8% (69/178) |
| Switch penalty | -10.2% |

### By speaker

| Bucket | Clips | WER |
|---|---:|---:|
| `spk02` | 40 | 34.4% (124/360) |

### By domain

| Bucket | Clips | WER |
|---|---:|---:|
| `everyday` | 5 | 31.9% (15/47) |
| `oral_tradition` | 5 | 31.9% (15/47) |
| `school_work` | 5 | 21.3% (10/47) |
| `market` | 5 | 50.0% (23/46) |
| `transport` | 5 | 26.1% (12/46) |
| `health` | 5 | 45.5% (20/44) |
| `culture` | 5 | 33.3% (14/42) |
| `family` | 5 | 36.6% (15/41) |

### By switch type

| Bucket | Clips | WER |
|---|---:|---:|
| `HIL+EN` | 15 | 29.3% (39/133) |
| `HIL` | 10 | 50.0% (44/88) |
| `HIL+TL+EN` | 7 | 30.6% (22/72) |
| `HIL+TL` | 8 | 28.4% (19/67) |

### By token language

| Bucket | Clips | WER |
|---|---:|---:|
| `hil` | 40 | 37.3% (79/212) |
| `tl` | 15 | 26.5% (26/98) |
| `en` | 22 | 32.0% (16/50) |

### Switch-region by language pair

| Bucket | WER |
|---|---:|
| `hil<->en` | 26.2% (27/103) |
| `hil<->tl` | 32.8% (19/58) |
| `tl<->en` | 31.6% (12/38) |

Unattributed token-language insertions: 3

## combined

Clips: 80

| Metric | WER |
|---|---:|
| Overall | 47.2% (346/733) |
| Switch-region | 32.0% (111/347) |
| Monolingual | 53.6% (207/386) |
| Switch penalty | -21.6% |

### By speaker

| Bucket | Clips | WER |
|---|---:|---:|
| `spk01` | 40 | 59.5% (222/373) |
| `spk02` | 40 | 34.4% (124/360) |

### By domain

| Bucket | Clips | WER |
|---|---:|---:|
| `oral_tradition` | 10 | 47.1% (48/102) |
| `transport` | 10 | 41.1% (39/95) |
| `market` | 10 | 53.8% (50/93) |
| `everyday` | 10 | 38.0% (35/92) |
| `school_work` | 10 | 42.4% (39/92) |
| `family` | 10 | 50.0% (44/88) |
| `health` | 10 | 55.8% (48/86) |
| `culture` | 10 | 50.6% (43/85) |

### By switch type

| Bucket | Clips | WER |
|---|---:|---:|
| `HIL+EN` | 32 | 45.9% (133/290) |
| `HIL` | 21 | 63.3% (119/188) |
| `HIL+TL` | 15 | 44.6% (58/130) |
| `HIL+TL+EN` | 12 | 28.8% (36/125) |

### By token language

| Bucket | Clips | WER |
|---|---:|---:|
| `hil` | 80 | 49.6% (255/514) |
| `tl` | 27 | 27.3% (33/121) |
| `en` | 44 | 30.6% (30/98) |

### Switch-region by language pair

| Bucket | WER |
|---|---:|
| `hil<->en` | 33.6% (75/223) |
| `hil<->tl` | 29.1% (30/103) |
| `tl<->en` | 24.1% (13/54) |

Unattributed token-language insertions: 28
