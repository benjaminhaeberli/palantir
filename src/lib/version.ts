import { execSync } from 'node:child_process';
import pkg from '../../package.json';

/**
 * Version affichée sur le site, résolue AU BUILD (le frontmatter Astro s'exécute
 * dans Node, pas dans le navigateur — inutile de passer par une API).
 *
 * On lit le dernier tag git ; si git est absent ou sans tag (build depuis une
 * archive, ou clone superficiel), on retombe sur la version de package.json.
 *
 * ⚠ En CI, `actions/checkout` clone sans les tags par défaut : le workflow doit
 * préciser `fetch-depth: 0`, sinon la production affiche toujours le repli.
 */
const fromGit = (): string | null => {
  try {
    const tag = execSync('git describe --tags --abbrev=0', {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    return tag || null;
  } catch {
    return null;
  }
};

export const version = fromGit() ?? `v${pkg.version}`;
