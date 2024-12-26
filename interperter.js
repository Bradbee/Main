const MainInterpreter = {
    variables: {},
    functions: {},
    
    evalExpr: function(expr) {
        try {
            return eval(expr);
        } catch (e) {
            return `Error evaluating expression: ${e.message}`;
        }
    },
    
    execLine: function(line) {
        const tokens = line.trim().split(/\s+/);
        if (tokens.length === 0) return '';

        const cmd = tokens[0];
        
        if (cmd === 'let') {
            const varName = tokens[1];
            const value = this.evalExpr(tokens.slice(3).join(' '));
            this.variables[varName] = value;
            return '';
        } else if (cmd === 'function') {
            const funcName = tokens[1];
            this.functions[funcName] = line;
            return '';
        } else if (cmd in this.functions) {
            return this.execFunction(cmd, tokens.slice(1));
        } else if (cmd === 'if') {
            const condition = tokens.slice(1).join(' ');
            if (this.evalExpr(condition)) {
                return this.execLines();
            }
            return '';
        } else if (cmd === 'print') {
            const toPrint = tokens.slice(1).join(' ');
            return `${this.evalExpr(toPrint)}\n`;
        } else if (cmd === 'asm') {
            return `Simulated assembly: ${tokens.slice(1).join(' ')}\n`;
        }
    },
    
    execFunction: function(funcName, args) {
        const func = this.functions[funcName];
        const [_, , ...funcBody] = func.split(/\s+/);
        return this.execLines(funcBody.join(' ').split(';'));
    },
    
    execLines: function(lines) {
        let output = '';
        for (const line of lines) {
            output += this.execLine(line);
        }
        return output;
    },
    
    run: function(code) {
        this.variables = {};
        this.functions = {};
        return this.execLines(code.trim().split('\n'));
    }
};
