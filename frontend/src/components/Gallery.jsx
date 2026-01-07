import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Download, Eye, Trash2 } from 'lucide-react';
import { comicAPI } from '../services/api';
import { useComicStore } from '../store/comicStore';
import toast from 'react-hot-toast';

const Gallery = () => {
    const { comics, setComics } = useComicStore();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadComics();
    }, []);

    const loadComics = async () => {
        try {
            const data = await comicAPI.getAllComics();
            setComics(data);
        } catch (error) {
            toast.error('Failed to load comics');
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = async (jobId, format = 'pdf') => {
        try {
            const blob = await comicAPI.downloadComic(jobId, format);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `comic-${jobId}.${format}`;
            a.click();
            toast.success('Download started!');
        } catch (error) {
            toast.error('Download failed');
            console.error(error);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <h2 className="text-3xl font-bold mb-8">Your Comics</h2>

                {comics.length === 0 ? (
                    <div className="card text-center py-12">
                        <p className="text-xl opacity-50">No comics generated yet</p>
                        <p className="mt-2 opacity-30">Create your first comic to see it here!</p>
                    </div>
                ) : (
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {comics.map((comic, index) => (
                            <motion.div
                                key={comic.job_id}
                                initial={{ opacity: 0, scale: 0.9 }}
                                animate={{ opacity: 1, scale: 1 }}
                                transition={{ delay: index * 0.1 }}
                                className="card group hover:scale-105 transition-transform"
                            >
                                {/* Thumbnail */}
                                <div className="aspect-[3/4] bg-gradient-to-br from-primary-600 to-secondary-600 rounded-lg mb-4 flex items-center justify-center">
                                    <span className="text-6xl font-bold opacity-50">📚</span>
                                </div>

                                {/* Info */}
                                <h3 className="font-bold text-lg mb-2 truncate">{comic.title}</h3>
                                <p className="text-sm opacity-70 mb-4">
                                    {comic.total_pages} pages • {comic.format.toUpperCase()}
                                </p>

                                {/* Actions */}
                                <div className="flex gap-2">
                                    <button
                                        onClick={() => handleDownload(comic.job_id, 'pdf')}
                                        className="flex-1 glass hover:bg-white/20 px-4 py-2 rounded-lg flex items-center justify-center gap-2 transition-all"
                                    >
                                        <Download className="w-4 h-4" />
                                        PDF
                                    </button>
                                    <button
                                        onClick={() => handleDownload(comic.job_id, 'cbz')}
                                        className="flex-1 glass hover:bg-white/20 px-4 py-2 rounded-lg flex items-center justify-center gap-2 transition-all"
                                    >
                                        <Download className="w-4 h-4" />
                                        CBZ
                                    </button>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                )}
            </motion.div>
        </div>
    );
};

export default Gallery;
