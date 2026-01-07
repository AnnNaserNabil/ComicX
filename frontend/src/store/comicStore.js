import { create } from 'zustand';

export const useComicStore = create((set, get) => ({
    // State
    comics: [],
    currentComic: null,
    generationStatus: null,
    isGenerating: false,
    error: null,

    // Actions
    setComics: (comics) => set({ comics }),

    setCurrentComic: (comic) => set({ currentComic: comic }),

    setGenerationStatus: (status) => set({ generationStatus: status }),

    setIsGenerating: (isGenerating) => set({ isGenerating }),

    setError: (error) => set({ error }),

    addComic: (comic) => set((state) => ({
        comics: [comic, ...state.comics],
    })),

    updateComicStatus: (jobId, status) => set((state) => ({
        comics: state.comics.map((comic) =>
            comic.job_id === jobId ? { ...comic, ...status } : comic
        ),
    })),

    clearError: () => set({ error: null }),

    reset: () => set({
        currentComic: null,
        generationStatus: null,
        isGenerating: false,
        error: null,
    }),
}));

export const useSettingsStore = create((set) => ({
    // Settings state
    artStyle: 'cartoon',
    targetPages: 20,
    targetAudience: 'general',
    outputFormats: ['pdf'],

    // Actions
    setArtStyle: (artStyle) => set({ artStyle }),
    setTargetPages: (targetPages) => set({ targetPages }),
    setTargetAudience: (targetAudience) => set({ targetAudience }),
    setOutputFormats: (outputFormats) => set({ outputFormats }),

    resetSettings: () => set({
        artStyle: 'cartoon',
        targetPages: 20,
        targetAudience: 'general',
        outputFormats: ['pdf'],
    }),
}));
