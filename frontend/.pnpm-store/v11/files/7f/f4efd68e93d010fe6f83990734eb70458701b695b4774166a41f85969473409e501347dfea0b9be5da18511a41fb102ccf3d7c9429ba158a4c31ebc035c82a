/**
 * @inheritdoc
 */
export declare function wrapLoadWithSentry<T extends (...args: any) => any>(origLoad: T): T;
/**
 * Wrap a server-only load function (e.g. +page.server.js or +layout.server.js) with Sentry functionality
 *
 * Usage:
 *
 * ```js
 * // +page.serverjs
 *
 * import { wrapServerLoadWithSentry }
 *
 * export const load = wrapServerLoadWithSentry((event) => {
 *   // your load code
 * });
 * ```
 *
 * @param origServerLoad SvelteKit user defined server-only load function
 */
export declare function wrapServerLoadWithSentry<T extends (...args: any) => any>(origServerLoad: T): T;
//# sourceMappingURL=load.d.ts.map