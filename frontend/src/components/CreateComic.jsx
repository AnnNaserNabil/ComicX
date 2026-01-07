import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, Sparkles, Loader2 } from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import toast from 'react-hot-toast';
import { comicAPI, storyAPI } from '../services/api';
import { useComicStore, useSettingsStore } from '../store/comicStore';

const CreateComic = () => {
    const [activeTab, setActiveTab] = useState('text');
    const [storyText, setStoryText] = useState('');
    const [storyPrompt, setStoryPrompt] = useState('');
    const [genre, setGenre] = useState('Fantasy');
    const [themes, setThemes] = useState([]);
    const [generatedStory, setGeneratedStory] = useState('');
    const [isGeneratingStory, setIsGeneratingStory] = useState(false);

    const { setIsGenerating, setGenerationStatus, addComic } = useComicStore();
    const { artStyle, targetPages, targetAudience } = useSettingsStore();

    const onDrop = async (acceptedFiles) => {
        const file = acceptedFiles[0];
        if (!file) return;

        try {
            setIsGenerating(true);
            toast.loading('Generating comic from PDF...', { id: 'generate' });

            const result = await comicAPI.generateFromPDF(file, {
                artStyle,
                targetPages,
                targetAudience,
            });

            addComic(result);
            toast.success('Comic generation started!', { id: 'generate' });
            setGenerationStatus(result);
        } catch (error) {
            toast.error('Failed to generate comic', { id: 'generate' });
            console.error(error);
        } finally {
            setIsGenerating(false);
        }
    };

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'application/pdf': ['.pdf'] },
        maxFiles: 1,
    });

    const handleGenerateStory = async () => {
        if (!storyPrompt.trim()) {
            toast.error('Please enter a story prompt');
            return;
        }

        try {
            setIsGeneratingStory(true);
            toast.loading('Generating story with AI...', { id: 'story' });

            const result = await storyAPI.generateStory(storyPrompt, {
                genre,
                themes,
                numChapters: 5,
            });

            setGeneratedStory(result.story);
            toast.success('Story generated!', { id: 'story' });
        } catch (error) {
            toast.error('Failed to generate story', { id: 'story' });
            console.error(error);
        } finally {
            setIsGeneratingStory(false);
        }
    };

    const handleGenerateComic = async () => {
        const text = generatedStory || storyText;

        if (!text.trim()) {
            toast.error('Please provide a story');
            return;
        }

        try {
            setIsGenerating(true);
            toast.loading('Generating comic...', { id: 'generate' });

            const result = await comicAPI.generateFromText({
                text,
                title: 'AI Generated Comic',
                artStyle,
                targetPages,
                targetAudience,
            });

            addComic(result);
            toast.success('Comic generation started!', { id: 'generate' });
            setGenerationStatus(result);
        } catch (error) {
            toast.error('Failed to generate comic', { id: 'generate' });
            console.error(error);
        } finally {
            setIsGenerating(false);
        }
    };

    return (
        <div className="max-w-6xl mx-auto">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="card"
            >
                {/* Tabs */}
                <div className="flex gap-4 mb-6 border-b border-white/10 pb-4">
                    {[
                        { id: 'text', icon: FileText, label: 'Write Story' },
                        { id: 'pdf', icon: Upload, label: 'Upload PDF' },
                        { id: 'ai', icon: Sparkles, label: 'AI Generator' },
                    ].map((tab) => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-all ${activeTab === tab.id
                                    ? 'bg-gradient-to-r from-primary-600 to-secondary-600 text-white'
                                    : 'glass hover:bg-white/20'
                                }`}
                        >
                            <tab.icon className="w-5 h-5" />
                            {tab.label}
                        </button>
                    ))}
                </div>

                {/* Text Input Tab */}
                {activeTab === 'text' && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="space-y-4"
                    >
                        <h3 className="text-2xl font-bold mb-4">Write Your Story</h3>
                        <textarea
                            value={storyText}
                            onChange={(e) => setStoryText(e.target.value)}
                            placeholder="Once upon a time in a distant galaxy..."
                            className="input min-h-[300px] resize-none"
                        />
                        <button onClick={handleGenerateComic} className="btn-primary w-full">
                            Generate Comic Book
                        </button>
                    </motion.div>
                )}

                {/* PDF Upload Tab */}
                {activeTab === 'pdf' && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="space-y-4"
                    >
                        <h3 className="text-2xl font-bold mb-4">Upload PDF</h3>
                        <div
                            {...getRootProps()}
                            className={`glass border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all ${isDragActive ? 'border-primary-500 bg-primary-500/10' : 'border-white/20'
                                }`}
                        >
                            <input {...getInputProps()} />
                            <Upload className="w-16 h-16 mx-auto mb-4 opacity-50" />
                            <p className="text-lg mb-2">
                                {isDragActive ? 'Drop PDF here' : 'Drag & drop PDF or click to browse'}
                            </p>
                            <p className="text-sm opacity-50">Supports PDF files only</p>
                        </div>
                    </motion.div>
                )}

                {/* AI Generator Tab */}
                {activeTab === 'ai' && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="space-y-4"
                    >
                        <h3 className="text-2xl font-bold mb-4">AI Story Generator</h3>

                        <div className="grid md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium mb-2">Genre</label>
                                <select
                                    value={genre}
                                    onChange={(e) => setGenre(e.target.value)}
                                    className="input"
                                >
                                    <option>Fantasy</option>
                                    <option>Sci-Fi</option>
                                    <option>Adventure</option>
                                    <option>Mystery</option>
                                    <option>Romance</option>
                                    <option>Horror</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium mb-2">Themes</label>
                                <input
                                    type="text"
                                    placeholder="Friendship, Courage, Discovery..."
                                    className="input"
                                    onChange={(e) => setThemes(e.target.value.split(',').map(t => t.trim()))}
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-2">Story Prompt</label>
                            <textarea
                                value={storyPrompt}
                                onChange={(e) => setStoryPrompt(e.target.value)}
                                placeholder="A young wizard discovers an ancient prophecy..."
                                className="input min-h-[150px] resize-none"
                            />
                        </div>

                        <button
                            onClick={handleGenerateStory}
                            disabled={isGeneratingStory}
                            className="btn-primary w-full flex items-center justify-center gap-2"
                        >
                            {isGeneratingStory ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    Generating Story...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-5 h-5" />
                                    Generate Story
                                </>
                            )}
                        </button>

                        {generatedStory && (
                            <div className="mt-6">
                                <h4 className="text-lg font-semibold mb-2">Generated Story</h4>
                                <div className="glass p-4 rounded-lg max-h-[300px] overflow-y-auto">
                                    <p className="whitespace-pre-wrap">{generatedStory}</p>
                                </div>
                                <button onClick={handleGenerateComic} className="btn-primary w-full mt-4">
                                    Generate Comic from Story
                                </button>
                            </div>
                        )}
                    </motion.div>
                )}
            </motion.div>
        </div>
    );
};

export default CreateComic;
