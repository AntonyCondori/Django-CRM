import type { Plugin } from 'vite';
export type AutoInstrumentSelection = {
    /**
     * If this flag is `true`, the Sentry plugins will automatically instrument the `load` function of
     * your universal `load` functions declared in your `+page.(js|ts)` and `+layout.(js|ts)` files.
     *
     * @default true
     */
    load?: boolean;
    /**
     * If this flag is `true`, the Sentry plugins will automatically instrument the `load` function of
     * your server-only `load` functions declared in your `+page.server.(js|ts)`
     * and `+layout.server.(js|ts)` files.
     *
     * @default true
     */
    serverLoad?: boolean;
};
type AutoInstrumentPluginOptions = AutoInstrumentSelection & {
    debug: boolean;
    onlyInstrumentClient: boolean;
};
/**
 * Creates a Vite plugin that automatically instruments the parts of the app
 * specified in @param options. This includes
 *
 * - universal `load` functions from `+page.(js|ts)` and `+layout.(js|ts)` files
 * - server-only `load` functions from `+page.server.(js|ts)` and `+layout.server.(js|ts)` files
 *
 * @returns the plugin
 */
export declare function makeAutoInstrumentationPlugin(options: AutoInstrumentPluginOptions): Plugin;
/**
 * We only want to apply our wrapper to files that
 *
 *  - Have no Sentry code yet in them. This is to avoid double-wrapping or interfering with custom
 *    Sentry calls.
 *  - Actually declare a `load` function. The second check of course is not 100% accurate, but it's good enough.
 *    Injecting our wrapper into files that don't declare a `load` function would result in a build-time warning
 *    because vite/rollup warns if we reference an export from the user's file in our wrapping code that
 *    doesn't exist.
 *
 * Exported for testing
 *
 * @returns `true` if we can wrap the given file, `false` otherwise
 */
export declare function canWrapLoad(id: string, debug: boolean): Promise<boolean>;
export {};
//# sourceMappingURL=autoInstrument.d.ts.map