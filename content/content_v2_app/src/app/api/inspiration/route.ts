
import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
    const CONTENT_V2_DIR = path.resolve(process.cwd(), '..', 'content_v2');
    const INPUT_DIR = path.join(CONTENT_V2_DIR, 'input');

    if (!fs.existsSync(INPUT_DIR)) {
        return NextResponse.json({ links: [], images: [] });
    }

    // Links
    let links: string[] = [];
    const linksFile = path.join(INPUT_DIR, 'links.txt');
    if (fs.existsSync(linksFile)) {
        links = fs.readFileSync(linksFile, 'utf-8').split('\n').filter(Boolean);
    }

    // Images
    const files = fs.readdirSync(INPUT_DIR);
    const images = files.filter(file => /\.(jpg|jpeg|png|webp|gif)$/i.test(file));

    return NextResponse.json({ links, images });
}

export async function POST(req: Request) {
    const formData = await req.formData();
    const file = formData.get('file') as File | null;
    const link = formData.get('link') as string | null;

    const CONTENT_V2_DIR = path.resolve(process.cwd(), '..', 'content_v2');
    const INPUT_DIR = path.join(CONTENT_V2_DIR, 'input');

    if (!fs.existsSync(INPUT_DIR)) {
        fs.mkdirSync(INPUT_DIR, { recursive: true });
    }

    if (file) {
        const buffer = Buffer.from(await file.arrayBuffer());
        const filePath = path.join(INPUT_DIR, file.name);
        fs.writeFileSync(filePath, buffer);
        return NextResponse.json({ success: true, type: 'image', name: file.name });
    }

    if (link) {
        const linksFile = path.join(INPUT_DIR, 'links.txt');
        fs.appendFileSync(linksFile, link + '\n');
        return NextResponse.json({ success: true, type: 'link', content: link });
    }

    return NextResponse.json({ success: false, error: 'No file or link provided' }, { status: 400 });
}

export async function DELETE(req: Request) {
    const { searchParams } = new URL(req.url);
    const type = searchParams.get('type'); // 'image' or 'link'
    const content = searchParams.get('content');

    if (!content) return NextResponse.json({ error: 'Content required' }, { status: 400 });

    const CONTENT_V2_DIR = path.resolve(process.cwd(), '..', 'content_v2');
    const INPUT_DIR = path.join(CONTENT_V2_DIR, 'input');
    const linksFile = path.join(INPUT_DIR, 'links.txt');

    if (type === 'image') {
        const filePath = path.join(INPUT_DIR, content);
        if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
    } else if (type === 'link') {
        if (fs.existsSync(linksFile)) {
            const lines = fs.readFileSync(linksFile, 'utf-8').split('\n');
            const newLines = lines.filter(line => line.trim() !== content.trim());
            fs.writeFileSync(linksFile, newLines.join('\n'));
        }
    }

    return NextResponse.json({ success: true });
}
