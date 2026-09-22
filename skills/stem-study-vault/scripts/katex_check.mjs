import fs from 'node:fs';
import path from 'node:path';
import katex from 'katex';

const EXCLUDED_TREES = new Set([
  'Templates',
  'source-original',
  'source-historical',
  'extracted-text',
]);
const EXCLUDED_RELATIVE_TREES = new Set([
  'Sources/Original',
  'Sources/Historical',
  'Sources/Historical ELEC271',
  'Sources/Extracted',
]);
const BARE_COMMAND = /\\(frac|sum|int|omega|mathrm|begin|end)(?![A-Za-z])/g;

function usageError(message) {
  console.error(message);
  process.exit(2);
}

function walk(directory, root = directory) {
  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if (entry.name.startsWith('.') || entry.name === 'node_modules' || entry.isSymbolicLink()) continue;
    const absolute = path.join(directory, entry.name);
    const relative = path.relative(root, absolute).split(path.sep).join('/');
    if (entry.isDirectory()) {
      if (!EXCLUDED_TREES.has(entry.name) && !EXCLUDED_RELATIVE_TREES.has(relative)) {
        files.push(...walk(absolute, root));
      }
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(absolute);
    }
  }
  return files;
}

function blank(match) {
  return match.replace(/[^\r\n]/g, ' ');
}

function stripCode(text) {
  let fence = null;
  const lines = text.match(/[^\r\n]*(?:\r\n|\r|\n|$)/g) ?? [];
  const withoutFences = lines.map((line) => {
    if (fence) {
      const closesFence = new RegExp(
        `^ {0,3}${fence.character}{${fence.length},}[ \\t]*(?:\\r\\n|\\r|\\n|$)`,
      ).test(line);
      const redacted = blank(line);
      if (closesFence) fence = null;
      return redacted;
    }

    const openingFence = line.match(/^ {0,3}(`{3,}|~{3,})[^\r\n]*(?:\r\n|\r|\n|$)/);
    if (!openingFence) return line;
    fence = {
      character: openingFence[1][0],
      length: openingFence[1].length,
    };
    return blank(line);
  }).join('');

  return stripInlineCode(withoutFences);
}

function stripInlineCode(text) {
  let result = '';
  let index = 0;

  while (index < text.length) {
    if (text[index] !== '`') {
      result += text[index];
      index += 1;
      continue;
    }

    let openingLength = 1;
    while (text[index + openingLength] === '`') openingLength += 1;
    let closing = -1;
    for (let cursor = index + openingLength; cursor < text.length; cursor += 1) {
      if (text[cursor] !== '`') continue;
      let closingLength = 1;
      while (text[cursor + closingLength] === '`') closingLength += 1;
      if (closingLength === openingLength) {
        closing = cursor;
        break;
      }
      cursor += closingLength - 1;
    }

    if (closing === -1) return result + blank(text.slice(index));
    result += blank(text.slice(index, closing + openingLength));
    index = closing + openingLength;
  }
  return result;
}

function lineNumber(text, offset) {
  return (text.slice(0, offset).match(/\r\n|\r|\n/g)?.length ?? 0) + 1;
}

function normalized(formula) {
  return formula.replace(/\s+/g, ' ').trim();
}

function isEscaped(text, index) {
  let backslashes = 0;
  for (let cursor = index - 1; cursor >= 0 && text[cursor] === '\\'; cursor -= 1) {
    backslashes += 1;
  }
  return backslashes % 2 === 1;
}

function delimiterAt(text, index) {
  if (text[index] === '$' && !isEscaped(text, index)) {
    return text[index + 1] === '$'
      ? { value: '$$', kind: 'both', displayMode: true }
      : { value: '$', kind: 'both', displayMode: false };
  }

  if (text[index] === '\\' && !isEscaped(text, index)) {
    const delimiters = {
      '[': { value: '\\[', kind: 'open', close: '\\]', displayMode: true },
      ']': { value: '\\]', kind: 'close' },
      '(': { value: '\\(', kind: 'open', close: '\\)', displayMode: false },
      ')': { value: '\\)', kind: 'close' },
    };
    return delimiters[text[index + 1]];
  }

  return null;
}

function errorContext(text, start) {
  const lineEnd = text.indexOf('\n', start);
  return normalized(text.slice(start, lineEnd === -1 ? text.length : lineEnd));
}

function delimiterError(file, text, index, delimiter, message) {
  return {
    file,
    line: lineNumber(text, index),
    formula: errorContext(text, index) || delimiter,
    message: `${message}: ${delimiter}`,
  };
}

function collectMath(text, file, errors) {
  const spans = [];
  const maskedRanges = [];
  let opening = null;

  for (let index = 0; index < text.length; index += 1) {
    const delimiter = delimiterAt(text, index);
    if (!delimiter) continue;

    if (!opening) {
      if (delimiter.kind === 'close') {
        errors.push(delimiterError(file, text, index, delimiter.value, 'Unmatched closing math delimiter'));
        maskedRanges.push({ start: index, end: index + delimiter.value.length });
      } else {
        opening = { ...delimiter, start: index, contentStart: index + delimiter.value.length };
      }
    } else if (delimiter.value === (opening.close ?? opening.value)) {
      spans.push({
        start: opening.start,
        end: index + delimiter.value.length,
        formula: text.slice(opening.contentStart, index),
        displayMode: opening.displayMode,
      });
      opening = null;
    }
    index += delimiter.value.length - 1;
  }

  if (opening) {
    errors.push(delimiterError(file, text, opening.start, opening.value, 'Unmatched opening math delimiter'));
    maskedRanges.push({ start: opening.start, end: text.length });
  }
  return { spans, maskedRanges };
}

function checkFile(file, errors) {
  const text = stripCode(fs.readFileSync(file, 'utf8'));
  const { spans, maskedRanges } = collectMath(text, file, errors);
  const outsideMath = text.split('');

  for (const range of [...spans, ...maskedRanges]) {
    outsideMath.fill(' ', range.start, range.end);
  }
  for (const span of spans) {
    const formula = normalized(span.formula);
    try {
      katex.renderToString(formula, { throwOnError: true, displayMode: span.displayMode });
    } catch (error) {
      errors.push({
        file,
        line: lineNumber(text, span.start),
        formula,
        message: error.message,
      });
    }
  }

  const bareText = outsideMath.join('');
  for (const match of bareText.matchAll(BARE_COMMAND)) {
    if (isEscaped(bareText, match.index)) continue;
    const command = match[0];
    errors.push({
      file,
      line: lineNumber(text, match.index),
      formula: command,
      message: `Bare KaTeX command outside math span: ${command}`,
    });
  }
  return spans.length;
}

const target = process.argv[2];
if (!target) usageError('Missing path: provide a directory to check.');
if (!fs.existsSync(target)) usageError(`Missing path: ${target}`);
if (!fs.statSync(target).isDirectory()) usageError(`Not a directory: ${target}`);

const errors = [];
const files = walk(target);
const formulas = files.reduce((total, file) => total + checkFile(file, errors), 0);
console.log(JSON.stringify({ files: files.length, formulas, errors }));
process.exitCode = errors.length > 0 ? 1 : 0;
