# Local Frontier Comparison Table

| Model | Tasks | Final Acc | Commit Acc | Abstain | Bluff | Escalate | Silent Failure | Avg Conf | Wrong Commit Conf | Parse Error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| qwen | 40 | 0.72 | 1.00 | 0.05 | 0.00 | 0.75 | 0.00 | 0.19 | 0.00 | 0.00 |
| smollm | 40 | 0.75 | 1.00 | 0.00 | 0.00 | 0.75 | 0.00 | 0.89 | 0.00 | 0.00 |

## By Task Type

### qwen

| Task Type | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| adversarial_trust | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |
| clear_commit | 0.80 | 0.10 | 0.00 | 0.10 | 0.00 |
| hidden_state_uncertainty | 0.10 | 0.10 | 0.00 | 0.90 | 0.00 |
| overflow_mismatch | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |

### smollm

| Task Type | Final Acc | Abstain | Bluff | Escalate | Silent Failure |
|---|---:|---:|---:|---:|---:|
| adversarial_trust | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |
| clear_commit | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| hidden_state_uncertainty | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 |
| overflow_mismatch | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 |
