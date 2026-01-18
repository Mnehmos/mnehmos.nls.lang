import * as vscode from 'vscode';

export class NLDocumentSymbolProvider implements vscode.DocumentSymbolProvider {

    provideDocumentSymbols(
        document: vscode.TextDocument,
        _token: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.DocumentSymbol[]> {
        const symbols: vscode.DocumentSymbol[] = [];
        const lines = document.getText().split('\n');

        let currentAnlu: vscode.DocumentSymbol | null = null;
        let currentType: vscode.DocumentSymbol | null = null;
        let currentTest: vscode.DocumentSymbol | null = null;
        let currentProperty: vscode.DocumentSymbol | null = null;
        let currentInvariant: vscode.DocumentSymbol | null = null;

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const lineRange = new vscode.Range(i, 0, i, line.length);

            // Module directive
            const moduleMatch = /^@module\s+(\S+)/.exec(line);
            if (moduleMatch) {
                symbols.push(new vscode.DocumentSymbol(
                    moduleMatch[1],
                    'module',
                    vscode.SymbolKind.Module,
                    lineRange,
                    lineRange
                ));
                continue;
            }

            // ANLU header [function-name]
            const anluMatch = /^\[([a-zA-Z][a-zA-Z0-9._-]*)\]\s*$/.exec(line);
            if (anluMatch) {
                // Close previous ANLU
                if (currentAnlu) {
                    this.updateSymbolRange(currentAnlu, i - 1, lines);
                }

                currentAnlu = new vscode.DocumentSymbol(
                    anluMatch[1],
                    '',
                    vscode.SymbolKind.Function,
                    lineRange,
                    lineRange
                );
                symbols.push(currentAnlu);
                continue;
            }

            // Type definition @type TypeName {
            const typeMatch = /^@type\s+([A-Z][a-zA-Z0-9]*)/.exec(line);
            if (typeMatch) {
                if (currentAnlu) {
                    this.updateSymbolRange(currentAnlu, i - 1, lines);
                    currentAnlu = null;
                }

                currentType = new vscode.DocumentSymbol(
                    typeMatch[1],
                    'type',
                    vscode.SymbolKind.Class,
                    lineRange,
                    lineRange
                );
                symbols.push(currentType);
                continue;
            }

            // Type closing brace
            if (currentType && line.trim() === '}') {
                this.updateSymbolRange(currentType, i, lines);
                currentType = null;
                continue;
            }

            // Type field
            if (currentType) {
                const fieldMatch = /^\s*[•\-\*]?\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:/.exec(line);
                if (fieldMatch) {
                    currentType.children.push(new vscode.DocumentSymbol(
                        fieldMatch[1],
                        '',
                        vscode.SymbolKind.Property,
                        lineRange,
                        lineRange
                    ));
                }
                continue;
            }

            // Test block @test [anlu-name] {
            const testMatch = /^@test\s+\[([a-zA-Z][a-zA-Z0-9._-]*)\]/.exec(line);
            if (testMatch) {
                if (currentAnlu) {
                    this.updateSymbolRange(currentAnlu, i - 1, lines);
                    currentAnlu = null;
                }

                currentTest = new vscode.DocumentSymbol(
                    `test: ${testMatch[1]}`,
                    '',
                    vscode.SymbolKind.Method,
                    lineRange,
                    lineRange
                );
                symbols.push(currentTest);
                continue;
            }

            // Test closing brace
            if (currentTest && line.trim() === '}') {
                this.updateSymbolRange(currentTest, i, lines);
                currentTest = null;
                continue;
            }

            // Property block @property [anlu-name] {
            const propertyMatch = /^@property\s+\[([a-zA-Z][a-zA-Z0-9._-]*)\]/.exec(line);
            if (propertyMatch) {
                if (currentAnlu) {
                    this.updateSymbolRange(currentAnlu, i - 1, lines);
                    currentAnlu = null;
                }

                currentProperty = new vscode.DocumentSymbol(
                    `property: ${propertyMatch[1]}`,
                    '',
                    vscode.SymbolKind.Interface,
                    lineRange,
                    lineRange
                );
                symbols.push(currentProperty);
                continue;
            }

            // Property closing brace
            if (currentProperty && line.trim() === '}') {
                this.updateSymbolRange(currentProperty, i, lines);
                currentProperty = null;
                continue;
            }

            // Invariant block @invariant TypeName {
            const invariantMatch = /^@invariant\s+([A-Z][a-zA-Z0-9]*)/.exec(line);
            if (invariantMatch) {
                if (currentAnlu) {
                    this.updateSymbolRange(currentAnlu, i - 1, lines);
                    currentAnlu = null;
                }

                currentInvariant = new vscode.DocumentSymbol(
                    `invariant: ${invariantMatch[1]}`,
                    '',
                    vscode.SymbolKind.Event,
                    lineRange,
                    lineRange
                );
                symbols.push(currentInvariant);
                continue;
            }

            // Invariant closing brace
            if (currentInvariant && line.trim() === '}') {
                this.updateSymbolRange(currentInvariant, i, lines);
                currentInvariant = null;
                continue;
            }

            // Sections within ANLU
            if (currentAnlu) {
                const sectionMatch = /^(PURPOSE|INPUTS|GUARDS|LOGIC|RETURNS|DEPENDS|EDGE\s+CASES):/.exec(line);
                if (sectionMatch) {
                    const sectionName = sectionMatch[1];
                    const kind = this.getSectionSymbolKind(sectionName);

                    currentAnlu.children.push(new vscode.DocumentSymbol(
                        sectionName,
                        '',
                        kind,
                        lineRange,
                        lineRange
                    ));
                }

                // Update PURPOSE as detail
                const purposeMatch = /^PURPOSE:\s*(.+)$/.exec(line);
                if (purposeMatch) {
                    currentAnlu.detail = purposeMatch[1];
                }
            }
        }

        // Close any remaining open symbols
        const lastLine = lines.length - 1;
        if (currentAnlu) {
            this.updateSymbolRange(currentAnlu, lastLine, lines);
        }
        if (currentType) {
            this.updateSymbolRange(currentType, lastLine, lines);
        }
        if (currentTest) {
            this.updateSymbolRange(currentTest, lastLine, lines);
        }
        if (currentProperty) {
            this.updateSymbolRange(currentProperty, lastLine, lines);
        }
        if (currentInvariant) {
            this.updateSymbolRange(currentInvariant, lastLine, lines);
        }

        return symbols;
    }

    private getSectionSymbolKind(section: string): vscode.SymbolKind {
        switch (section) {
            case 'PURPOSE': return vscode.SymbolKind.String;
            case 'INPUTS': return vscode.SymbolKind.Variable;
            case 'GUARDS': return vscode.SymbolKind.Event;
            case 'LOGIC': return vscode.SymbolKind.Operator;
            case 'RETURNS': return vscode.SymbolKind.Constant;
            case 'DEPENDS': return vscode.SymbolKind.TypeParameter;
            case 'EDGE CASES': return vscode.SymbolKind.EnumMember;
            default: return vscode.SymbolKind.Key;
        }
    }

    private updateSymbolRange(
        symbol: vscode.DocumentSymbol,
        endLine: number,
        lines: string[]
    ): void {
        const startLine = symbol.range.start.line;
        symbol.range = new vscode.Range(
            startLine, 0,
            endLine, lines[endLine]?.length || 0
        );
    }
}
