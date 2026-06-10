import type { HttpError, Redirect } from '@sveltejs/kit';
export declare const WRAPPED_MODULE_SUFFIX = "?sentry-auto-wrap";
export type SentryWrappedFlag = {
    /**
     * If this flag is set, we know that the load event was already wrapped once
     * and we shouldn't wrap it again.
     */
    __sentry_wrapped__?: true;
};
interface EventLike {
    route?: {
        id?: string | null;
    };
    untrack<T>(fn: () => T): T;
}
/**
 * Get route.id from a load event without triggering SvelteKit's route proxy
 * (which would cause unwanted invalidations). Uses `untrack` when available (SvelteKit 2+),
 * otherwise falls back to getOwnPropertyDescriptor for SvelteKit 1.x.
 */
export declare function getRouteId(event: EventLike): string | void;
/**
 * Determines if a thrown "error" is a Redirect object which SvelteKit users can throw to redirect to another route
 * see: https://kit.svelte.dev/docs/modules#sveltejs-kit-redirect
 * @param error the potential redirect error
 */
export declare function isRedirect(error: unknown): error is Redirect;
/**
 * Determines if a thrown "error" is a HttpError
 */
export declare function isHttpError(err: unknown): err is HttpError;
export {};
//# sourceMappingURL=utils.d.ts.map