// Entry for the 21 November 2026 news-image competition.
// Saturday's front page is entry.jpg in this folder. The job here is
// small and strict: confirm the picture is a whole 1024 by 1024 JPEG
// under one mebibyte, copy it to the output folder as entry.png, and
// confirm the copy matches the original byte for byte. Running it twice
// must give the same bytes both times.
//
// Try it: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HOME = dirname(fileURLToPath(import.meta.url));
const PICTURE = 'entry.jpg';
const MAX_BYTES = 1048576;
const EDGE = 1024;

interface Dims {
  w: number;
  h: number;
}

// Hunt for the first frame header (SOF0 or SOF2) and read the picture's
// width and height out of it. Returns null when the bytes are not a JPEG
// or no frame header turns up before the image ends.
function jpegDimensions(bytes: Buffer): Dims | null {
  if (bytes.length < 4) return null;
  if (bytes[0] !== 0xff || bytes[1] !== 0xd8) return null;
  let cursor = 2;
  while (cursor + 4 <= bytes.length) {
    if (bytes[cursor] !== 0xff) return null;
    const marker = bytes[cursor + 1];
    if (marker === 0xd9) return null;
    if (marker === 0x01 || (marker >= 0xd0 && marker <= 0xd7)) {
      cursor += 2;
      continue;
    }
    const segLen = bytes.readUInt16BE(cursor + 2);
    if (segLen < 2) return null;
    if (cursor + 2 + segLen > bytes.length) return null;
    if (marker === 0xc0 || marker === 0xc2) {
      return {
        h: bytes.readUInt16BE(cursor + 5),
        w: bytes.readUInt16BE(cursor + 7),
      };
    }
    cursor += 2 + segLen;
  }
  return null;
}

function digest(bytes: Buffer): string {
  return createHash('sha256').update(bytes).digest('hex');
}

function die(text: string, code: number): never {
  process.stderr.write(`news-image-20261121: ${text}\n`);
  process.exit(code);
}

function main(): void {
  const source = join(HOME, PICTURE);
  if (!existsSync(source)) {
    die(`missing ${PICTURE} beside main.ts; build it with compose.py first`, 2);
  }
  const original = readFileSync(source);
  if (original.length > MAX_BYTES) {
    die(`${PICTURE} is ${original.length} bytes, over the ${MAX_BYTES} byte cap`, 1);
  }
  const dims = jpegDimensions(original);
  if (dims === null) {
    die(`${PICTURE} carries no JPEG frame header`, 1);
  }
  if (dims.w !== EDGE || dims.h !== EDGE) {
    die(`${PICTURE} measures ${dims.w}x${dims.h}, expected ${EDGE}x${EDGE}`, 1);
  }
  const destDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  mkdirSync(destDir, { recursive: true });
  const dest = join(destDir, 'entry.png');
  writeFileSync(dest, original);
  const again = readFileSync(dest);
  if (again.length !== original.length || digest(again) !== digest(original)) {
    die(`the copy at ${dest} is not identical to ${PICTURE}`, 1);
  }
  // Confirm the copy's own frame header too, so a cut-off or swapped
  // file is caught even when its length happens to line up.
  const againDims = jpegDimensions(again);
  if (againDims === null || againDims.w !== EDGE || againDims.h !== EDGE) {
    die(`the copy at ${dest} does not parse as a ${EDGE}x${EDGE} JPEG`, 1);
  }
  const short = digest(again).slice(0, 16);
  process.stdout.write(
    `news-image-20261121: wrote ${dest} (${again.length} bytes, JPEG 1024x1024, sha256 ${short}...)\n`,
  );
}

main();
