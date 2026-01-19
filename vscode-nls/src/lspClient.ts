import * as vscode from 'vscode';
import * as cp from 'child_process';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
} from 'vscode-languageclient/node';

let client: LanguageClient | undefined;
let outputChannel: vscode.OutputChannel;

export function activateLspClient(context: vscode.ExtensionContext): void {
    try {
        // Create output channel immediately for visibility
        outputChannel = vscode.window.createOutputChannel('NLS Language Server');
        context.subscriptions.push(outputChannel);

        outputChannel.appendLine('NLS Language Server initializing...');
        outputChannel.appendLine(`Extension path: ${context.extensionPath}`);

    const nlscPath = vscode.workspace.getConfiguration('nls').get<string>('nlscPath', 'nlsc');

    // Check if nlsc is available
    outputChannel.appendLine(`Looking for nlsc at: ${nlscPath}`);

    try {
        const result = cp.spawnSync(nlscPath, ['--version'], {
            encoding: 'utf8',
            shell: true,
            timeout: 5000
        });

        if (result.error) {
            outputChannel.appendLine(`ERROR: Cannot find nlsc: ${result.error.message}`);
            outputChannel.appendLine('');
            outputChannel.appendLine('To enable hover, completions, and go-to-definition:');
            outputChannel.appendLine('  pip install nlsc');
            outputChannel.appendLine('');
            outputChannel.appendLine('Or specify the path in settings:');
            outputChannel.appendLine('  "nls.nlscPath": "/path/to/nlsc"');
            vscode.window.showWarningMessage(
                'NLS: nlsc not found. Install with: pip install nlsc',
                'Open Output'
            ).then(selection => {
                if (selection === 'Open Output') {
                    outputChannel.show();
                }
            });
            return;
        }

        const version = result.stdout?.trim() || result.stderr?.trim() || 'unknown';
        outputChannel.appendLine(`Found nlsc version: ${version}`);
    } catch (error) {
        outputChannel.appendLine(`ERROR checking nlsc: ${error}`);
        return;
    }

    // Server options - spawn nlsc lsp process
    const serverOptions: ServerOptions = {
        command: nlscPath,
        args: ['lsp'],
        options: { shell: true }
    };

    // Client options
    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'nl' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.nl'),
        },
        outputChannel: outputChannel,
    };

    // Create and start the client
    client = new LanguageClient(
        'nls-language-server',
        'NLS Language Server',
        serverOptions,
        clientOptions
    );

    outputChannel.appendLine('Starting NLS Language Server...');

    // Start the client
    client.start().then(() => {
        outputChannel.appendLine('NLS Language Server started successfully');
        outputChannel.appendLine('Hover, completions, and go-to-definition are now available');
    }).catch((error) => {
        outputChannel.appendLine(`ERROR: Failed to start NLS Language Server: ${error}`);
        outputChannel.appendLine('');
        outputChannel.appendLine('Make sure nlsc is installed with LSP support:');
        outputChannel.appendLine('  pip install nlsc');
        vscode.window.showWarningMessage(
            `NLS Language Server failed to start: ${error.message}`,
            'Open Output'
        ).then(selection => {
            if (selection === 'Open Output') {
                outputChannel.show();
            }
        });
    });

    context.subscriptions.push({
        dispose: () => {
            if (client) {
                client.stop();
            }
        }
    });
    } catch (error) {
        // Catch any initialization errors
        console.error('NLS LSP Client activation error:', error);
        if (outputChannel) {
            outputChannel.appendLine(`FATAL ERROR during activation: ${error}`);
        }
        vscode.window.showErrorMessage(`NLS Language Server failed to initialize: ${error}`);
    }
}

export function deactivateLspClient(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}

export function getClient(): LanguageClient | undefined {
    return client;
}
