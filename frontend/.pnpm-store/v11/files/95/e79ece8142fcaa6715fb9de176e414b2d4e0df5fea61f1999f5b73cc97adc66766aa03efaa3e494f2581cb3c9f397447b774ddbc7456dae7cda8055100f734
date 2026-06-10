import type { Plugin, UserConfig } from 'vite';
import type { BackwardsForwardsCompatibleSvelteConfig } from './svelteConfig';
import type { CustomSentryVitePluginOptions } from './types';
/**
 * Creates a new Vite plugin that uses the unplugin-based Sentry Vite plugin to create
 * releases and upload source maps to Sentry.
 *
 * Because the unplugin-based Sentry Vite plugin doesn't work ootb with SvelteKit,
 * we need to add some additional stuff to make source maps work:
 *
 * - the `config` hook needs to be added to generate source maps
 * - the `configResolved` hook tells us when to upload source maps.
 *   We only want to upload once at the end, given that SvelteKit makes multiple builds
 * - the `closeBundle` hook is used to flatten server source maps, which at the moment is necessary for SvelteKit.
 *   After the maps are flattened, they're uploaded to Sentry as in the original plugin.
 *   see: https://github.com/sveltejs/kit/discussions/9608
 *
 * @returns the custom Sentry Vite plugin
 */
export declare function makeCustomSentryVitePlugins(options: CustomSentryVitePluginOptions, svelteConfig: BackwardsForwardsCompatibleSvelteConfig): Promise<Plugin[]>;
/** There are 3 ways to set up source map generation (https://github.com/getsentry/sentry-j avascript/issues/13993)
 *
 *     1. User explicitly disabled source maps
 *       - keep this setting (emit a warning that errors won't be unminified in Sentry)
 *       - We won't upload anything
 *
 *     2. Users enabled source map generation (true, 'hidden', 'inline').
 *       - keep this setting (don't do anything - like deletion - besides uploading)
 *
 *     3. Users didn't set source maps generation
 *       - we enable 'hidden' source maps generation
 *       - configure `filesToDeleteAfterUpload` to delete all .map files (we emit a log about this)
 *
 * --> only exported for testing
 */
export declare function _getUpdatedSourceMapSettings(viteConfig: UserConfig, sentryPluginOptions?: CustomSentryVitePluginOptions): boolean | 'inline' | 'hidden';
//# sourceMappingURL=sourceMaps.d.ts.map