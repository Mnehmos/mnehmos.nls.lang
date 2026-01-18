import * as vscode from "vscode";
import * as cp from "child_process";

export class DiagnosticsProvider implements vscode.Disposable {
  private diagnosticCollection: vscode.DiagnosticCollection;
  private disposables: vscode.Disposable[] = [];
  private nlscPath: string;
  private validateOnSave: boolean;
  private validateOnType: boolean;
  private validationTimeout: NodeJS.Timeout | undefined;

  constructor() {
    this.diagnosticCollection =
      vscode.languages.createDiagnosticCollection("nl");
    this.nlscPath = vscode.workspace
      .getConfiguration("nls")
      .get("nlscPath", "nlsc");
    this.validateOnSave = vscode.workspace
      .getConfiguration("nls")
      .get("validateOnSave", true);
    this.validateOnType = vscode.workspace
      .getConfiguration("nls")
      .get("validateOnType", false);

    // Validate on save
    this.disposables.push(
      vscode.workspace.onDidSaveTextDocument((doc) => {
        if (doc.languageId === "nl" && this.validateOnSave) {
          this.validate(doc);
        }
      }),
    );

    // Validate on type (debounced)
    this.disposables.push(
      vscode.workspace.onDidChangeTextDocument((e) => {
        if (e.document.languageId === "nl" && this.validateOnType) {
          this.scheduleValidation(e.document);
        }
      }),
    );

    // Clear diagnostics when document closes
    this.disposables.push(
      vscode.workspace.onDidCloseTextDocument((doc) => {
        this.diagnosticCollection.delete(doc.uri);
      }),
    );
  }

  updateConfiguration(): void {
    this.nlscPath = vscode.workspace
      .getConfiguration("nls")
      .get("nlscPath", "nlsc");
    this.validateOnSave = vscode.workspace
      .getConfiguration("nls")
      .get("validateOnSave", true);
    this.validateOnType = vscode.workspace
      .getConfiguration("nls")
      .get("validateOnType", false);
  }

  private scheduleValidation(document: vscode.TextDocument): void {
    if (this.validationTimeout) {
      clearTimeout(this.validationTimeout);
    }
    this.validationTimeout = setTimeout(() => {
      this.validate(document);
    }, 500);
  }

  validate(document: vscode.TextDocument): void {
    const filePath = document.uri.fsPath;

    cp.exec(
      `${this.nlscPath} verify "${filePath}" --json`,
      (error, stdout, stderr) => {
        const diagnostics: vscode.Diagnostic[] = [];

        try {
          // Parse JSON output from nlsc verify
          const result = JSON.parse(stdout);

          if (result.errors) {
            for (const err of result.errors) {
              const line = (err.line || 1) - 1;
              const range = new vscode.Range(line, 0, line, 1000);
              const diagnostic = new vscode.Diagnostic(
                range,
                err.message || "Parse error",
                vscode.DiagnosticSeverity.Error,
              );
              diagnostic.source = "nlsc";
              diagnostics.push(diagnostic);
            }
          }

          if (result.warnings) {
            for (const warn of result.warnings) {
              const line = (warn.line || 1) - 1;
              const range = new vscode.Range(line, 0, line, 1000);
              const diagnostic = new vscode.Diagnostic(
                range,
                warn.message || "Warning",
                vscode.DiagnosticSeverity.Warning,
              );
              diagnostic.source = "nlsc";
              diagnostics.push(diagnostic);
            }
          }
        } catch {
          // If JSON parsing fails, try to extract error info from stderr
          if (stderr && stderr.length > 0) {
            const lineMatch = /line (\d+)/i.exec(stderr);
            const line = lineMatch ? parseInt(lineMatch[1]) - 1 : 0;
            const range = new vscode.Range(line, 0, line, 1000);
            const diagnostic = new vscode.Diagnostic(
              range,
              stderr.trim(),
              vscode.DiagnosticSeverity.Error,
            );
            diagnostic.source = "nlsc";
            diagnostics.push(diagnostic);
          }
        }

        this.diagnosticCollection.set(document.uri, diagnostics);
      },
    );
  }

  dispose(): void {
    if (this.validationTimeout) {
      clearTimeout(this.validationTimeout);
    }
    this.diagnosticCollection.dispose();
    this.disposables.forEach((d) => d.dispose());
  }
}
