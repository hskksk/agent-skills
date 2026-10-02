#!/usr/bin/env node

import { execFileSync } from 'node:child_process';

const version = process.argv[2];

if (!version) {
  throw new Error('Usage: node scripts/prepare-release.mjs <semver>');
}

const repository = process.env.GITHUB_REPOSITORY;
if (!repository) {
  throw new Error(
    'GITHUB_REPOSITORY is not set. Release runs on GitHub Actions where it is provided automatically.',
  );
}

const sinceTag = (() => {
  try {
    return execFileSync('git', ['describe', '--tags', '--abbrev=0'], {
      encoding: 'utf8',
    }).trim();
  } catch {
    return '';
  }
})();

const artifactBaseUrl = `https://github.com/${repository}/releases/download/v${version}`;

execFileSync('node', ['scripts/bump-skill-versions.mjs', version, sinceTag], {
  stdio: 'inherit',
});

execFileSync('node', ['scripts/build-discovery-index.mjs', artifactBaseUrl], {
  stdio: 'inherit',
  env: { ...process.env, AGENT_SKILLS_SOURCE: 'worktree' },
});
