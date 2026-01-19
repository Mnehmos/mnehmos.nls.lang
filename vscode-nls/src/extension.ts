import * as vscode from 'vscode';
import { DiagnosticsProvider } from './diagnostics';
import { NLDocumentSymbolProvider } from './documentSymbols';
import { NLFoldingRangeProvider } from './folding';
import { registerCommands } from './commands';
import { activateLspClient, deactivateLspClient } from './lspClient';

let diagnosticsProvider: DiagnosticsProvider;

export function activate(context: vscode.ExtensionContext): void {
    console.log('NLS extension activating...');

    // Create main extension output channel for debugging
    const mainChannel = vscode.window.createOutputChannel('NLS Extension');
    context.subscriptions.push(mainChannel);
    mainChannel.appendLine(`NLS extension activating at ${new Date().toISOString()}`);
    mainChannel.appendLine(`Extension path: ${context.extensionPath}`);

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

    // Set up diagnostics (nlsc verify integration) as fallback
    diagnosticsProvider = new DiagnosticsProvider();
    context.subscriptions.push(diagnosticsProvider);

    // Register commands
    registerCommands(context, diagnosticsProvider);

    // Start LSP client for hover, definition, completions
    // LSP also provides diagnostics, so it may override the fallback
    activateLspClient(context);

    // Watch for configuration changes
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('nls')) {
                diagnosticsProvider.updateConfiguration();
            }
        })
    );

    mainChannel.appendLine('NLS extension activated successfully');
    console.log('NLS extension activated');
}

export function deactivate(): Thenable<void> | undefined {
    if (diagnosticsProvider) {
        diagnosticsProvider.dispose();
    }
    return deactivateLspClient();
}

