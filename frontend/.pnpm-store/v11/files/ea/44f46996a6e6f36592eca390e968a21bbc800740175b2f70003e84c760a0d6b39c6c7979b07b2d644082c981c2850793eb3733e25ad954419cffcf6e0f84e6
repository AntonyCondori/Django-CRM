import type { Handle, ResolveOptions } from '@sveltejs/kit';
export type SentryHandleOptions = {
    /**
     * Controls whether the SDK should capture errors and traces in requests that don't belong to a
     * route defined in your SvelteKit application.
     *
     * By default, this option is set to `false` to reduce noise (e.g. bots sending random requests to your server).
     *
     * Set this option to `true` if you want to monitor requests events without a route. This might be useful in certain
     * scenarios, for instance if you registered other handlers that handle these requests.
     * If you set this option, you might want adjust the the transaction name in the `beforeSendTransaction`
     * callback of your server-side `Sentry.init` options. You can also use `beforeSendTransaction` to filter out
     * transactions that you still don't want to be sent to Sentry.
     *
     * @default false
     */
    handleUnknownRoutes?: boolean;
    /**
     * Controls if `sentryHandle` should inject a script tag into the page that enables instrumentation
     * of `fetch` calls in `load` functions.
     *
     * @default true
     */
    injectFetchProxyScript?: boolean;
};
export declare const FETCH_PROXY_SCRIPT = "\n    const f = window.fetch;\n    if(f){\n      window._sentryFetchProxy = function(...a){return f(...a)}\n      window.fetch = function(...a){return window._sentryFetchProxy(...a)}\n    }\n";
/**
 * Adds Sentry tracing <meta> tags to the returned html page.
 * Adds Sentry fetch proxy script to the returned html page if enabled in options.
 *
 * Exported only for testing
 */
export declare function addSentryCodeToPage(options: {
    injectFetchProxyScript: boolean;
}): NonNullable<ResolveOptions['transformPageChunk']>;
/**
 * We only need to inject the fetch proxy script for SvelteKit versions < 2.16.0.
 * Exported only for testing.
 */
export declare function isFetchProxyRequired(version: string): boolean;
/**
 * A SvelteKit handle function that wraps the request for Sentry error and
 * performance monitoring.
 *
 * Usage:
 * ```
 * // src/hooks.server.ts
 * import { sentryHandle } from '@sentry/sveltekit';
 *
 * export const handle = sentryHandle();
 *
 * // Optionally use the `sequence` function to add additional handlers.
 * // export const handle = sequence(sentryHandle(), yourCustomHandler);
 * ```
 */
export declare function sentryHandle(handlerOptions?: SentryHandleOptions): Handle;
//# sourceMappingURL=handle.d.ts.map