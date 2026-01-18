import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';
import { DiagnosticsProvider } from './diagnostics';

export function registerCommands(
    context: vscode.ExtensionContext,
    diagnosticsProvider: DiagnosticsProvider
): void {
    const nlscPath = () => vscode.workspace.getConfiguration('nls').get('nlscPath', 'nlsc');
    
    // NLS: Verify Current File
    context.subscriptions.push(
        vscode.commands.registerCommand('nls.verify', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor || editor.document.languageId !== 'nl') {
                vscode.window.showWarningMessage('No .nl file is open');
                return;
            }
            
            await editor.document.save();
            diagnosticsProvider.validate(editor.document);
            vscode.window.showInformationMessage('NLS: Verification complete');
        })
    );
    
    // NLS: Compile to Python
    context.subscriptions.push(
        vscode.commands.registerCommand('nls.compile', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor || editor.document.languageId !== 'nl') {
                vscode.window.showWarningMessage('No .nl file is open');
                return;
            }
            
            await editor.document.save();
            const filePath = editor.document.uri.fsPath;
            
            const terminal = vscode.window.createTerminal('NLS Compile');
            terminal.show();
            terminal.sendText(`${nlscPath()} compile "${filePath}"`);
        })
    );
    
    // NLS: Run Tests
    context.subscriptions.push(
        vscode.commands.registerCommand('nls.test', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor || editor.document.languageId !== 'nl') {
                vscode.window.showWarningMessage('No .nl file is open');
                return;
            }
            
            await editor.document.save();
            const filePath = editor.document.uri.fsPath;
            
            const terminal = vscode.window.createTerminal('NLS Test');
            terminal.show();
            terminal.sendText(`${nlscPath()} test "${filePath}"`);
        })
    );
    
    // NLS: Show Dependency Graph
    context.subscriptions.push(
        vscode.commands.registerCommand('nls.graph', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor || editor.document.languageId !== 'nl') {
                vscode.window.showWarningMessage('No .nl file is open');
                return;
            }
            
            await editor.document.save();
            const filePath = editor.document.uri.fsPath;
            
            const terminal = vscode.window.createTerminal('NLS Graph');
            terminal.show();
            terminal.sendText(`${nlscPath()} graph "${filePath}"`);
        })
    );
    
    // NLS: Open Generated Python File
    context.subscriptions.push(
        vscode.commands.registerCommand('nls.openGenerated', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor || editor.document.languageId !== 'nl') {
                vscode.window.showWarningMessage('No .nl file is open');
                return;
            }
            
            const nlPath = editor.document.uri.fsPath;
            const pyPath = nlPath.replace(/\.nl$/, '.py');
            
            try {
                const doc = await vscode.workspace.openTextDocument(pyPath);
                await vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
            } catch {
                vscode.window.showWarningMessage(`Generated file not found: ${path.basename(pyPath)}`);
            }
        })
    );
}
