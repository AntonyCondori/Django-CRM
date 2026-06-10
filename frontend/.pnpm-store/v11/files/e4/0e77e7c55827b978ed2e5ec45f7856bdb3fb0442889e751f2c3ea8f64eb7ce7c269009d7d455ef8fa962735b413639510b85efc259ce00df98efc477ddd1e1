import type { RequestEvent } from '@sveltejs/kit';
/**
 * Wraps a server route handler for API or server routes registered in `+server.(js|js)` files.
 *
 * This function will automatically capture any errors that occur during the execution of the route handler
 * and it will start a span for the duration of your route handler.
 *
 * @example
 * ```js
 * import { wrapServerRouteWithSentry } from '@sentry/sveltekit';
 *
 * const get = async event => {
 *   return new Response(JSON.stringify({ message: 'hello world' }));
 * }
 *
 * export const GET = wrapServerRouteWithSentry(get);
 * ```
 *
 * @param originalRouteHandler your server route handler
 * @param httpMethod the HTTP method of your route handler
 *
 * @returns a wrapped version of your server route handler
 */
export declare function wrapServerRouteWithSentry<T extends RequestEvent>(originalRouteHandler: (request: T) => Promise<Response>): (requestEvent: T) => Promise<Response>;
//# sourceMappingURL=serverRoute.d.ts.map