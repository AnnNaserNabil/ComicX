import React from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { motion } from 'framer-motion';
import { BookOpen, Home, Image, Settings as SettingsIcon, Sparkles } from 'lucide-react';
import CreateComic from './components/CreateComic';
import Gallery from './components/Gallery';
import Settings from './components/Settings';
import './index.css';

const Navigation = () => {
    const location = useLocation();

    const navItems = [
        { path: '/', icon: Home, label: 'Create' },
        { path: '/gallery', icon: Image, label: 'Gallery' },
        { path: '/settings', icon: SettingsIcon, label: 'Settings' },
    ];

    return (
        <nav className="glass border-b border-white/10">
            <div className="max-w-7xl mx-auto px-6 py-4">
                <div className="flex items-center justify-between">
                    {/* Logo */}
                    <Link to="/" className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg flex items-center justify-center">
                            <BookOpen className="w-6 h-6" />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold">AI Comic Generator</h1>
                            <p className="text-xs opacity-50">Powered by Gemini & ModelsLab</p>
                        </div>
                    </Link>

                    {/* Nav Links */}
                    <div className="flex gap-2">
                        {navItems.map((item) => {
                            const isActive = location.pathname === item.path;
                            return (
                                <Link
                                    key={item.path}
                                    to={item.path}
                                    className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${isActive
                                            ? 'bg-gradient-to-r from-primary-600 to-secondary-600'
                                            : 'glass hover:bg-white/20'
                                        }`}
                                >
                                    <item.icon className="w-5 h-5" />
                                    <span className="hidden md:inline">{item.label}</span>
                                </Link>
                            );
                        })}
                    </div>
                </div>
            </div>
        </nav>
    );
};

const Home = () => {
    return (
        <div className="space-y-12">
            {/* Hero Section */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center py-12"
            >
                <div className="inline-block mb-6">
                    <div className="w-20 h-20 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-2xl flex items-center justify-center animate-float">
                        <Sparkles className="w-10 h-10" />
                    </div>
                </div>
                <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-primary-400 via-secondary-400 to-accent-500 bg-clip-text text-transparent">
                    Create Amazing Comics with AI
                </h1>
                <p className="text-xl opacity-70 max-w-2xl mx-auto">
                    Transform your stories into stunning visual comics using Google Gemini and ModelsLab
                </p>
            </motion.div>

            {/* Create Comic Section */}
            <CreateComic />

            {/* Features */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="grid md:grid-cols-3 gap-6 mt-12"
            >
                {[
                    {
                        icon: Sparkles,
                        title: 'AI-Powered',
                        description: 'Generate stories and artwork with cutting-edge AI',
                    },
                    {
                        icon: Image,
                        title: 'Multiple Styles',
                        description: '7 different art styles from cartoon to cinematic',
                    },
                    {
                        icon: BookOpen,
                        title: 'Professional Output',
                        description: 'Export as PDF, CBZ, Web, or animated video',
                    },
                ].map((feature, index) => (
                    <motion.div
                        key={index}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4 + index * 0.1 }}
                        className="card text-center"
                    >
                        <div className="w-12 h-12 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                            <feature.icon className="w-6 h-6" />
                        </div>
                        <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                        <p className="text-sm opacity-70">{feature.description}</p>
                    </motion.div>
                ))}
            </motion.div>
        </div>
    );
};

function App() {
    return (
        <BrowserRouter>
            <div className="min-h-screen">
                <Navigation />

                <main className="max-w-7xl mx-auto px-6 py-8">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/gallery" element={<Gallery />} />
                        <Route path="/settings" element={<Settings />} />
                    </Routes>
                </main>

                <Toaster
                    position="bottom-right"
                    toastOptions={{
                        className: 'glass',
                        style: {
                            background: 'rgba(255, 255, 255, 0.1)',
                            backdropFilter: 'blur(10px)',
                            color: '#fff',
                            border: '1px solid rgba(255, 255, 255, 0.2)',
                        },
                    }}
                />
            </div>
        </BrowserRouter>
    );
}

export default App;
