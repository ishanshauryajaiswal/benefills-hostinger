
import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
    const CONTENT_V2_DIR = path.resolve(process.cwd(), '..', 'content_v2');
    const OUTPUT_DIR = path.join(CONTENT_V2_DIR, 'output');

    if (!fs.existsSync(OUTPUT_DIR)) {
        return NextResponse.json({ runs: [] });
    }

    const runs = [];
    const runDirs = fs.readdirSync(OUTPUT_DIR).filter(d => d.startsWith('run_'));

    for (const runDir of runDirs) {
        const runPath = path.join(OUTPUT_DIR, runDir);
        const stats = fs.statSync(runPath);

        if (stats.isDirectory()) {
            const posts = [];
            const postDirs = fs.readdirSync(runPath).filter(p => p.startsWith('post_'));

            for (const postDir of postDirs) {
                const postPath = path.join(runPath, postDir);
                const imagePath = path.join(postPath, 'image.png');
                const metadataPath = path.join(postPath, 'metadata.json');
                const captionPath = path.join(postPath, 'caption.txt');

                if (fs.existsSync(imagePath)) {
                    let metadata = {};
                    if (fs.existsSync(metadataPath)) {
                        try {
                            metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf-8'));
                        } catch (e) {
                            console.error(`Failed to parse metadata for ${runDir}/${postDir}`);
                        }
                    }

                    let caption = '';
                    if (fs.existsSync(captionPath)) {
                        caption = fs.readFileSync(captionPath, 'utf-8');
                    }

                    posts.push({
                        id: postDir,
                        image: `/api/output-image?run=${runDir}&post=${postDir}`,
                        metadata,
                        caption
                    });
                }
            }

            if (posts.length > 0) {
                runs.push({
                    id: runDir,
                    timestamp: stats.mtime,
                    posts
                });
            }
        }
    }

    // Sort runs by recency
    runs.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime());

    return NextResponse.json({ runs });
}
