import * as vscode from 'vscode';
import { DiagnosticsProvider } from './diagnostics';
import { NLDocumentSymbolProvider } from './documentSymbols';
import { NLFoldingRangeProvider } from './folding';
import { registerCommands } from './commands';

let diagnosticsProvider: DiagnosticsProvider;

export function activate(context: vscode.ExtensionContext): void {
    console.log('NLS extension activating...');

    // Register document symbol provider (outline view)
    const symbolProvider = new NLDocumentSymbolProvider();
    context.subscriptions.push(
        vscode.languages.registerDocumentSymbolProvider(
            { language: 'nl' },
            symbolProvider
        )
    );

    // Register folding provider
    const foldingProvider = new NLFoldingRangeProvider();
    context.subscriptions.push(
        vscode.languages.registerFoldingRangeProvider(
            { language: 'nl' },
            foldingProvider
        )
    );

    // Set up diagnostics (nlsc verify integration)
    diagnosticsProvider = new DiagnosticsProvider();
    context.subscriptions.push(diagnosticsProvider);

    // Register commands
    registerCommands(context, diagnosticsProvider);

    // Watch for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('nls')) {
                diagnosticsProvider.updateConfiguration();
            }
        })
    );

    console.log('NLS extension activated');
}

export function deactivate(): void {
    if (diagnosticsProvider) {
        diagnosticsProvider.dispose();
    }
}
