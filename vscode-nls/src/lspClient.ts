import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
} from 'vscode-languageclient/node';

let client: LanguageClient | undefined;

export function activateLspClient(context: vscode.ExtensionContext): void {
    const nlscPath = vscode.workspace.getConfiguration('nls').get<string>('nlscPath', 'nlsc');
    
    // Server options - spawn nlsc lsp process
    // nlsc lsp defaults to stdio transport, so no extra args needed
    const serverOptions: ServerOptions = {
        command: nlscPath,
        args: ['lsp'],
    };
    
    // Client options
    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'nl' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.nl'),
        },
        outputChannelName: 'NLS Language Server',
    };
    
    // Create and start the client
    client = new LanguageClient(
        'nls-language-server',
        'NLS Language Server',
        serverOptions,
        clientOptions
    );
    
    // Start the client
    client.start().then(() => {
        console.log('NLS Language Server started');
    }).catch((error) => {
        console.error('Failed to start NLS Language Server:', error);
        vscode.window.showWarningMessage(
            `NLS Language Server failed to start. Make sure nlsc is installed: pip install nlsc[lsp]`
        );
    });
    
    context.subscriptions.push({
        dispose: () => {
            if (client) {
                client.stop();
            }
        }
    });
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
