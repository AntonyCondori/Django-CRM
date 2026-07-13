import { addNonEnumerableProperty, startSpan, SEMANTIC_ATTRIBUTE_SENTRY_SOURCE, SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN, flushIfServerless } from '@sentry/core';
import { getRouteId } from '../common/utils.js';
import { sendErrorToSentry } from './utils.js';

/**
 * @inheritdoc
 */
// The liberal generic typing of `T` is necessary because we cannot let T extend `Load`.
// This function needs to tell TS that it returns exactly the type that it was called with
// because SvelteKit generates the narrowed down `PageLoad` or `LayoutLoad` types
// at build time for every route.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function wrapLoadWithSentry(origLoad) {
  return new Proxy(origLoad, {
    apply: async (wrappingTarget, thisArg, args) => {
      // Type casting here because `T` cannot extend `Load` (see comment above function signature)
      // Also, this event possibly already has a sentry wrapped flag attached
      const event = args[0] ;

      if (event.__sentry_wrapped__) {
        return wrappingTarget.apply(thisArg, args);
      }

      addNonEnumerableProperty(event , '__sentry_wrapped__', true);

      const routeId = getRouteId(event);

      try {
        // We need to await before returning, otherwise we won't catch any errors thrown by the load function
        return await startSpan(
          {
            op: 'function.sveltekit.load',
            attributes: {
              [SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.function.sveltekit',
              [SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: routeId ? 'route' : 'url',
            },
            name: routeId ? routeId : event.url.pathname,
          },
          () => wrappingTarget.apply(thisArg, args),
        );
      } catch (e) {
        sendErrorToSentry(e, 'load');
        throw e;
      } finally {
        await flushIfServerless();
      }
    },
  });
}

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
// The liberal generic typing of `T` is necessary because we cannot let T extend `ServerLoad`.
// This function needs to tell TS that it returns exactly the type that it was called with
// because SvelteKit generates the narrowed down `PageServerLoad` or `LayoutServerLoad` types
// at build time for every route.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function wrapServerLoadWithSentry(origServerLoad) {
  return new Proxy(origServerLoad, {
    apply: async (wrappingTarget, thisArg, args) => {
      // Type casting here because `T` cannot extend `ServerLoad` (see comment above function signature)
      // Also, this event possibly already has a sentry wrapped flag attached
      const event = args[0] ;

      if (event.__sentry_wrapped__) {
        return wrappingTarget.apply(thisArg, args);
      }

      addNonEnumerableProperty(event , '__sentry_wrapped__', true);

      // Accessing any member of `event.route` causes SvelteKit to invalidate the
      // server `load` function's data on every route change. We use `getRouteId` which uses
      // SvelteKit 2's `untrack` when available, otherwise getOwnPropertyDescriptor for 1.x.
      const routeId = getRouteId(event);

      try {
        // We need to await before returning, otherwise we won't catch any errors thrown by the load function
        return await startSpan(
          {
            op: 'function.sveltekit.server.load',
            attributes: {
              [SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.function.sveltekit',
              [SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: routeId ? 'route' : 'url',
              'http.method': event.request.method,
            },
            name: routeId ? routeId : event.url.pathname,
          },
          () => wrappingTarget.apply(thisArg, args),
        );
      } catch (e) {
        sendErrorToSentry(e, 'load');
        throw e;
      } finally {
        await flushIfServerless();
      }
    },
  });
}

export { wrapLoadWithSentry, wrapServerLoadWithSentry };
//# sourceMappingURL=load.js.map
