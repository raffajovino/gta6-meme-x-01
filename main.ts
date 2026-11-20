// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry itself is the X post: an agent-made GTA 6 meme, posted from a
// public account with make.fun (a link or written out) and/or a tag of
// @makefunai plus one of the account's play codes in its text. This program
// does the one mechanical job the bounty asks of it: it carries POST.json,
// which names that post's address, from the repository into /output, where
// the house reads it, fetches the post from X itself, and hands the post's
// first picture and text to the judge. Nothing this program writes about
// the post is judged.
//
// Outside the grader, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR stand in for
// /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(BOT_DIR, 'POST.json');
const target = join(OUTPUT_DIR, 'POST.json');

let post;
try {
  post = readFileSync(source, 'utf8');
} catch (err) {
  console.error(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

let parsed: unknown;
try {
  parsed = JSON.parse(post);
} catch (err) {
  console.error(`POST.json is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}

if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
  console.error('POST.json must be a JSON object with a url field.');
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(target, JSON.stringify(parsed) + '\n', 'utf8');
