import type { BackwardsForwardsCompatibleSvelteConfig } from './svelteConfig';
/**
 * Supported @sveltejs/adapters-[adapter] SvelteKit adapters
 */
export type SupportedSvelteKitAdapters = 'node' | 'auto' | 'vercel' | 'cloudflare' | 'other';
/**
 * Tries to detect the used adapter for SvelteKit.
 * 1. If svelteConfig is provided and has kit.adapter.name, uses that (source of truth from svelte.config.js).
 * 2. Otherwise falls back to inferring from package.json dependencies.
 * Returns the name of the adapter or 'other' if no supported adapter was found.
 *
 * @param svelteConfig - Loaded svelte config (e.g. from loadSvelteConfig()). Pass `undefined` to skip config-based detection.
 * @param debug - Whether to log detection result. Pass `undefined` for false.
 */
export declare function detectAdapter(svelteConfig: BackwardsForwardsCompatibleSvelteConfig | undefined, debug: boolean | undefined): Promise<SupportedSvelteKitAdapters>;
//# sourceMappingURL=detectAdapter.d.ts.map