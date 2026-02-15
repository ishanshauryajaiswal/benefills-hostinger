
import Link from 'next/link';
import { ArrowRight, Image as ImageIcon, Sparkles } from 'lucide-react';

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

        <div className="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
          {/* Inspiration Card */}
          <Link
            href="/inspiration"
            className="group relative bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg transition-all hover:-translate-y-1 overflow-hidden"
          >
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <ImageIcon size={120} />
            </div>
            <div className="relative z-10 space-y-4">
              <div className="p-3 bg-purple-100 w-fit rounded-lg text-purple-600">
                <ImageIcon size={28} />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Inspiration Library</h2>
              <p className="text-gray-500">
                Curate source material. Add Instagram links or upload reference images for the AI to analyze.
              </p>
              <div className="flex items-center text-purple-600 font-medium group-hover:translate-x-1 transition-transform">
                Manage Inputs <ArrowRight size={18} className="ml-2" />
              </div>
            </div>
          </Link>

          {/* Generator Card (Placeholder for now) */}
          <div className="group relative bg-gray-50 p-8 rounded-2xl border border-dashed border-gray-300 opacity-60 hover:opacity-100 transition-opacity cursor-not-allowed">
            <div className="absolute top-0 right-0 p-4 opacity-5">
              <Sparkles size={120} />
            </div>
            <div className="relative z-10 space-y-4">
              <div className="p-3 bg-gray-200 w-fit rounded-lg text-gray-500">
                <Sparkles size={28} />
              </div>
              <h2 className="text-2xl font-bold text-gray-400">Content Generator</h2>
              <p className="text-gray-400">
                Run the generation pipeline. Configure style, variants, and review generated posts.
              </p>
              <div className="flex items-center text-gray-400 font-medium">
                Coming Soon
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
