import React from 'react';
import { motion } from 'framer-motion';
import { Palette, Users, FileText, Settings as SettingsIcon } from 'lucide-react';
import { useSettingsStore } from '../store/comicStore';

const Settings = () => {
    const {
        artStyle,
        targetPages,
        targetAudience,
        outputFormats,
        setArtStyle,
        setTargetPages,
        setTargetAudience,
        setOutputFormats,
    } = useSettingsStore();

    const artStyles = [
        'cartoon',
        'manga',
        'realistic',
        'watercolor',
        'sketch',
        'comic',
        'cinematic',
    ];

    const audiences = ['children', 'young adult', 'adult', 'general'];

    const formats = [
        { id: 'pdf', label: 'PDF' },
        { id: 'cbz', label: 'CBZ' },
        { id: 'web', label: 'Web' },
        { id: 'video', label: 'Video' },
    ];

    const toggleFormat = (format) => {
        if (outputFormats.includes(format)) {
            setOutputFormats(outputFormats.filter((f) => f !== format));
        } else {
            setOutputFormats([...outputFormats, format]);
        }
    };

    return (
        <div className="max-w-4xl mx-auto">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
            >
                <h2 className="text-3xl font-bold mb-8">Generation Settings</h2>

                {/* Art Style */}
                <div className="card">
                    <div className="flex items-center gap-3 mb-4">
                        <Palette className="w-6 h-6 text-primary-400" />
                        <h3 className="text-xl font-semibold">Art Style</h3>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {artStyles.map((style) => (
                            <button
                                key={style}
                                onClick={() => setArtStyle(style)}
                                className={`px-4 py-3 rounded-lg capitalize transition-all ${artStyle === style
                                        ? 'bg-gradient-to-r from-primary-600 to-secondary-600'
                                        : 'glass hover:bg-white/20'
                                    }`}
                            >
                                {style}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Target Pages */}
                <div className="card">
                    <div className="flex items-center gap-3 mb-4">
                        <FileText className="w-6 h-6 text-primary-400" />
                        <h3 className="text-xl font-semibold">Number of Pages</h3>
                    </div>
                    <div className="space-y-4">
                        <input
                            type="range"
                            min="5"
                            max="50"
                            step="5"
                            value={targetPages}
                            onChange={(e) => setTargetPages(parseInt(e.target.value))}
                            className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer"
                        />
                        <div className="flex justify-between text-sm opacity-70">
                            <span>5 pages</span>
                            <span className="text-2xl font-bold text-primary-400">{targetPages}</span>
                            <span>50 pages</span>
                        </div>
                    </div>
                </div>

                {/* Target Audience */}
                <div className="card">
                    <div className="flex items-center gap-3 mb-4">
                        <Users className="w-6 h-6 text-primary-400" />
                        <h3 className="text-xl font-semibold">Target Audience</h3>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {audiences.map((audience) => (
                            <button
                                key={audience}
                                onClick={() => setTargetAudience(audience)}
                                className={`px-4 py-3 rounded-lg capitalize transition-all ${targetAudience === audience
                                        ? 'bg-gradient-to-r from-primary-600 to-secondary-600'
                                        : 'glass hover:bg-white/20'
                                    }`}
                            >
                                {audience}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Output Formats */}
                <div className="card">
                    <div className="flex items-center gap-3 mb-4">
                        <SettingsIcon className="w-6 h-6 text-primary-400" />
                        <h3 className="text-xl font-semibold">Output Formats</h3>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {formats.map((format) => (
                            <button
                                key={format.id}
                                onClick={() => toggleFormat(format.id)}
                                className={`px-4 py-3 rounded-lg transition-all ${outputFormats.includes(format.id)
                                        ? 'bg-gradient-to-r from-primary-600 to-secondary-600'
                                        : 'glass hover:bg-white/20'
                                    }`}
                            >
                                {format.label}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Current Settings Summary */}
                <div className="card bg-gradient-to-r from-primary-600/20 to-secondary-600/20">
                    <h3 className="text-xl font-semibold mb-4">Current Configuration</h3>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                        <div>
                            <span className="opacity-70">Art Style:</span>
                            <span className="ml-2 font-semibold capitalize">{artStyle}</span>
                        </div>
                        <div>
                            <span className="opacity-70">Pages:</span>
                            <span className="ml-2 font-semibold">{targetPages}</span>
                        </div>
                        <div>
                            <span className="opacity-70">Audience:</span>
                            <span className="ml-2 font-semibold capitalize">{targetAudience}</span>
                        </div>
                        <div>
                            <span className="opacity-70">Formats:</span>
                            <span className="ml-2 font-semibold">{outputFormats.join(', ').toUpperCase()}</span>
                        </div>
                    </div>
                </div>
            </motion.div>
        </div>
    );
};

export default Settings;
