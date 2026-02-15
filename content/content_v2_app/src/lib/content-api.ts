
import fs from 'fs';
import path from 'path';


// Define paths relative to the Next.js app root
// Assuming the app is in content/content_v2_app and the backend is in content/content_v2
const CONTENT_V2_DIR = path.resolve(process.cwd(), '..', 'content_v2');
const INPUT_DIR = path.join(CONTENT_V2_DIR, 'input');
// const OUTPUT_DIR = path.join(CONTENT_V2_DIR, 'output');
const LINKS_FILE = path.join(INPUT_DIR, 'links.txt');

export interface InspirationItem {
    type: 'image' | 'link';
    content: string; // url or filename
    path?: string; // full path for images (internal use)
}

export async function getInspiration(): Promise<InspirationItem[]> {
    const items: InspirationItem[] = [];

    // Ensure input directory exists
    if (!fs.existsSync(INPUT_DIR)) {
        return items;
    }

    // 1. Read Links
    if (fs.existsSync(LINKS_FILE)) {
        const fileContent = fs.readFileSync(LINKS_FILE, 'utf-8');
        const links = fileContent.split('\n').filter(line => line.trim() !== '');
        links.forEach(link => {
            items.push({ type: 'link', content: link.trim() });
        });
    }

    // 2. Read Images
    const files = fs.readdirSync(INPUT_DIR);
    const imageExtensions = ['.jpg', '.jpeg', '.png', '.webp'];

    files.forEach(file => {
        const ext = path.extname(file).toLowerCase();
        if (imageExtensions.includes(ext)) {
            items.push({ type: 'image', content: file, path: path.join(INPUT_DIR, file) });
        }
    });

    return items;
}

export async function addLink(url: string) {
    // Ensure input directory exists
    if (!fs.existsSync(INPUT_DIR)) {
        fs.mkdirSync(INPUT_DIR, { recursive: true });
    }

    // Append to links.txt
    fs.appendFileSync(LINKS_FILE, url + '\n');
}

export async function saveImage(buffer: Buffer, filename: string) {
    if (!fs.existsSync(INPUT_DIR)) {
        fs.mkdirSync(INPUT_DIR, { recursive: true });
    }
    const filePath = path.join(INPUT_DIR, filename);
    fs.writeFileSync(filePath, buffer);
    return filename;
}


export async function deleteInspiration(type: 'image' | 'link', content: string) {
    if (type === 'link') {
        if (fs.existsSync(LINKS_FILE)) {
            const fileContent = fs.readFileSync(LINKS_FILE, 'utf-8');
            const lines = fileContent.split('\n');
            const newLines = lines.filter(line => line.trim() !== content.trim());
            fs.writeFileSync(LINKS_FILE, newLines.join('\n'));
        }
    } else if (type === 'image') {
        const filePath = path.join(INPUT_DIR, content);
        if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
        }
    }
}
