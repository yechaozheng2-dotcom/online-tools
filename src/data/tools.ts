export interface Tool {
  slug: string;
  name: string;
  description: string;
  category: string;
  icon: string;
}

export const tools: Tool[] = [
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
    slug: 'password-generator',
    name: 'Password Generator',
    description: 'Generate strong, random passwords with custom rules. Uses crypto API.',
    category: 'Security',
    icon: '🔑',
  },
  {
    slug: 'color-picker',
    name: 'Color Picker',
    description: 'Pick colors and convert between HEX, RGB, HSL and CSS formats instantly.',
    category: 'Design',
    icon: '🎨',
  },
  {
    slug: 'qr-generator',
    name: 'QR Code Generator',
    description: 'Generate QR codes from any text or URL. Download as PNG instantly.',
    category: 'Utilities',
    icon: '▦',
  },
];

export const categories = [...new Set(tools.map(t => t.category))];
