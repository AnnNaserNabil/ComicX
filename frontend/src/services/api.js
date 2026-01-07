import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Comic Generation API
export const comicAPI = {
    // Generate comic from text
    generateFromText: async (data) => {
        const formData = new FormData();
        formData.append('text', data.text);
        formData.append('title', data.title);
        formData.append('art_style', data.artStyle);
        formData.append('target_pages', data.targetPages);
        formData.append('target_audience', data.targetAudience);

        const response = await api.post('/api/v1/generate', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return response.data;
    },

    // Generate comic from PDF
    generateFromPDF: async (file, options) => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('art_style', options.artStyle);
        formData.append('target_pages', options.targetPages);
        formData.append('target_audience', options.targetAudience);

        const response = await api.post('/api/v1/generate', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return response.data;
    },

    // Get generation status
    getStatus: async (jobId) => {
        const response = await api.get(`/api/v1/status/${jobId}`);
        return response.data;
    },

    // Download comic
    downloadComic: async (jobId, format = 'pdf') => {
        const response = await api.get(`/api/v1/download/${jobId}`, {
            params: { format },
            responseType: 'blob',
        });
        return response.data;
    },

    // Get all comics
    getAllComics: async () => {
        const response = await api.get('/api/v1/comics');
        return response.data;
    },
};

// Story Generation API
export const storyAPI = {
    // Generate story with AI
    generateStory: async (prompt, options) => {
        const response = await api.post('/api/v1/story/generate', {
            prompt,
            genre: options.genre,
            themes: options.themes,
            num_chapters: options.numChapters || 5,
        });
        return response.data;
    },
};

// Health check
export const healthCheck = async () => {
    const response = await api.get('/health');
    return response.data;
};

export default api;
