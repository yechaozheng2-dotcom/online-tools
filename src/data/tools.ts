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
    description: 'Format, validate and minify JSON instantly in your browser. No data sent to server.',
    category: 'Developer',
    icon: '{ }',
  },
];

export const categories = [...new Set(tools.map(t => t.category))];
