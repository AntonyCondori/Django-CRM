import { defineIntegration, debug, getActiveSpan, updateSpanName, getRootSpan, getIsolationScope, captureException, getClient } from '@sentry/core';
import { DEBUG_BUILD } from '../debug-build.js';

const INTEGRATION_NAME = 'Hono';

/** Only exported for internal use */
function getHonoIntegration() {
  return getClient()?.getIntegrationByName(INTEGRATION_NAME);
}

function isHonoError(err) {
  if (err instanceof Error) {
    return true;
  }
  return typeof err === 'object' && err !== null && 'status' in (err );
}

// Vendored from https://github.com/honojs/hono/blob/d3abeb1f801aaa1b334285c73da5f5f022dbcadb/src/helper/route/index.ts#L58-L59
const routePath = (c) => c.req?.path ?? '';

const _honoIntegration = ((options = {}) => {
  return {
    name: INTEGRATION_NAME,
    // Hono error handler: https://github.com/honojs/hono/blob/d3abeb1f801aaa1b334285c73da5f5f022dbcadb/src/hono-base.ts#L35
    handleHonoException(err, context) {
      const shouldHandleError = options.shouldHandleError || defaultShouldHandleError;

      if (!isHonoError(err)) {
        DEBUG_BUILD && debug.log("[Hono] Won't capture exception in `onError` because it's not a Hono error.", err);
        return;
      }

      if (shouldHandleError(err)) {
        if (context) {
          const activeSpan = getActiveSpan();
          const spanName = `${context.req.method} ${routePath(context)}`;

          if (activeSpan) {
            activeSpan.updateName(spanName);
            updateSpanName(getRootSpan(activeSpan), spanName);
          }

          getIsolationScope().setTransactionName(spanName);
        }

        captureException(err, { mechanism: { handled: false, type: 'auto.faas.hono.error_handler' } });
      } else {
        DEBUG_BUILD && debug.log('[Hono] Not capturing exception because `shouldHandleError` returned `false`.', err);
      }
    },
  };
}) ;

/**
 * Automatically captures exceptions caught with the `onError` handler in Hono.
 *
 * The integration is enabled by default.
 *
 * @example
 * integrations: [
 *   honoIntegration({
 *     shouldHandleError: (err) => true; // always capture exceptions in onError
 *   })
 * ]
 */
const honoIntegration = defineIntegration(_honoIntegration);

/**
 * Default function to determine if an error should be sent to Sentry
 *
 * 3xx and 4xx errors are not sent by default.
 */
function defaultShouldHandleError(error) {
  const statusCode = error?.status;
  // 3xx and 4xx errors are not sent by default.
  return statusCode ? statusCode >= 500 || statusCode <= 299 : true;
}

export { getHonoIntegration, honoIntegration };
//# sourceMappingURL=hono.js.map
