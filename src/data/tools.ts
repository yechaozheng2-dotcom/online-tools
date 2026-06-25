export interface Tool {
  slug: string;
  name: string;
  description: string;
  category: string;
  icon: string;
}

export const tools: Tool[] = [
  // Developer
  { slug: 'json-formatter',        name: 'JSON Formatter',           description: 'Format, validate and minify JSON instantly.',                          category: 'Developer',  icon: '{ }' },
  { slug: 'url-encoder',           name: 'URL Encoder / Decoder',    description: 'Encode and decode URLs with UTF-8 support.',                           category: 'Developer',  icon: '🔗' },
  { slug: 'timestamp-converter',   name: 'Timestamp Converter',      description: 'Convert Unix timestamps to readable dates and back.',                   category: 'Developer',  icon: '⏱' },
  { slug: 'base64',                name: 'Base64 Encoder / Decoder', description: 'Encode and decode Base64 strings instantly.',                          category: 'Developer',  icon: '64' },
  { slug: 'jwt-decoder',           name: 'JWT Decoder',              description: 'Decode and inspect JSON Web Tokens.',                                   category: 'Developer',  icon: '🪙' },
  { slug: 'regex-tester',          name: 'Regex Tester',             description: 'Test regular expressions with live match highlighting.',                category: 'Developer',  icon: '.*' },
  { slug: 'number-base-converter', name: 'Number Base Converter',    description: 'Convert between binary, octal, decimal and hexadecimal.',               category: 'Developer',  icon: '01' },
  { slug: 'html-entity',           name: 'HTML Entity Encoder',      description: 'Encode and decode HTML entities like &amp; &lt; &gt;.',                 category: 'Developer',  icon: '&' },
  { slug: 'cron-parser',           name: 'Cron Expression Parser',   description: 'Parse cron expressions and preview next execution times.',              category: 'Developer',  icon: '⏰' },
  { slug: 'chmod-calculator',      name: 'Chmod Calculator',         description: 'Convert Unix file permissions between rwx and numeric notation.',       category: 'Developer',  icon: '🔐' },
  { slug: 'css-unit-converter',    name: 'CSS Unit Converter',       description: 'Convert between px, rem, em, vw and pt units.',                        category: 'Developer',  icon: 'px' },
  { slug: 'svg-to-datauri',        name: 'SVG to Data URI',          description: 'Convert SVG code to Base64 Data URI for use in CSS.',                  category: 'Developer',  icon: '◈' },
  // Text
  { slug: 'word-counter',          name: 'Word Counter',             description: 'Count words, characters, lines and estimate reading time.',             category: 'Text',       icon: '¶' },
  { slug: 'case-converter',        name: 'Case Converter',           description: 'Convert text between camelCase, snake_case, UPPER, Title and more.',   category: 'Text',       icon: 'Aa' },
  { slug: 'lorem-ipsum',           name: 'Lorem Ipsum Generator',    description: 'Generate placeholder text with custom paragraph and word count.',       category: 'Text',       icon: '✍' },
  { slug: 'text-diff',             name: 'Text Diff',                description: 'Compare two texts and highlight the differences.',                      category: 'Text',       icon: '⟺' },
  { slug: 'markdown-preview',      name: 'Markdown Preview',         description: 'Write Markdown and see the rendered HTML preview in real time.',        category: 'Text',       icon: 'M↓' },
  { slug: 'slug-generator',        name: 'Slug Generator',           description: 'Convert any text to a URL-friendly slug.',                              category: 'Text',       icon: '-_-' },
  // Math
  { slug: 'unit-converter',        name: 'Unit Converter',           description: 'Convert length, weight, temperature and area units.',                   category: 'Math',       icon: '⇄' },
  { slug: 'percentage-calculator', name: 'Percentage Calculator',    description: 'Calculate percentages, increases and decreases instantly.',             category: 'Math',       icon: '%' },
  { slug: 'roman-numeral',         name: 'Roman Numeral Converter',  description: 'Convert between Arabic numbers and Roman numerals.',                    category: 'Math',       icon: 'Ⅷ' },
  { slug: 'age-calculator',        name: 'Age Calculator',           description: 'Calculate exact age in years, months and days from a birthdate.',       category: 'Math',       icon: '🎂' },
  { slug: 'tip-calculator',        name: 'Tip Calculator',           description: 'Calculate tip amount and split the bill between any number of people.', category: 'Math',       icon: '🍽' },
  { slug: 'bmi-calculator',        name: 'BMI Calculator',           description: 'Calculate Body Mass Index with metric and imperial units.',             category: 'Math',       icon: '⚖' },
  // Security
  { slug: 'password-generator',    name: 'Password Generator',       description: 'Generate strong random passwords with custom rules.',                   category: 'Security',   icon: '🔑' },
  { slug: 'hash-generator',        name: 'Hash Generator',           description: 'Generate SHA-256, SHA-512 and SHA-1 hashes from any text.',             category: 'Security',   icon: '#' },
  { slug: 'uuid-generator',        name: 'UUID Generator',           description: 'Generate UUID v4 identifiers. Bulk generation supported.',              category: 'Security',   icon: '⬡' },
  // Design
  { slug: 'color-picker',          name: 'Color Picker & Converter', description: 'Pick colors and convert between HEX, RGB and HSL.',                    category: 'Design',     icon: '🎨' },
  { slug: 'contrast-checker',      name: 'Contrast Checker',         description: 'Check color contrast ratio and WCAG AA/AAA compliance.',                category: 'Design',     icon: '◑' },
  { slug: 'css-shadow-generator',  name: 'CSS Shadow Generator',     description: 'Visually build box-shadow and copy the CSS instantly.',                 category: 'Design',     icon: '□' },
  { slug: 'css-gradient-generator',name: 'CSS Gradient Generator',   description: 'Generate linear and radial CSS gradients visually.',                   category: 'Design',     icon: '▤' },
  { slug: 'border-radius-generator',name: 'Border Radius Generator', description: 'Visually build CSS border-radius with live preview and copy.',          category: 'Design',     icon: '▢' },
  { slug: 'tint-shade-generator',  name: 'Tint & Shade Generator',   description: 'Generate tints and shades from any color for design systems.',          category: 'Design',     icon: '◫' },
  // Utilities
  { slug: 'qr-generator',          name: 'QR Code Generator',        description: 'Generate QR codes from any text or URL. Download as PNG.',             category: 'Utilities',  icon: '▦' },
  { slug: 'countdown-timer',       name: 'Countdown Timer',          description: 'Set a countdown timer with alarm. Runs entirely in your browser.',     category: 'Utilities',  icon: '⏳' },
  { slug: 'stopwatch',             name: 'Stopwatch',                description: 'Precision stopwatch with lap times. Runs entirely in your browser.',   category: 'Utilities',  icon: '🏁' },
];

export const categories = [...new Set(tools.map(t => t.category))];
