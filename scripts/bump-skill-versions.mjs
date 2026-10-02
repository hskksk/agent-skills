#!/usr/bin/env node

import { execFileSync } from 'node:child_process';
import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { parse, stringify } from 'yaml';

const version = process.argv[2];
const sinceTag = process.argv[3] ?? '';

if (!version) {
  throw new Error(
    'Usage: node scripts/bump-skill-versions.mjs <semver> [sinceGitTag]',
  );
}

if (!/^\d+\.\d+\.\d+/.test(version)) {
  throw new Error(`Not a semver release version: ${version}`);
}

const listAllSkills = () =>
  readdirSync('skills', { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();

const changedSkills = (tag) => {
  if (!tag || tag === 'undefined' || tag === 'null') {
    return listAllSkills();
  }

  try {
    const output = execFileSync(
      'git',
      ['diff', '--name-only', tag, 'HEAD', '--', 'skills/'],
      { encoding: 'utf8' },
    ).trim();

    if (!output) {
      return [];
    }

    const names = new Set();
    for (const line of output.split('\n')) {
      const match = line.match(/^skills\/([^/]+)\//);
      if (match) {
        names.add(match[1]);
      }
    }
    return [...names].sort();
  } catch {
    return listAllSkills();
  }
};

const bumpSkill = (directory, nextVersion) => {
  const path = join('skills', directory, 'SKILL.md');
  const content = readFileSync(path, 'utf8');
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---(\r?\n[\s\S]*)$/);
  if (!match) {
    throw new Error(`Missing frontmatter in ${path}`);
  }

  const frontmatter = parse(match[1]);
  if (!frontmatter || typeof frontmatter !== 'object' || Array.isArray(frontmatter)) {
    throw new Error(`Invalid frontmatter in ${path}`);
  }

  if (frontmatter.metadata === undefined) {
    frontmatter.metadata = {};
  }
  if (
    typeof frontmatter.metadata !== 'object' ||
    Array.isArray(frontmatter.metadata)
  ) {
    throw new Error(`metadata must be a string map in ${path}`);
  }

  frontmatter.metadata.version = nextVersion;
  const body = match[2].startsWith('\r\n') ? match[2] : `\n${match[2]}`;
  writeFileSync(
    path,
    `---\n${stringify(frontmatter, { lineWidth: 0 }).trimEnd()}\n---${body}`,
  );
  console.log(`Set skills/${directory}/SKILL.md metadata.version to ${nextVersion}`);
};

const targets = changedSkills(sinceTag);
if (targets.length === 0) {
  console.log('No changes under skills/ since last release; skip version bumps.');
  process.exit(0);
}

for (const directory of targets) {
  bumpSkill(directory, version);
}
