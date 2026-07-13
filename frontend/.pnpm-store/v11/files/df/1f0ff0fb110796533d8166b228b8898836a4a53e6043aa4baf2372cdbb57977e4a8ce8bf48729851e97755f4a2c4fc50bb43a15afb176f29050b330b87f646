Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');
const utils = require('../common/utils.js');
const utils$1 = require('./utils.js');

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

      core.addNonEnumerableProperty(event , '__sentry_wrapped__', true);

      const routeId = utils.getRouteId(event);

      try {
        // We need to await before returning, otherwise we won't catch any errors thrown by the load function
        return await core.startSpan(
          {
            op: 'function.sveltekit.load',
            attributes: {
              [core.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.function.sveltekit',
              [core.SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: routeId ? 'route' : 'url',
            },
            name: routeId ? routeId : event.url.pathname,
          },
          () => wrappingTarget.apply(thisArg, args),
        );
      } catch (e) {
        utils$1.sendErrorToSentry(e, 'load');
        throw e;
      } finally {
        await core.flushIfServerless();
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

      core.addNonEnumerableProperty(event , '__sentry_wrapped__', true);

      // Accessing any member of `event.route` causes SvelteKit to invalidate the
      // server `load` function's data on every route change. We use `getRouteId` which uses
      // SvelteKit 2's `untrack` when available, otherwise getOwnPropertyDescriptor for 1.x.
      const routeId = utils.getRouteId(event);

      try {
        // We need to await before returning, otherwise we won't catch any errors thrown by the load function
        return await core.startSpan(
          {
            op: 'function.sveltekit.server.load',
            attributes: {
              [core.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.function.sveltekit',
              [core.SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: routeId ? 'route' : 'url',
              'http.method': event.request.method,
            },
            name: routeId ? routeId : event.url.pathname,
          },
          () => wrappingTarget.apply(thisArg, args),
        );
      } catch (e) {
        utils$1.sendErrorToSentry(e, 'load');
        throw e;
      } finally {
        await core.flushIfServerless();
      }
    },
  });
}

exports.wrapLoadWithSentry = wrapLoadWithSentry;
exports.wrapServerLoadWithSentry = wrapServerLoadWithSentry;
//# sourceMappingURL=load.js.map
