#!/usr/bin/env node

import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import {
  mkdirSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from 'node:fs';
import { join } from 'node:path';
import { parse } from 'yaml';

const schema = 'https://schemas.agentskills.io/discovery/0.2.0/schema.json';
const baseUrl = process.argv[2];
const outputDirectory = 'dist';
const useWorktree = process.env.AGENT_SKILLS_SOURCE === 'worktree';
const archiveEnvironment = {
  ...process.env,
  GIT_AUTHOR_DATE: '2000-01-01T00:00:00Z',
  GIT_AUTHOR_EMAIL: 'agent-skills@users.noreply.github.com',
  GIT_AUTHOR_NAME: 'agent-skills',
  GIT_COMMITTER_DATE: '2000-01-01T00:00:00Z',
  GIT_COMMITTER_EMAIL: 'agent-skills@users.noreply.github.com',
  GIT_COMMITTER_NAME: 'agent-skills',
};

if (!baseUrl) {
  throw new Error(
    'Usage: node scripts/build-discovery-index.mjs <artifact-base-url>',
  );
}

const git = (args, options = {}) =>
  execFileSync('git', args, { encoding: 'utf8', ...options });

const readSkillText = (directory, relativePath) => {
  if (useWorktree) {
    return readFileSync(join('skills', directory, relativePath), 'utf8');
  }
  return git(['show', `HEAD:skills/${directory}/${relativePath}`]);
};

const readSkillBytes = (directory, relativePath) => {
  if (useWorktree) {
    return readFileSync(join('skills', directory, relativePath));
  }
  return execFileSync('git', ['show', `HEAD:skills/${directory}/${relativePath}`]);
};

const listSkillDirectories = () => {
  if (useWorktree) {
    return readdirSync('skills', { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
      .sort();
  }

  return git(['ls-tree', '-d', '--name-only', 'HEAD:skills'])
    .trim()
    .split('\n')
    .filter(Boolean);
};

const listSkillFiles = (directory) => {
  if (useWorktree) {
    const root = join('skills', directory);
    const files = [];
    const walk = (current, prefix) => {
      for (const entry of readdirSync(current, { withFileTypes: true })) {
        const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
        const absolute = join(current, entry.name);
        if (entry.isDirectory()) {
          walk(absolute, relative);
        } else {
          files.push(relative);
        }
      }
    };
    walk(root, '');
    return files.sort();
  }

  return git(['ls-tree', '-r', `HEAD:skills/${directory}`])
    .trim()
    .split('\n')
    .filter(Boolean)
    .map((entry) => entry.slice(entry.indexOf('\t') + 1));
};

const readMetadata = (directory) => {
  const path = `skills/${directory}/SKILL.md`;
  const source = readSkillText(directory, 'SKILL.md');
  const frontmatter = source.match(/^---\r?\n([\s\S]*?)\r?\n---/)?.[1];
  if (!frontmatter) throw new Error(`Missing frontmatter in ${path}`);

  let metadata;
  try {
    metadata = parse(frontmatter);
  } catch (error) {
    throw new Error(`Invalid frontmatter in ${path}`, { cause: error });
  }

  if (!metadata || typeof metadata !== 'object' || Array.isArray(metadata)) {
    throw new Error(`Invalid frontmatter in ${path}`);
  }

  const { name, description } = metadata;
  if (typeof name !== 'string' || typeof description !== 'string') {
    throw new Error(`Missing name or description in ${path}`);
  }

  if (name !== directory) {
    throw new Error(
      `Skill name "${name}" must match directory skills/${directory}`,
    );
  }

  if (
    name.length === 0 ||
    name.length > 64 ||
    !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name) ||
    description.length === 0 ||
    description.length > 1024
  ) {
    throw new Error(`Invalid name or description in ${path}`);
  }

  if (
    metadata.compatibility !== undefined &&
    (typeof metadata.compatibility !== 'string' ||
      metadata.compatibility.length === 0 ||
      metadata.compatibility.length > 500)
  ) {
    throw new Error(`Invalid compatibility in ${path}`);
  }

  if (metadata['allowed-tools'] !== undefined) {
    if (
      typeof metadata['allowed-tools'] !== 'string' ||
      metadata['allowed-tools'].length === 0
    ) {
      throw new Error(`allowed-tools must be a space-separated string in ${path}`);
    }
  }

  if (metadata.metadata !== undefined) {
    const extra = metadata.metadata;
    if (!extra || typeof extra !== 'object' || Array.isArray(extra)) {
      throw new Error(`metadata must be a string map in ${path}`);
    }
    for (const [key, value] of Object.entries(extra)) {
      if (typeof value !== 'string') {
        throw new Error(`metadata.${key} must be a string in ${path}`);
      }
    }
    if (
      extra.version !== undefined &&
      !/^\d+\.\d+\.\d+/.test(extra.version)
    ) {
      throw new Error(`metadata.version must be semver in ${path}`);
    }
  }

  return { name, description, source };
};

const assertReferencesExist = (directory, source, files) => {
  const fileSet = new Set(files);
  const referenced = source.matchAll(
    /`((?:references|scripts|assets)\/[^`\s]+)`/g,
  );
  for (const match of referenced) {
    const relativePath = match[1];
    if (!fileSet.has(relativePath)) {
      throw new Error(
        `skills/${directory}/SKILL.md references missing file ${relativePath}`,
      );
    }
  }
};

const createArchiveFromGit = (directory) => {
  const tree = git(['rev-parse', `HEAD:skills/${directory}`]).trim();
  const commit = git(['commit-tree', tree], {
    encoding: 'utf8',
    env: archiveEnvironment,
    input: 'Agent Skills archive\n',
  }).trim();
  const tar = execFileSync('git', ['archive', '--format=tar', commit]);
  return execFileSync('gzip', ['-n', '-9', '-c'], { input: tar });
};

const createArchiveFromWorktree = (directory) => {
  const tar = execFileSync('tar', ['-c', '-f', '-', '.'], {
    cwd: join('skills', directory),
  });
  return execFileSync('gzip', ['-n', '-9', '-c'], { input: tar });
};

const createArtifact = (directory, source) => {
  const files = listSkillFiles(directory);
  if (files.length === 0) {
    throw new Error(`No files in skills/${directory}`);
  }

  assertReferencesExist(directory, source, files);

  if (files.length === 1 && files[0] === 'SKILL.md') {
    return {
      content: readSkillBytes(directory, 'SKILL.md'),
      extension: 'md',
      type: 'skill-md',
    };
  }

  return {
    content: useWorktree
      ? createArchiveFromWorktree(directory)
      : createArchiveFromGit(directory),
    extension: 'tar.gz',
    type: 'archive',
  };
};

const assertPageConfig = (publishedNames) => {
  const pageConfig = JSON.parse(readFileSync('skills.sh.json', 'utf8'));
  if (!Array.isArray(pageConfig.groupings) || pageConfig.groupings.length === 0) {
    throw new Error('skills.sh.json groupings must be a non-empty array');
  }

  const seen = new Set();
  for (const group of pageConfig.groupings) {
    if (typeof group?.title !== 'string' || group.title.length === 0) {
      throw new Error('skills.sh.json group is missing a title');
    }
    if (!Array.isArray(group.skills) || group.skills.length === 0) {
      throw new Error(`skills.sh.json group "${group.title}" has no skills`);
    }
    for (const skill of group.skills) {
      if (!publishedNames.has(skill)) {
        throw new Error(`skills.sh.json lists unknown skill "${skill}"`);
      }
      seen.add(skill);
    }
  }

  for (const name of publishedNames) {
    if (!seen.has(name)) {
      throw new Error(`Skill "${name}" is missing from skills.sh.json`);
    }
  }
};

rmSync(outputDirectory, { force: true, recursive: true });
mkdirSync(outputDirectory);

const directories = listSkillDirectories();
if (directories.length === 0) {
  throw new Error('No skills found under skills/');
}

const skills = directories
  .map((directory) => {
    const metadata = readMetadata(directory);
    const artifact = createArtifact(directory, metadata.source);
    const filename = `${metadata.name}.${artifact.extension}`;
    writeFileSync(join(outputDirectory, filename), artifact.content);

    return {
      name: metadata.name,
      description: metadata.description,
      type: artifact.type,
      url: `${baseUrl.replace(/\/$/, '')}/${filename}`,
      digest: `sha256:${createHash('sha256').update(artifact.content).digest('hex')}`,
    };
  })
  .sort((a, b) => a.name.localeCompare(b.name));

if (new Set(skills.map(({ name }) => name)).size !== skills.length) {
  throw new Error('Skill names must be unique');
}

assertPageConfig(new Set(skills.map(({ name }) => name)));

writeFileSync(
  join(outputDirectory, 'index.json'),
  `${JSON.stringify({ $schema: schema, skills }, null, 2)}\n`,
);

console.log(`Published ${skills.length} skills to ${outputDirectory}`);
