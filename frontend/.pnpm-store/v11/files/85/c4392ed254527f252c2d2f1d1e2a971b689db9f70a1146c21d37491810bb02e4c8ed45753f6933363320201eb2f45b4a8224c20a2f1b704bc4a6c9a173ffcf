import { httpIntegration as originalHttpIntegration } from '@sentry/node';
type HttpOptions = Parameters<typeof originalHttpIntegration>[0];
/**
 * The http integration instruments Node's internal http and https modules.
 * It creates breadcrumbs and spans for outgoing HTTP requests which will be attached to the currently active span.
 *
 * For SvelteKit, does not create spans for incoming requests but instead we use SvelteKit's own spans.
 * If you need to create incoming spans, set the `disableIncomingRequestSpans` option to `false`.
 * (You likely don't need this!)
 *
 */
export declare const httpIntegration: (options?: HttpOptions) => import("@sentry/core").Integration;
export {};
//# sourceMappingURL=http.d.ts.map