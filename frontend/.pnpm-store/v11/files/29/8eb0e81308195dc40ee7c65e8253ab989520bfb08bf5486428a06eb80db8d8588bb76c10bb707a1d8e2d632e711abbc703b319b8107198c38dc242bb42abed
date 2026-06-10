/**
 * Wrap load function with Sentry. This wrapper will
 *
 * - catch errors happening during the execution of `load`
 * - create a load span if performance monitoring is enabled
 * - attach tracing Http headers to `fetch` requests if performance monitoring is enabled to get connected traces.
 * - add a fetch breadcrumb for every `fetch` request
 *
 * Note that tracing Http headers are only attached if the url matches the specified `tracePropagationTargets`
 * entries to avoid CORS errors.
 *
 * @param origLoad SvelteKit user defined load function
 */
export declare function wrapLoadWithSentry<T extends (...args: any) => any>(origLoad: T): T;
//# sourceMappingURL=load.d.ts.map