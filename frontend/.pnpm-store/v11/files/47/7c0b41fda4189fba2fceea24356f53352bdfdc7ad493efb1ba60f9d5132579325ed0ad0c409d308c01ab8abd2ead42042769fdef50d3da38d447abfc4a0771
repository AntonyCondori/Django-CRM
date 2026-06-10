import { type InternalGlobal } from '@sentry/core';
import type { Plugin } from 'vite';
import { type BackwardsForwardsCompatibleSvelteConfig } from './svelteConfig';
import type { SentrySvelteKitPluginOptions } from './types';
export type GlobalSentryValues = {
    __sentry_sveltekit_output_dir?: string;
};
/**
 * Extend the `global` type with custom properties that are
 * injected by the SvelteKit SDK at build time.
 * @see packages/sveltekit/src/vite/sourcemaps.ts
 */
export type GlobalWithSentryValues = InternalGlobal & GlobalSentryValues;
export declare const VIRTUAL_GLOBAL_VALUES_FILE = "\0sentry-inject-global-values-file";
/**
 * @returns code that injects @param globalSentryValues into the global object.
 */
export declare function getGlobalValueInjectionCode(globalSentryValues: GlobalSentryValues): string;
/**
 * Injects SvelteKit app configuration values the svelte.config.js into the
 * server's global object so that the SDK can pick up the information at runtime
 */
export declare function makeGlobalValuesInjectionPlugin(svelteConfig: BackwardsForwardsCompatibleSvelteConfig, options: Pick<SentrySvelteKitPluginOptions, 'adapter' | 'debug'>): Promise<Plugin>;
//# sourceMappingURL=injectGlobalValues.d.ts.map