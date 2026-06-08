import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// rehype plugin maison : enveloppe chaque <table> dans un
// <div class="table-scroll"> pour la rendre scrollable horizontalement
// (overflow-x:auto via global.css) sans casser le rendu desktop.
function rehypeWrapTables() {
  const wrap = node => {
    if (!node.children) return;
    node.children = node.children.map(child => {
      wrap(child);
      if (child.type === 'element' && child.tagName === 'table') {
        return {
          type: 'element',
          tagName: 'div',
          properties: { className: ['table-scroll'] },
          children: [child],
        };
      }
      return child;
    });
  };
  return tree => wrap(tree);
}

// https://astro.build/config
export default defineConfig({
  site: 'https://palantir-rpg.com',
  base: '/',
  trailingSlash: 'never',
  integrations: [mdx(), sitemap()],
  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
    rehypePlugins: [rehypeWrapTables],
  },
});
