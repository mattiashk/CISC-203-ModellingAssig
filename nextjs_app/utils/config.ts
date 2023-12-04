import fs from 'fs';
import path from 'path';

export function loadConfig() {
  const filePath = path.join(process.cwd(), 'config.json');
  const jsonString = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(jsonString);
}
