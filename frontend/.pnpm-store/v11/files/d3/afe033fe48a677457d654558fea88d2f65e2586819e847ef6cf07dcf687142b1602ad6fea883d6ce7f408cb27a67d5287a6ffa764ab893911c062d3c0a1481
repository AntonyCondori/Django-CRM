import type { Plugin } from 'vite';
import type { CustomSentryVitePluginOptions, SentrySvelteKitPluginOptions } from './types';
/**
 * Vite Plugins for the Sentry SvelteKit SDK, taking care of creating
 * Sentry releases and uploading source maps to Sentry.
 *
 * Sentry adds a few additional properties to your Vite config.
 * Make sure, it is registered before the SvelteKit plugin.
 */
export declare function sentrySvelteKit(options?: SentrySvelteKitPluginOptions): Promise<Plugin[]>;
/**
 * This function creates the options for the custom Sentry Vite plugin.
 * The options are derived from the Sentry SvelteKit plugin options, where the `_unstable` options take precedence.
 *
 * only exported for testing
 */
export declare function generateVitePluginOptions(svelteKitPluginOptions: SentrySvelteKitPluginOptions): CustomSentryVitePluginOptions | null;
//# sourceMappingURL=sentryVitePlugins.d.ts.map