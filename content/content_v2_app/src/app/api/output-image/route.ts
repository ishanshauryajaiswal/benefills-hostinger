
import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET(req: Request) {
    const { searchParams } = new URL(req.url);
    const run = searchParams.get('run');
    const post = searchParams.get('post');

    if (!run || !post) {
        return new NextResponse('Missing parameters', { status: 400 });
    }

    const CONTENT_V2_DIR = path.resolve(process.cwd(), '..', 'content_v2');
    const filePath = path.join(CONTENT_V2_DIR, 'output', run, post, 'image.png');

    if (!fs.existsSync(filePath)) {
        return new NextResponse('File not found', { status: 404 });
    }

    const fileBuffer = fs.readFileSync(filePath);

    return new NextResponse(fileBuffer, {
        headers: {
            'Content-Type': 'image/png',
            'Cache-Control': 'public, max-age=31536000, immutable',
        },
    });
}
