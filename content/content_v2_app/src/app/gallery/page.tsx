
'use client';

import { useState, useEffect } from 'react';
import { LayoutGrid, Calendar, Info, Copy, Check, ChevronRight, ChevronDown, ExternalLink } from 'lucide-react';
import Image from 'next/image';

interface Post {
    id: string;
    image: string;
    metadata: any;
    caption: string;
}

interface Run {
    id: string;
    timestamp: string;
    posts: Post[];
}

export default function GalleryPage() {
    const [runs, setRuns] = useState<Run[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedPost, setSelectedPost] = useState<Post | null>(null);
    const [expandedRuns, setExpandedRuns] = useState<Record<string, boolean>>({});
    const [copied, setCopied] = useState<string | null>(null);

    useEffect(() => {
        const fetchRuns = async () => {
            try {
                const res = await fetch('/api/gallery');
                if (res.ok) {
                    const data = await res.json();
                    setRuns(data.runs);
                    // Expand first run by default
                    if (data.runs.length > 0) {
                        setExpandedRuns({ [data.runs[0].id]: true });
                    }
                }
            } catch (error) {
                console.error('Failed to fetch gallery', error);
            } finally {
                setLoading(false);
            }
        };
        fetchRuns();
    }, []);

    const toggleRun = (runId: string) => {
        setExpandedRuns(prev => ({ ...prev, [runId]: !prev[runId] }));
    };

    const copyToClipboard = (text: string, id: string) => {
        navigator.clipboard.writeText(text);
        setCopied(id);
        setTimeout(() => setCopied(null), 2000);
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-7xl mx-auto space-y-8">

                {/* Header */}
                <div className="flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Generated Content Gallery</h1>
                        <p className="text-gray-500 mt-1">Review and manage AI-generated Instagram posts</p>
                    </div>
                    <div className="bg-white px-4 py-2 rounded-lg shadow-sm border border-gray-100 flex items-center space-x-2 text-sm font-medium text-gray-600">
                        <LayoutGrid size={16} className="text-purple-600" />
                        <span>{runs.reduce((acc, run) => acc + run.posts.length, 0)} Posts Total</span>
                    </div>
                </div>

                {loading ? (
                    <div className="flex flex-col items-center justify-center py-20 animate-pulse">
                        <div className="w-12 h-12 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"></div>
                        <p className="mt-4 text-gray-500 font-medium">Loading generation runs...</p>
                    </div>
                ) : runs.length === 0 ? (
                    <div className="bg-white rounded-2xl border border-dashed border-gray-300 py-20 text-center space-y-4">
                        <div className="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center text-gray-400">
                            <LayoutGrid size={32} />
                        </div>
                        <div className="space-y-1">
                            <h3 className="text-lg font-semibold text-gray-900">No generated content yet</h3>
                            <p className="text-gray-500 max-w-sm mx-auto">
                                Once you run the generation pipeline, your AI-crafted posts will appear here.
                            </p>
                        </div>
                    </div>
                ) : (
                    <div className="space-y-6">
                        {runs.map((run) => (
                            <div key={run.id} className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                                {/* Run Header */}
                                <button
                                    onClick={() => toggleRun(run.id)}
                                    className="w-full flex items-center justify-between p-4 hover:bg-gray-50 transition-colors border-b border-gray-50"
                                >
                                    <div className="flex items-center space-x-4">
                                        <div className="p-2 bg-purple-50 rounded-lg text-purple-600">
                                            <Calendar size={20} />
                                        </div>
                                        <div className="text-left">
                                            <h3 className="font-bold text-gray-900">{run.id}</h3>
                                            <p className="text-xs text-gray-500">{new Date(run.timestamp).toLocaleString()}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center space-x-4">
                                        <span className="text-xs font-semibold px-2 py-1 bg-gray-100 text-gray-600 rounded-full">
                                            {run.posts.length} variants
                                        </span>
                                        {expandedRuns[run.id] ? <ChevronDown size={20} className="text-gray-400" /> : <ChevronRight size={20} className="text-gray-400" />}
                                    </div>
                                </button>

                                {/* Run Posts */}
                                {expandedRuns[run.id] && (
                                    <div className="p-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                                        {run.posts.map((post) => (
                                            <div
                                                key={post.id}
                                                className="group relative bg-gray-50 rounded-xl overflow-hidden border border-gray-200 hover:border-purple-300 hover:shadow-md transition-all cursor-pointer"
                                                onClick={() => setSelectedPost(post)}
                                            >
                                                <div className="aspect-square relative">
                                                    <Image
                                                        src={post.image}
                                                        alt={post.id}
                                                        fill
                                                        className="object-cover"
                                                    />
                                                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                                                        <span className="px-4 py-2 bg-white text-gray-900 rounded-full text-sm font-bold shadow-lg">
                                                            Inspect Post
                                                        </span>
                                                    </div>

                                                    {/* Score Badge */}
                                                    {post.metadata?.review?.overall_quality?.score && (
                                                        <div className="absolute top-2 right-2 px-2 py-1 bg-white/90 backdrop-blur-sm rounded-md shadow-sm border border-gray-100 flex items-center space-x-1">
                                                            <span className="text-xs font-bold text-purple-700">{post.metadata.review.overall_quality.score}/10</span>
                                                        </div>
                                                    )}
                                                </div>
                                                <div className="p-3 bg-white">
                                                    <div className="flex justify-between items-center mb-1">
                                                        <span className="text-[10px] font-bold uppercase tracking-wider text-purple-600">{post.metadata?.angle || 'post'}</span>
                                                        <span className="text-[10px] text-gray-400">{post.id}</span>
                                                    </div>
                                                    <p className="text-xs text-gray-600 line-clamp-2 italic">"{post.caption.split('\n')[0]}"</p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Post Inspector Modal */}
            {selectedPost && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                    <div className="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" onClick={() => setSelectedPost(null)}></div>
                    <div className="relative bg-white w-full max-w-5xl max-h-[90vh] rounded-2xl shadow-2xl overflow-hidden flex flex-col md:flex-row">

                        {/* Image Section */}
                        <div className="md:w-1/2 bg-black flex items-center justify-center relative group">
                            <Image
                                src={selectedPost.image}
                                alt="Selected post"
                                width={800}
                                height={800}
                                className="w-full h-full object-contain"
                            />
                            <a
                                href={selectedPost.image}
                                target="_blank"
                                className="absolute top-4 right-4 p-2 bg-black/50 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-black/70"
                            >
                                <ExternalLink size={20} />
                            </a>
                        </div>

                        {/* Details Section */}
                        <div className="md:w-1/2 flex flex-col h-full bg-white overflow-y-auto">
                            <div className="p-6 border-b border-gray-100 flex justify-between items-center sticky top-0 bg-white z-10">
                                <div>
                                    <h2 className="text-xl font-bold text-gray-900">Post Insight</h2>
                                    <p className="text-sm text-gray-500">Variant {selectedPost.id}</p>
                                </div>
                                <button
                                    onClick={() => setSelectedPost(null)}
                                    className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                                >
                                    <ChevronDown className="rotate-90" />
                                </button>
                            </div>

                            <div className="p-6 space-y-8">
                                {/* Caption */}
                                <div className="space-y-3">
                                    <div className="flex justify-between items-center">
                                        <label className="text-xs font-bold uppercase tracking-widest text-gray-400">Generated Caption</label>
                                        <button
                                            onClick={() => copyToClipboard(selectedPost.caption, 'caption')}
                                            className={`flex items-center space-x-1 text-xs font-medium transition-colors ${copied === 'caption' ? 'text-teal-600' : 'text-purple-600 hover:text-purple-700'}`}
                                        >
                                            {copied === 'caption' ? <Check size={14} /> : <Copy size={14} />}
                                            <span>{copied === 'caption' ? 'Copied!' : 'Copy'}</span>
                                        </button>
                                    </div>
                                    <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
                                        {selectedPost.caption}
                                    </div>
                                </div>

                                {/* AI Review Score Breakdown */}
                                {selectedPost.metadata?.review && (
                                    <div className="space-y-4">
                                        <label className="text-xs font-bold uppercase tracking-widest text-gray-400">AI Review (Internal)</label>
                                        <div className="grid grid-cols-3 gap-3">
                                            <div className="bg-purple-50 p-3 rounded-lg text-center">
                                                <div className="text-lg font-bold text-purple-700">{selectedPost.metadata.review.brand_alignment?.score || '-'}/10</div>
                                                <div className="text-[10px] text-purple-600 font-medium">Brand Fit</div>
                                            </div>
                                            <div className="bg-teal-50 p-3 rounded-lg text-center">
                                                <div className="text-lg font-bold text-teal-700">{selectedPost.metadata.review.engagement_potential?.score || '-'}/10</div>
                                                <div className="text-[10px] text-teal-600 font-medium">Engagement</div>
                                            </div>
                                            <div className="bg-amber-50 p-3 rounded-lg text-center">
                                                <div className="text-lg font-bold text-amber-700">{selectedPost.metadata.review.overall_quality?.score || '-'}/10</div>
                                                <div className="text-[10px] text-amber-600 font-medium">Overall</div>
                                            </div>
                                        </div>
                                        {selectedPost.metadata.review.overall_quality?.reason && (
                                            <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 text-sm">
                                                <div className="flex items-center space-x-2 mb-2">
                                                    <Info size={14} className="text-purple-600" />
                                                    <span className="font-bold text-gray-900">Expert Summary</span>
                                                </div>
                                                <p className="text-gray-600">{selectedPost.metadata.review.overall_quality.reason}</p>
                                            </div>
                                        )}
                                    </div>
                                )}

                                {/* Prompt used */}
                                <div className="space-y-3">
                                    <div className="flex justify-between items-center">
                                        <label className="text-xs font-bold uppercase tracking-widest text-gray-400">Exact Image Prompt</label>
                                        <button
                                            onClick={() => copyToClipboard(selectedPost.metadata?.image_prompt_used || '', 'prompt')}
                                            className={`flex items-center space-x-1 text-xs font-medium transition-colors ${copied === 'prompt' ? 'text-teal-600' : 'text-purple-600 hover:text-purple-700'}`}
                                        >
                                            {copied === 'prompt' ? <Check size={14} /> : <Copy size={14} />}
                                            <span>{copied === 'prompt' ? 'Copied' : 'Copy Prompt'}</span>
                                        </button>
                                    </div>
                                    <p className="text-xs text-gray-500 italic bg-gray-50 p-3 rounded-lg border border-gray-100">
                                        {selectedPost.metadata?.image_prompt_used}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
