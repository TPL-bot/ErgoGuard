const fs = require('fs');
const content = fs.readFileSync('index.html', 'utf8');
const scriptMatch = content.match(/<script>([\s\S]*?)<\/script>/);
if (scriptMatch) {
  const scriptContent = scriptMatch[1];
  // Try to parse as JavaScript to check syntax
  try {
    new Function(scriptContent);
    console.log('✅ JavaScript syntax is valid');
  } catch (e) {
    console.log('❌ JavaScript syntax error:', e.message);
  }
} else {
  console.log('⚠️  No script section found');
}
