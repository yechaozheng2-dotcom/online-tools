export interface Tool {
  slug: string;
  name: string;
  description: string;
  category: string;
  icon: string;
}

export const tools: Tool[] = [
  // Developer
  {
    slug: 'json-formatter',
    name: 'JSON Formatter',
    description: 'Format, validate and minify JSON instantly. Runs in your browser.',
    category: 'Developer',
    icon: '{ }',
  },
  {
    slug: 'url-encoder',
    name: 'URL Encoder / Decoder',
    description: 'Encode and decode URLs and query strings with UTF-8 support.',
    category: 'Developer',
    icon: '🔗',
  },
  {
    slug: 'timestamp-converter',
    name: 'Timestamp Converter',
    description: 'Convert Unix timestamps to readable dates and back. Supports multiple timezones.',
    category: 'Developer',
    icon: '⏱',
  },
  {
    slug: 'base64',
    name: 'Base64 Encoder / Decoder',
    description: 'Encode and decode Base64 strings and files instantly in your browser.',
    category: 'Developer',
    icon: '64',
  },
  {
    slug: 'jwt-decoder',
    name: 'JWT Decoder',
    description: 'Decode and inspect JSON Web Tokens. View header, payload and signature.',
    category: 'Developer',
    icon: '🪙',
  },
  {
    slug: 'regex-tester',
    name: 'Regex Tester',
    description: 'Test and debug regular expressions with live match highlighting.',
    category: 'Developer',
    icon: '.*',
  },
  {
    slug: 'number-base-converter',
    name: 'Number Base Converter',
    description: 'Convert numbers between binary, octal, decimal and hexadecimal.',
    category: 'Developer',
    icon: '01',
  },
  // Security
  {
    slug: 'password-generator',
    name: 'Password Generator',
    description: 'Generate strong, random passwords with custom rules. Uses crypto API.',
    category: 'Security',
    icon: '🔑',
  },
  {
    slug: 'hash-generator',
    name: 'Hash Generator',
    description: 'Generate SHA-256, SHA-512 and SHA-1 hashes from any text. Uses Web Crypto API.',
    category: 'Security',
    icon: '#',
  },
  {
    slug: 'uuid-generator',
    name: 'UUID Generator',
    description: 'Generate UUID v4 identifiers instantly. Bulk generation supported.',
    category: 'Security',
    icon: '⬡',
  },
  // Design
  {
    slug: 'color-picker',
    name: 'Color Picker & Converter',
    description: 'Pick colors and convert between HEX, RGB, HSL and CSS formats instantly.',
    category: 'Design',
    icon: '🎨',
  },
  // Utilities
  {
    slug: 'qr-generator',
    name: 'QR Code Generator',
    description: 'Generate QR codes from any text or URL. Download as PNG instantly.',
    category: 'Utilities',
    icon: '▦',
  },
];

export const categories = [...new Set(tools.map(t => t.category))];
