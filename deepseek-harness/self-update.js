// prospector-self-update
//
// Runs once per session, before the first turn, on the `agent/session-start`
// lifecycle event (the harness's "session lifecycle began, once before the
// first turn" hook — the installed SDK's equivalent of `session/created`).
//
// It updates the site-prospector TOOLKIT from its git repository, fire-and-
// forget, with a logged, non-fatal failure. It never touches the user's data
// folder (prospector.db, leads.md, sites/, prospector-config.json) — only the
// toolkit repo and the preset's active `skills/` copy.
//
// Config (on the agent.cordis.yml row):
//   toolkitDir: absolute path to the site-prospector git repo
//   skillsDir:  optional override for the preset's active skills directory
//               (defaults to <presetDir>/skills next to this file)

import { execFile } from 'node:child_process'
import { promisify } from 'node:util'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { cp, access } from 'node:fs/promises'

const execFileAsync = promisify(execFile)

export const name = 'prospector-self-update'

export function apply(ctx, config = {}) {
  const presetDir = dirname(fileURLToPath(import.meta.url))
  const toolkitDir = config.toolkitDir ?? ''
  const skillsDir = config.skillsDir ?? join(presetDir, 'skills')

  ctx.on('agent/session-start', () => {
    void update(ctx, { presetDir, toolkitDir, skillsDir }).catch((error) => {
      ctx.logger.warn(
        `prospector-self-update: update failed (non-fatal): ${error?.message ?? String(error)}`,
      )
    })
  })
}

async function update(ctx, { toolkitDir, skillsDir }) {
  if (!toolkitDir) {
    ctx.logger.info('prospector-self-update: no toolkitDir configured; skipping')
    return
  }
  if (!(await exists(toolkitDir))) {
    ctx.logger.warn(`prospector-self-update: toolkit not found at ${toolkitDir}; skipping`)
    return
  }

  // 1. fetch tags from origin (non-fatal when no remote is configured yet)
  try {
    await git(ctx, toolkitDir, ['fetch', '--tags', 'origin'])
  } catch (error) {
    ctx.logger.info(
      `prospector-self-update: origin unavailable (no remote configured?) — skipping: ${error.message}`,
    )
    return
  }

  // 2. compare local HEAD with origin/main
  const behind = await git(ctx, toolkitDir, [
    'rev-list', '--count', 'HEAD..origin/main',
  ]).then((out) => Number.parseInt(out.trim(), 10)).catch(() => 0)

  // 3. pull --ff-only when newer, then re-sync the active copies
  if (!Number.isFinite(behind) || behind <= 0) {
    ctx.logger.info('prospector-self-update: up to date (origin/main is not ahead of HEAD)')
    return
  }

  const oldHead = (await git(ctx, toolkitDir, ['rev-parse', 'HEAD'])).trim()
  await git(ctx, toolkitDir, ['pull', '--ff-only'])

  // 4. re-sync the active copies into the harness (skills only; MCP config and
  //    dashboard changes surface through the repo and are applied by the skills)
  await syncSkills(ctx, toolkitDir, skillsDir)

  // 5. report what changed
  const log = await git(ctx, toolkitDir, ['log', `${oldHead}..HEAD`, '--oneline'])
  ctx.logger.info(
    `prospector-self-update: updated ${behind} commit(s):\n${log.trim()}`,
  )
}

async function syncSkills(ctx, toolkitDir, skillsDir) {
  const source = join(toolkitDir, 'skills')
  if (!(await exists(source))) {
    ctx.logger.warn('prospector-self-update: toolkit has no skills/ directory')
    return
  }
  await cp(source, skillsDir, { recursive: true, force: true })
  ctx.logger.info(`prospector-self-update: re-synced skills into ${skillsDir}`)
}

async function git(ctx, cwd, args) {
  try {
    const { stdout } = await execFileAsync('git', ['-C', cwd, ...args], {
      windowsHide: true,
      maxBuffer: 4 * 1024 * 1024,
    })
    return stdout
  } catch (error) {
    const detail = error?.stderr?.trim() || error?.message || String(error)
    throw new Error(`git ${args.join(' ')} failed: ${detail}`)
  }
}

async function exists(path) {
  try {
    await access(path)
    return true
  } catch {
    return false
  }
}
