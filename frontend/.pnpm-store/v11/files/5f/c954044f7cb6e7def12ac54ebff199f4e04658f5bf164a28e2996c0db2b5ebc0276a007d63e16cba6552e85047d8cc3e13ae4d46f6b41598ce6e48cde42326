import type { Config } from '@sveltejs/kit';
import type { SupportedSvelteKitAdapters } from './detectAdapter';
export type SvelteKitTracingConfig = {
    tracing?: {
        server: boolean;
    };
    instrumentation?: {
        server: boolean;
    };
};
/**
 * Experimental tracing and instrumentation config is available @since 2.31.0
 * // TODO: Once instrumentation and tracing is promoted stable, adjust this type!s
 */
type BackwardsForwardsCompatibleKitConfig = Config['kit'] & {
    experimental?: SvelteKitTracingConfig;
};
export interface BackwardsForwardsCompatibleSvelteConfig extends Config {
    kit?: BackwardsForwardsCompatibleKitConfig;
}
/**
 * Imports the svelte.config.js file and returns the config object.
 * The sveltekit plugins import the config in the same way.
 * See: https://github.com/sveltejs/kit/blob/master/packages/kit/src/core/config/index.js#L63
 */
export declare function loadSvelteConfig(): Promise<BackwardsForwardsCompatibleSvelteConfig>;
/**
 * Reads a custom hooks directory from the SvelteKit config. In case no custom hooks
 * directory is specified, the default directory is returned.
 */
export declare function getHooksFileName(svelteConfig: Config, hookType: 'client' | 'server'): string;
/**
 * Attempts to read a custom output directory that can be specified in the options
 * of a SvelteKit adapter. If no custom output directory is specified, the default
 * directory is returned.
 */
export declare function getAdapterOutputDir(svelteConfig: Config, adapter: SupportedSvelteKitAdapters): Promise<string>;
export {};
//# sourceMappingURL=svelteConfig.d.ts.map