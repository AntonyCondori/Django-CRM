Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');
const svelte = require('@sentry/svelte');
const utils = require('../common/utils.js');

function sendErrorToSentry(e) {
  // In case we have a primitive, wrap it in the equivalent wrapper class (string -> String, etc.) so that we can
  // store a seen flag on it.
  const objectifiedErr = core.objectify(e);

  // We don't want to capture thrown `Redirect`s as these are not errors but expected behaviour
  // Neither 4xx errors, given that they are not valuable.
  if (
    utils.isRedirect(objectifiedErr) ||
    (utils.isHttpError(objectifiedErr) && objectifiedErr.status < 500 && objectifiedErr.status >= 400)
  ) {
    return objectifiedErr;
  }

  svelte.captureException(objectifiedErr, {
    mechanism: {
      type: 'auto.function.sveltekit.load',
      handled: false,
    },
  });

  return objectifiedErr;
}

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
// The liberal generic typing of `T` is necessary because we cannot let T extend `Load`.
// This function needs to tell TS that it returns exactly the type that it was called with
// because SvelteKit generates the narrowed down `PageLoad` or `LayoutLoad` types
// at build time for every route.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function wrapLoadWithSentry(origLoad) {
  return new Proxy(origLoad, {
    apply: (wrappingTarget, thisArg, args) => {
      // Type casting here because `T` cannot extend `Load` (see comment above function signature)
      const event = args[0] ;

      // Check if already wrapped
      if (event.__sentry_wrapped__) {
        return wrappingTarget.apply(thisArg, args);
      }

      const patchedEvent = {
        ...event,
      };

      core.addNonEnumerableProperty(patchedEvent , '__sentry_wrapped__', true);

      const routeId = utils.getRouteId(event);

      return core.startSpan(
        {
          op: 'function.sveltekit.load',
          attributes: {
            [core.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.function.sveltekit',
            [core.SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: routeId ? 'route' : 'url',
          },
          name: routeId ? routeId : event.url.pathname,
        },
        () => core.handleCallbackErrors(() => wrappingTarget.apply(thisArg, [patchedEvent]), sendErrorToSentry),
      );
    },
  });
}

exports.wrapLoadWithSentry = wrapLoadWithSentry;
//# sourceMappingURL=load.js.map
