
import Link from 'next/link';
import { ArrowRight, Image as ImageIcon, Sparkles, LayoutGrid } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-8">
      <div className="max-w-4xl w-full space-y-12">
        <div className="text-center space-y-4">
          <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight">
            Benefills Content Engine <span className="text-purple-600">v2</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-powered Instagram content generation workflow.
            Manage inspiration, generate posts, and review analytics.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Inspiration Card */}
          <Link
            href="/inspiration"
            className="group relative bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg transition-all hover:-translate-y-1 overflow-hidden"
          >
            <div className="relative z-10 space-y-4">
              <div className="p-3 bg-purple-100 w-fit rounded-lg text-purple-600">
                <ImageIcon size={24} />
              </div>
              <h2 className="text-xl font-bold text-gray-900">Inspiration Library</h2>
              <p className="text-sm text-gray-500">
                Curate source material. Add Instagram links or upload reference images for the AI to analyze.
              </p>
              <div className="flex items-center text-purple-600 font-medium group-hover:translate-x-1 transition-transform text-sm">
                Manage Inputs <ArrowRight size={16} className="ml-2" />
              </div>
            </div>
          </Link>

          {/* Gallery Card */}
          <Link
            href="/gallery"
            className="group relative bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg transition-all hover:-translate-y-1 overflow-hidden"
          >
            <div className="relative z-10 space-y-4">
              <div className="p-3 bg-teal-100 w-fit rounded-lg text-teal-600">
                <LayoutGrid size={24} />
              </div>
              <h2 className="text-xl font-bold text-gray-900">Output Gallery</h2>
              <p className="text-sm text-gray-500">
                Review all generated posts. Inspect captions, exact prompts, and brand alignment scores.
              </p>
              <div className="flex items-center text-teal-600 font-medium group-hover:translate-x-1 transition-transform text-sm">
                View Results <ArrowRight size={16} className="ml-2" />
              </div>
            </div>
          </Link>

          {/* Generator Card (Placeholder for now) */}
          <div className="group relative bg-gray-50 p-6 rounded-2xl border border-dashed border-gray-300 opacity-60 transition-opacity cursor-not-allowed">
            <div className="relative z-10 space-y-4">
              <div className="p-3 bg-gray-200 w-fit rounded-lg text-gray-500">
                <Sparkles size={24} />
              </div>
              <h2 className="text-xl font-bold text-gray-400">Content Generator</h2>
              <p className="text-sm text-gray-400">
                Run the generation pipeline autonomously. Configure style, variants, and review posts.
              </p>
              <div className="flex items-center text-gray-400 font-medium text-sm">
                Coming Soon
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
