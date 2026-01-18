# Parser Performance Analysis

This document presents benchmark results comparing the regex and tree-sitter parsers.

## Benchmark Results

| ANLUs | Source Size | Regex Parser | Tree-Sitter | Ratio |
|-------|-------------|--------------|-------------|-------|
| 10 | 2.3 KB | 0.52ms | 0.76ms | 1.5x slower |
| 50 | 11.7 KB | 1.85ms | 2.54ms | 1.4x slower |
| 100 | 23.4 KB | 3.58ms | 5.14ms | 1.4x slower |
| 200 | 47.5 KB | 7.18ms | 10.81ms | 1.5x slower |

## Analysis

### Regex Parser Advantages
- **Faster raw parsing**: ~1.4-1.5x faster for simple parsing
- **Zero dependencies**: No binary libraries required
- **Simpler deployment**: Pure Python implementation

### Tree-Sitter Advantages
- **Error recovery**: Produces partial AST even with syntax errors
- **Incremental parsing**: Efficient for IDE integration
- **Precise source locations**: Better error messages
- **Standard grammar**: Reusable for other tools (syntax highlighting, etc.)

## Recommendations

### When to use Regex Parser
- CI/CD pipelines where speed matters
- Simple scripts and batch processing
- Environments where tree-sitter binaries are problematic

### When to use Tree-Sitter Parser
- IDE and editor integration
- Development workflows needing good error messages
- Interactive tools where error recovery matters

## Running the Benchmark

```bash
python stress-test/benchmark_parsers.py
```

## Methodology

- Each test runs 5 iterations
- Results show mean, min, max, and standard deviation
- Source files generated programmatically with varying ANLU counts
- Tested on Python 3.12, Windows 11

## Future Optimizations

Potential improvements:
1. **Regex parser**: Profile hot paths, consider compilation caching
2. **Tree-sitter**: Ensure language library is loaded once (already done)
3. **Both**: Consider parallel parsing for multi-file projects
