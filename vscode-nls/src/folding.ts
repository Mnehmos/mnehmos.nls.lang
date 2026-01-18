import * as vscode from 'vscode';

export class NLFoldingRangeProvider implements vscode.FoldingRangeProvider {
    
    provideFoldingRanges(
        document: vscode.TextDocument,
        _context: vscode.FoldingContext,
        _token: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.FoldingRange[]> {
        const ranges: vscode.FoldingRange[] = [];
        const lines = document.getText().split('\n');
        
        let anluStart: number | null = null;
        const blockStarts: Map<number, string> = new Map(); // line -> block type
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const trimmed = line.trim();
            
            // ANLU header [function-name]
            if (/^\[[a-zA-Z][a-zA-Z0-9._-]*\]\s*$/.test(trimmed)) {
                // Close previous ANLU
                if (anluStart !== null && anluStart < i - 1) {
                    ranges.push(new vscode.FoldingRange(anluStart, i - 1, vscode.FoldingRangeKind.Region));
                }
                anluStart = i;
                continue;
            }
            
            // Block opening: @type, @test, @property, @invariant, @literal, @main
            if (/^@(type|test|property|invariant|literal|main)\b.*\{\s*$/.test(trimmed)) {
                // Close any open ANLU before a block
                if (anluStart !== null && anluStart < i - 1) {
                    ranges.push(new vscode.FoldingRange(anluStart, i - 1, vscode.FoldingRangeKind.Region));
                    anluStart = null;
                }
                blockStarts.set(i, 'block');
                continue;
            }
            
            // Block closing }
            if (trimmed === '}') {
                // Find matching block start
                let matchedStart: number | null = null;
                for (const [startLine] of blockStarts) {
                    if (startLine < i) {
                        matchedStart = startLine;
                    }
                }
                if (matchedStart !== null) {
                    ranges.push(new vscode.FoldingRange(matchedStart, i, vscode.FoldingRangeKind.Region));
                    blockStarts.delete(matchedStart);
                }
                continue;
            }
            
            // Section headers (INPUTS:, GUARDS:, LOGIC:, etc.) - fold to next section or ANLU
            if (/^(PURPOSE|INPUTS|GUARDS|LOGIC|RETURNS|DEPENDS|EDGE\s+CASES):/.test(trimmed)) {
                // Look ahead to find where this section ends
                const sectionStart = i;
                let sectionEnd = i;
                
                for (let j = i + 1; j < lines.length; j++) {
                    const nextLine = lines[j].trim();
                    // Section ends at next section, ANLU header, or block directive
                    if (/^(PURPOSE|INPUTS|GUARDS|LOGIC|RETURNS|DEPENDS|EDGE\s+CASES):/.test(nextLine) ||
                        /^\[[a-zA-Z][a-zA-Z0-9._-]*\]\s*$/.test(nextLine) ||
                        /^@(type|test|property|invariant|literal|main)\b/.test(nextLine)) {
                        break;
                    }
                    if (nextLine.length > 0) {
                        sectionEnd = j;
                    }
                }
                
                if (sectionEnd > sectionStart) {
                    ranges.push(new vscode.FoldingRange(sectionStart, sectionEnd, vscode.FoldingRangeKind.Region));
                }
            }
        }
        
        // Close any remaining open ANLU at end of file
        if (anluStart !== null && anluStart < lines.length - 1) {
            ranges.push(new vscode.FoldingRange(anluStart, lines.length - 1, vscode.FoldingRangeKind.Region));
        }
        
        return ranges;
    }
}
