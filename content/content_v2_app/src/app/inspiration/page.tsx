'use client';

import { useState, useEffect } from 'react';
import { Upload, Link, Trash2, Plus, RefreshCw, Eye } from 'lucide-react';
import Image from 'next/image';

interface InspirationContent {
    links: string[];
    images: string[];
}

export default function InspirationPage() {
    const [content, setContent] = useState<InspirationContent>({ links: [], images: [] });
    const [loading, setLoading] = useState(true);
    const [uploading, setUploading] = useState(false);
    const [newLink, setNewLink] = useState('');

    const fetchContent = async () => {
        setLoading(true);
        try {
            const res = await fetch('/api/inspiration');
            if (res.ok) {
                const data = await res.json();
                setContent(data);
            }
        } catch (error) {
            console.error('Failed to fetch inspiration', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchContent();
    }, []);

    const handleLinkSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newLink.trim()) return;

        try {
            const formData = new FormData();
            formData.append('link', newLink);

            const res = await fetch('/api/inspiration', {
                method: 'POST',
                body: formData, // Sending as form data simplifies consistency
            });

            if (res.ok) {
                setNewLink('');
                fetchContent();
            }
        } catch (error) {
            console.error('Failed to add link', error);
        }
    };

    const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files || e.target.files.length === 0) return;

        setUploading(true);
        const file = e.target.files[0];
        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('/api/inspiration', {
                method: 'POST',
                body: formData,
            });

            if (res.ok) {
                fetchContent();
            }
        } catch (error) {
            console.error('Failed to upload image', error);
        } finally {
            setUploading(false);
            // Reset input value to allow re-uploading same file if needed
            e.target.value = '';
        }
    };

    const handleDelete = async (type: 'link' | 'image', item: string) => {
        if (!confirm('Are you sure you want to delete this item?')) return;

        try {
            const res = await fetch(`/api/inspiration?type=${type}&content=${encodeURIComponent(item)}`, {
                method: 'DELETE',
            });

            if (res.ok) {
                fetchContent();
            }
        } catch (error) {
            console.error('Failed to delete item', error);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-6xl mx-auto space-y-8">

                {/* Header */}
                <div className="flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Inspiration Library</h1>
                        <p className="text-gray-500 mt-1">Manage source material for content generation</p>
                    </div>
                    <button
                        onClick={fetchContent}
                        className="p-2 text-gray-500 hover:text-gray-900 transition-colors"
                        title="Refresh"
                    >
                        <RefreshCw size={20} />
                    </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

                    {/* Links Section */}
                    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 space-y-6">
                        <div className="flex items-center space-x-2 border-b border-gray-100 pb-4">
                            <Link className="text-purple-600" size={24} />
                            <h2 className="text-xl font-semibold text-gray-800">Instagram Links</h2>
                        </div>

                        {/* Add Link Form */}
                        <form onSubmit={handleLinkSubmit} className="flex gap-2">
                            <input
                                type="url"
                                value={newLink}
                                onChange={(e) => setNewLink(e.target.value)}
                                placeholder="Paste Instagram URL here..."
                                className="flex-1 px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all"
                                required
                            />
                            <button
                                type="submit"
                                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center gap-2 font-medium"
                                disabled={!newLink.trim()}
                            >
                                <Plus size={18} />
                                Add
                            </button>
                        </form>

                        {/* Links List */}
                        <div className="space-y-3 max-h-[500px] overflow-y-auto pr-2">
                            {loading ? (
                                <div className="text-center py-8 text-gray-400">Loading links...</div>
                            ) : content.links.length === 0 ? (
                                <div className="text-center py-8 text-gray-400 italic">No links added yet</div>
                            ) : (
                                content.links.map((link, idx) => (
                                    <div key={idx} className="group flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-purple-50 transition-colors border border-transparent hover:border-purple-100">
                                        <a
                                            href={link}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-gray-700 truncate flex-1 hover:text-purple-700 text-sm font-medium"
                                        >
                                            {link}
                                        </a>
                                        <button
                                            onClick={() => handleDelete('link', link)}
                                            className="ml-3 p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-md opacity-0 group-hover:opacity-100 transition-all"
                                            title="Remove link"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    {/* Images Section */}
                    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 space-y-6">
                        <div className="flex items-center justify-between border-b border-gray-100 pb-4">
                            <div className="flex items-center space-x-2">
                                <Upload className="text-teal-600" size={24} />
                                <h2 className="text-xl font-semibold text-gray-800">Visual Inspiration</h2>
                            </div>

                            {/* Upload Button (hidden input + label) */}
                            <label className={`cursor-pointer px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors flex items-center gap-2 font-medium text-sm ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}>
                                <Plus size={16} />
                                {uploading ? 'Uploading...' : 'Upload Image'}
                                <input
                                    type="file"
                                    accept="image/*"
                                    onChange={handleImageUpload}
                                    className="hidden"
                                    disabled={uploading}
                                />
                            </label>
                        </div>

                        {/* Images Grid */}
                        <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 max-h-[500px] overflow-y-auto pr-2">
                            {loading ? (
                                <div className="col-span-full text-center py-8 text-gray-400">Loading images...</div>
                            ) : content.images.length === 0 ? (
                                <div className="col-span-full text-center py-8 text-gray-400 italic">No images uploaded yet</div>
                            ) : (
                                content.images.map((img, idx) => (
                                    <div key={idx} className="group relative aspect-square bg-gray-100 rounded-lg overflow-hidden border border-gray-200">
                                        <Image
                                            src={`/api/image/${encodeURIComponent(img)}`}
                                            alt={img}
                                            fill
                                            className="object-cover transition-transform duration-300 group-hover:scale-105"
                                        />

                                        {/* Overlay Actions */}
                                        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                                            <a
                                                href={`/api/image/${encodeURIComponent(img)}`}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="p-2 bg-white/90 rounded-full text-gray-700 hover:text-purple-600 hover:bg-white transition-colors"
                                                title="View full size"
                                            >
                                                <Eye size={18} />
                                            </a>
                                            <button
                                                onClick={() => handleDelete('image', img)}
                                                className="p-2 bg-white/90 rounded-full text-gray-700 hover:text-red-500 hover:bg-white transition-colors"
                                                title="Delete image"
                                            >
                                                <Trash2 size={18} />
                                            </button>
                                        </div>

                                        {/* Filename badge */}
                                        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-2">
                                            <p className="text-white text-xs truncate px-1">{img}</p>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
}
