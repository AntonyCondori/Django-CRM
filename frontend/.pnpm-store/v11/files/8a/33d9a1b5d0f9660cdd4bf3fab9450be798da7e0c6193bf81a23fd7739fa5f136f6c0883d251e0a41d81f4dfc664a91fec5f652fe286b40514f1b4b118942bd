Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');
const utils = require('./utils.js');

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
function wrapServerRouteWithSentry(
  originalRouteHandler,
) {
  return new Proxy(originalRouteHandler, {
    apply: async (wrappingTarget, thisArg, args) => {
      const event = args[0] ;

      if (event.__sentry_wrapped__) {
        return wrappingTarget.apply(thisArg, args);
      }

      const routeId = event.route?.id;
      const httpMethod = event.request.method;

      core.addNonEnumerableProperty(event , '__sentry_wrapped__', true);

      try {
        return await core.startSpan(
          {
            name: `${httpMethod} ${routeId || 'Server Route'}`,
            op: `function.sveltekit.server.${httpMethod.toLowerCase()}`,
            attributes: {
              [core.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.function.sveltekit',
              [core.SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: 'route',
            },
            onlyIfParent: true,
          },
          () => wrappingTarget.apply(thisArg, args),
        );
      } catch (e) {
        utils.sendErrorToSentry(e, 'server_route');
        throw e;
      } finally {
        await core.flushIfServerless();
      }
    },
  });
}

exports.wrapServerRouteWithSentry = wrapServerRouteWithSentry;
//# sourceMappingURL=serverRoute.js.map
