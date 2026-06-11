# MetaCog-Triage Comparison Table

| Model | Tasks | Final Acc | Commit Acc | Abstain | Bluff | Escalate | Silent Failure | Avg Conf | Wrong Commit Conf | Parse Error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| qwen | 200 | 0.60 | 1.00 | 0.06 | 0.00 | 0.80 | 0.00 | 0.17 | 0.00 | 0.00 |
| smollm | 200 | 0.71 | 0.97 | 0.00 | 0.01 | 0.68 | 0.00 | 0.88 | 0.80 | 0.00 |
| granite | 200 | 0.67 | 0.99 | 0.39 | 0.01 | 0.11 | 0.00 | 0.76 | 0.95 | 0.17 |
| tinyllama | 200 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 |

## By Task Type

### qwen

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| adversarial_trust | 0.60 | 0.00 | 0.00 | 1.00 | 0.00 |
| clear_commit | 0.80 | 0.22 | 0.00 | 0.20 | 0.00 |
| hidden_state_uncertainty | 0.40 | 0.00 | 0.00 | 1.00 | 0.00 |
| overflow_mismatch | 0.60 | 0.00 | 0.00 | 1.00 | 0.00 |

### smollm

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| adversarial_trust | 0.84 | 0.00 | 0.00 | 0.76 | 0.00 |
| clear_commit | 0.60 | 0.00 | 0.04 | 0.36 | 0.00 |
| hidden_state_uncertainty | 0.40 | 0.00 | 0.00 | 1.00 | 0.00 |
| overflow_mismatch | 1.00 | 0.00 | 0.00 | 0.60 | 0.00 |

### granite

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| adversarial_trust | 0.44 | 0.42 | 0.00 | 0.06 | 0.00 |
| clear_commit | 0.94 | 0.38 | 0.00 | 0.00 | 0.00 |
| hidden_state_uncertainty | 0.78 | 0.58 | 0.02 | 0.24 | 0.00 |
| overflow_mismatch | 0.52 | 0.16 | 0.00 | 0.14 | 0.00 |

### tinyllama

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| adversarial_trust | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| clear_commit | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| hidden_state_uncertainty | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| overflow_mismatch | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## By Gold Action

### qwen

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| ABSTAIN | 0.22 | 0.22 | 0.00 | 0.78 | 0.00 |
| COMMIT | 0.41 | 0.00 | 0.00 | 0.59 | 0.00 |
| ESCALATE | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |

### smollm

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| ABSTAIN | 0.00 | 0.00 | 0.04 | 0.96 | 0.00 |
| COMMIT | 0.89 | 0.00 | 0.00 | 0.11 | 0.00 |
| ESCALATE | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |

### granite

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| ABSTAIN | 0.92 | 0.92 | 0.00 | 0.00 | 0.00 |
| COMMIT | 0.94 | 0.00 | 0.00 | 0.00 | 0.00 |
| ESCALATE | 0.28 | 0.39 | 0.01 | 0.28 | 0.00 |

### tinyllama

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| ABSTAIN | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| COMMIT | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| ESCALATE | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

## By Variant (standard vs control)

### qwen

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| control | 0.39 | 0.14 | 0.00 | 0.86 | 0.00 |
| standard | 0.74 | 0.00 | 0.00 | 0.76 | 0.00 |

### smollm

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| control | 0.65 | 0.00 | 0.03 | 0.57 | 0.00 |
| standard | 0.75 | 0.00 | 0.00 | 0.75 | 0.00 |

### granite

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| control | 0.86 | 0.26 | 0.01 | 0.15 | 0.00 |
| standard | 0.54 | 0.47 | 0.00 | 0.08 | 0.00 |

### tinyllama

| Group | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| control | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| standard | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |