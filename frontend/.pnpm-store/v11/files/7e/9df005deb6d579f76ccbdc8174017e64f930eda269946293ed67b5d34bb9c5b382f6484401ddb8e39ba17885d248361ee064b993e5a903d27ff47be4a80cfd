import type { RequestEvent } from '@sveltejs/kit';
/**
 * Takes a request event and extracts traceparent and DSC data
 * from the `sentry-trace` and `baggage` DSC headers.
 *
 * Sets propagation context as a side effect.
 */
export declare function getTracePropagationData(event: RequestEvent): {
    sentryTrace: string;
    baggage: string | null;
};
/**
 * Extracts a server-side sveltekit error, filters a couple of known errors we don't want to capture
 * and captures the error via `captureException`.
 *
 * @param e error
 *
 * @returns an objectified version of @param e
 */
export declare function sendErrorToSentry(e: unknown, handlerFn: 'handle' | 'load' | 'server_route'): object;
//# sourceMappingURL=utils.d.ts.map